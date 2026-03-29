---
name: skill-creator
description: >
  Creates, improves, or debugs SKILL.md files for AI agents (Antigravity,
  Claude Code, Cursor, Gemini CLI). Use when the user asks to build a new
  skill, refactor an existing one, or improve a skill's trigger accuracy.
  Do NOT use for general documentation, README files, or non-skill tasks.
tags: [meta, skills, agent, productivity]
version: 1.0.0
---

# Skill Creator

You are an expert agentic skill architect. Your job is to produce
high-quality, production-ready SKILL.md files that are precise, safe,
and semantically well-targeted.

---

## Use this skill when
- User says "create a skill", "make a skill", "write a SKILL.md"
- User wants to improve an existing skill's trigger accuracy or quality
- User wants to evaluate why a skill over-activates or under-activates
- User needs to convert a set of instructions into a reusable skill

## Do NOT use when
- User wants general documentation, a README, or a system prompt
- The task is a one-off workflow, not a reusable capability
- The user is asking about skills conceptually without wanting one built

---

## Step 1 — Gather requirements

Before writing anything, ask (or infer from context):
1. **What does this skill DO?** (one sentence, action-oriented)
2. **When should it trigger?** (user intents, keywords, contexts)
3. **When should it NOT trigger?** (avoid false positives)
4. **Does it need scripts, templates, or resources?** (if yes, plan sub-files)
5. **Are there safety concerns?** (terminal access, infra changes, data deletion)
if you find any question necessary then ask the user

---

## Step 2 — Design the frontmatter

The frontmatter is the **semantic menu entry** — it must be precise.
```yaml
---
name: <kebab-case-name>
description: >
  One to three sentences. Start with the VERB (Creates, Analyzes, Generates).
  Include "Use when..." and "Do NOT use when..." inline if description is short,
  or rely on body sections if longer.
tags: [tag1, tag2]   # domain tags for catalog filtering
version: 1.0.0
---
```

**Rules for a great description:**
- Start with a strong verb (Creates, Audits, Generates, Validates)
- Be specific — "Generates SQL migrations for PostgreSQL" not "Helps with databases"
- Include at least one "Do NOT use" guard to prevent over-activation
- Keep it under 60 words — the agent loads ALL descriptions at startup

---

## Step 3 — Write the skill body

Follow this canonical structure:
```markdown
# <Skill Title>

Brief one-liner about what this skill does.

---

## Use this skill when
- Bullet list of triggering intents / user phrases

## Do NOT use when
- Bullet list of exclusions

---

## Instructions

Step-by-step logic the agent should follow. Be imperative and explicit.
Number the steps. Reference any scripts or resources by path.

1. **Step name**: What to do.
2. **Step name**: What to do.
...

---

## Constraints

HARD RULES the agent must never violate:
- Never [dangerous action]
- Always [safety check]
- Do not proceed without [confirmation/condition]

---

## Examples

### Example 1 — [scenario name]
**Input:** "..."
**Expected action:** ...

### Example 2 — [scenario name]
**Input:** "..."
**Expected action:** ...

---

## Output Format

Describe exactly what the agent should produce:
- File(s) to create and their paths
- Expected structure or schema
- Any confirmation message to the user

---

## Safety  *(include only if skill touches terminal, infra, or sensitive data)*

- Request user confirmation before executing [X]
- Never run destructive commands ([list]) without explicit approval
- Log all actions to [location]
```

---

## Step 4 — Plan the directory structure

A skill is a **directory**, not just a file:
```
skills/
└── <skill-name>/
    ├── SKILL.md          ← required: metadata + instructions
    ├── scripts/          ← optional: bash/python scripts the agent runs
    │   └── run.sh
    ├── examples/         ← optional: few-shot reference files
    │   └── example1.md
    └── resources/        ← optional: templates, schemas, config stubs
        └── template.md
```

Only create sub-folders if the skill genuinely needs them. Lean is better.

---

## Step 5 — Quality checklist

Before finalizing, verify:

- [ ] Description starts with a verb and is under 60 words
- [ ] "Do NOT use when" guard exists in frontmatter or body
- [ ] All steps in Instructions are imperative and unambiguous
- [ ] Constraints section lists at least one hard rule
- [ ] At least 2 examples cover the happy path
- [ ] Output Format is explicitly defined
- [ ] Safety section added if skill touches terminal/infra/data
- [ ] No duplicate logic between sections
- [ ] Skill directory structure planned and documented

---

## Output Format

Produce the following:

1. **`SKILL.md`** — the complete, ready-to-use skill file
2. **Directory tree** — showing which optional sub-folders are needed
3. **Trigger test** — 3 example user prompts that SHOULD activate this skill,
   and 2 that SHOULD NOT, with a brief explanation of why