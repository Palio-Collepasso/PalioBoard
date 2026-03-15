import { test, expect } from '@playwright/test';

test('root resolves to the public shell', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveURL(/\/public(?:\/)?$/);
  await expect(page.getByRole('heading', { name: 'Public scaffold', exact: true })).toBeVisible();
});

const shellChecks = [
  { path: '/admin', heading: 'Admin scaffold', cards: 2 },
  { path: '/public', heading: 'Public scaffold', cards: 2 },
  { path: '/maxi', heading: 'Maxi-screen scaffold', cards: 1 }
] as const;

for (const shell of shellChecks) {
  test(`${shell.path} renders the expected shell scaffold`, async ({ page }) => {
    await page.goto(shell.path);

    await expect(page.getByRole('heading', { name: shell.heading })).toBeVisible();
    await expect(page.locator('.placeholder-card')).toHaveCount(shell.cards);
  });
}
