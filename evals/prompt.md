## Tasks

### Create tasks from milestone
Given the milestone `@m-x`, decompose it into tasks following the Backlog.md workflow. Use proper labels, keeping frontend and api tasks distinct.

### Work on a task

- **Before starting a task**: Work on `TASK-x` only. Research the codebase and write an implementation plan in the task. Wait for my approval before coding.
- **Approve the plan**: plan approved
- **When ready to push**: Commit and create PR

### Work in parallel on multiple subtasks
Given the task `x`:

1. Spawn a sub-agent for each subtask and ask them to come up with the implementation plan according to the Backlog.md workflow
2. Review the implementation plans and approve them when they are OK; otherwise, give the necessary feedback to fix them
3. When all subtasks have an implementation plan, let me know and I will do a final review and approve task execution

Review the code and check whether you may simplify it or it needs a refactoring. Check
  whether some logic needs to be extracted and shared or whether you re-implemented something used somewhere else