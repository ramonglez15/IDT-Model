# /blinders

**STOP. Put your blinders on and refocus.**

You just violated the **ContxOS-First** principle. Here's what you need to remember:

## The Critical Rule

**ALWAYS start with ContxOS tools (grep/unpack) before touching local files.**

Local files are just code. The knowledge base contains the **why**, the **decisions**, the **context**, and the **patterns** that matter.

## The Correct Workflow

```bash
# Step 1: Search the knowledge base FIRST
contxos :: grep '{"pattern": "your search query", "mode": "all"}'

# Step 2: Drill into results for full context
contxos :: unpack '{"id": "result-uuid-from-grep"}'

# Step 3 (ONLY IF NEEDED): Read specific files
# But usually the knowledge base already told you which files matter
```

## Why This Matters

- **grep** searches semantically across concepts, abstracts, and thoughts
- **grep** with `prioritize: "artifacts"` shows code artifacts first - use when looking for functions, views, tables
- **unpack** reveals full content and source chains
- **Knowledge base has context** - Decisions, TODOs, patterns, past work
- **Local files are dumb** - They don't know why they exist or what problem they solve
- **You waste context** - Reading random files without knowing which ones matter
- **You miss institutional knowledge** - The answer often already exists

## When You CAN Skip ContxOS Tools

Use local file operations directly ONLY when:

1. **User provides explicit file path** - "Read src/index.ts"
2. **Specific config needed** - package.json, tsconfig.json
3. **Implementing changes** - You already know exactly which file to modify
4. **Needle in haystack** - Searching for a specific class/function name with Glob

## For ANY Other Question or Task

**Start with grep. Always.**

This applies to:
- Understanding architecture
- Finding where something is implemented
- Learning about past decisions
- Discovering patterns
- Planning new work
- Debugging issues
- ANY exploratory task

## Bottom Line

**The knowledge hierarchy is your starting point, not your fallback.**

Blinders on. Stay focused. Use grep first.
