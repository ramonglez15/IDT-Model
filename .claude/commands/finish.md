# /finish

Complete a session by capturing accomplishments, decisions, pending work, and blockers.

## Usage
- `/finish` - Complete the current session

## Determine Workflow

Check if a handoff was loaded at session start:

### If handoff was loaded → Complete Handoff

```bash
contxos :: execute_compact '{"intent": "handoff", "branch": "complete handoff"}'
```

### If no handoff loaded → Complete Chat

```bash
contxos :: execute_compact '{"intent": "capture", "branch": "Complete Chat"}'
```

Follow the workflow guidance returned by the branch. The response includes template names only. To get full details (recipe, function parameters) for any template, drill down with:

```bash
contxos :: template_detail '{"name": "Template Name Here"}'
```

ARGUMENTS: $ARGUMENTS
