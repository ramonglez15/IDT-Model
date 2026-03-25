# /dream

Maintain and evolve your cognitive hierarchy through the Dream workflow.

## Usage
- `/dream` - Run Dream Status to check all dimensions and decide next action

## Execute

```bash
contxos :: execute_compact '{"intent": "dream", "branch": "Dream Status"}'
```

Follow the workflow guidance returned by the branch. The response includes template names only. To get full details (recipe, function parameters) for any template, drill down with:

```bash
contxos :: template_detail '{"name": "Template Name Here"}'
```

ARGUMENTS: $ARGUMENTS
