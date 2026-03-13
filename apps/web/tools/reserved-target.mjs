const [, , targetName, taskId] = process.argv;

if (!targetName || !taskId) {
  console.error('Usage: node ./tools/reserved-target.mjs <target-name> <task-id>');
  process.exit(1);
}

console.error(
  `${targetName} is still reserved for ${taskId}. TASK-3 only adds the Angular scaffold, routing shells, and boundary checks.`
);
process.exit(1);
