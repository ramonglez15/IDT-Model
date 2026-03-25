# /projects

Manage ContxOS projects — list, create, switch, or rename projects.

## Usage
- `/projects` - Open the projects management branch

## Execute

```bash
contxos :: execute_compact '{"intent": "welcome", "branch": "Contxos Projects"}'
```

Follow the workflow guidance returned by the branch. The response includes template names only. To get full details (recipe, function parameters) for any template, drill down with:

```bash
contxos :: template_detail '{"name": "Template Name Here"}'
```

## Prerequisites

The CLI must be installed globally for project switching to work:

```bash
npm install -g @contxos/cli
```

## After Switching Projects

The CLI automatically updates its stored token when you run `switch_project` — no manual token management needed.

After switching, update the `project_id` in CLAUDE.md (replace all occurrences of the old UUID with the new one).

ARGUMENTS: $ARGUMENTS
