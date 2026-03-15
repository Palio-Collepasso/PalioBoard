import { spawnSync } from 'node:child_process';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { setTimeout as delay } from 'node:timers/promises';

const currentFilePath = fileURLToPath(import.meta.url);
const toolsDirectory = dirname(currentFilePath);
const webDirectory = resolve(toolsDirectory, '..');
const repoRoot = resolve(webDirectory, '..', '..');
const composeFile = resolve(repoRoot, 'infra/compose/docker-compose.yml');
const playwrightBinary = resolve(
  webDirectory,
  'node_modules',
  '.bin',
  process.platform === 'win32' ? 'playwright.cmd' : 'playwright'
);
const explicitBaseUrl = process.env.PLAYWRIGHT_BASE_URL;
const baseUrl = explicitBaseUrl ?? 'http://127.0.0.1:8080';

process.env.PLAYWRIGHT_BASE_URL = baseUrl;

const manageStack = !(explicitBaseUrl ?? '').trim();
let shouldCleanupStack = false;
let exitCode = 1;

try {
  if (manageStack && !(await isReachable(baseUrl))) {
    shouldCleanupStack = true;
    runOrThrow('docker', ['compose', '-f', composeFile, 'up', '-d'], repoRoot);
    await waitForUrl(baseUrl, 120_000);
  }

  const testRun = spawnSync(playwrightBinary, ['test', ...process.argv.slice(2)], {
    cwd: webDirectory,
    env: process.env,
    stdio: 'inherit'
  });

  exitCode = testRun.status ?? 1;
} finally {
  if (shouldCleanupStack) {
    const cleanup = spawnSync('docker', ['compose', '-f', composeFile, 'down'], {
      cwd: repoRoot,
      env: process.env,
      stdio: 'inherit'
    });

    if (cleanup.status !== 0 && exitCode === 0) {
      exitCode = cleanup.status ?? 1;
    }
  }
}

process.exit(exitCode);

function runOrThrow(command, args, cwd) {
  const completed = spawnSync(command, args, {
    cwd,
    env: process.env,
    stdio: 'inherit'
  });

  if (completed.status === 0) {
    return;
  }

  throw new Error(`Command failed: ${command} ${args.join(' ')}`);
}

async function waitForUrl(url, timeoutMs) {
  const deadline = Date.now() + timeoutMs;

  while (Date.now() < deadline) {
    if (await isReachable(url)) {
      return;
    }

    await delay(1_000);
  }

  throw new Error(`Timed out waiting for ${url}`);
}

async function isReachable(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5_000);

  try {
    const response = await fetch(url, {
      method: 'GET',
      redirect: 'follow',
      signal: controller.signal
    });

    return response.ok;
  } catch {
    return false;
  } finally {
    clearTimeout(timeout);
  }
}
