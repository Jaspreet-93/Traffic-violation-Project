# Workspace Customization Rules

- **Automatic Git Push**:
  - After executing any command, modifying any file, or finishing a prompt response, the agent must check if there are any uncommitted, unstaged, or untracked changes in the workspace, or if there are local commits that have not been pushed.
  - If changes exist, the agent must automatically stage them, commit them with a descriptive commit message (e.g., "Sync project files after prompt work"), and push them to the remote repository `https://github.com/Jaspreet-93/Traffic-violation-Project.git` on the `main` branch.
