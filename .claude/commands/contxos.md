# /contxos

Execute ContxOS intelligent prompt routing with automatic tool discovery.

## Usage

`/contxos <prompt>` — Routes through ContxOS based on prompt structure:

### Routing rules

1. **Short prompt (1-2 words)** → pass to `contxos :: smart`
   Example: `/contxos lets resume`

2. **Longer prompt (3+ words)** → use `contxos :: grep` instead of `smart`
   Example: `/contxos how does the sync orchestrator work`

3. **Prompt with `|` separator** → only the text **before** `|` is the prompt; text **after** `|` is context/notes for you (the agent) and is NOT passed to any tool
   Example: `/contxos lets resume | pick up the intercompany work`
   → Prompt = `lets resume` (2 words → `smart`)
   → Notes = `pick up the intercompany work` (for your situational awareness only)

The `|` is optional. It only appears when the user wants to give you extra context while keeping the actual routed prompt short.

## Important: Start with ContxOS Tools

**Before searching files or reading code directly, use these discovery tools:**

```bash
# Search the knowledge hierarchy (concepts, abstracts, thoughts)
contxos :: grep '{"pattern": "your search query", "mode": "all"}'

# Search with artifact prioritization (for code-focused searches)
contxos :: grep '{"pattern": "function or table name", "prioritize": "artifacts"}'

# Search with workflow prioritization (for workflow-focused searches)
contxos :: grep '{"pattern": "your search query", "prioritize": "workflows"}'

# Drill into any result for full context
contxos :: unpack '{"id": "uuid-from-grep-results"}'
```

- `grep` searches semantically, not just text - it finds related decisions, plans, TODOs, and past work
- `grep` with `prioritize: "artifacts"` shows code artifacts (functions, views, tables) first - use when looking for code
- `grep` with `prioritize: "workflows"` shows workflow/flow/worker types first - use when looking for reusable procedures
- `unpack` reveals the full content and source chain of any concept/abstract/thought
- Local file grep and direct file reads waste context and miss institutional knowledge
- The knowledge hierarchy often contains the answer or points directly to the right files

## Execute

```bash
contxos :: smart '{"prompt": "USER_PROMPT_HERE"}'
```

## Important

- Replace `USER_PROMPT_HERE` with the routed prompt (text before `|` if present, otherwise the full prompt). Only use `smart` for 1-2 word prompts; use `grep` for longer ones.
- Don't modify the prompt - pass exactly what the user provides
- The system will automatically discover the tool and execute the appropriate branch
- Follow the workflow guidance returned by the query

## How It Works

This command uses ContxOS's intelligent tool discovery system to:
1. Analyze the user's prompt
2. Determine the most appropriate tool (handoff, workflow, dream, etc.)
3. Execute the corresponding branch with its templates
4. Return structured guidance for completing the task

The response will include the discovered branch, confidence level, and specific templates to execute.

## Following the Response

The response from ContxOS includes:
1. **Discovered tool and branch** - What the system determined you want to do
2. **Recipe** - Step-by-step instructions for completing the task
3. **Templates** - Executable functions with their parameters

**IMPORTANT**: The recipe contains the exact workflow you need to follow. Each template listed includes:
- The function name to execute (use with `contxos :: template_name`)
- Required parameters
- What it accomplishes

Always execute the templates in the order specified by the recipe. The system has already determined the optimal workflow for your request.

