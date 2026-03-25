# /handoff

Create a comprehensive handoff to preserve your work session context.

## Usage
- `/handoff` - Create a standard handoff
- `/handoff "context"` - Create a handoff with additional context

## Execute

```bash
contxos :: execute_compact '{"intent": "handoff", "branch": "Create Handoff"}'
```

Follow the workflow guidance returned by the branch. The response includes template names only. To get full details (recipe, function parameters) for any template, drill down with:

```bash
contxos :: template_detail '{"name": "Template Name Here"}'
```

ARGUMENTS: $ARGUMENTS

To resume in next chat just use /contxos lets resume
