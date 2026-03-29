---
name: code-review
description: >
  Reviews code changes for bugs, correctness, style violations, security issues,
  and best practices. Use when reviewing PRs, auditing a file, or checking code
  quality before merge. Do NOT use for explaining code concepts, writing new code
  from scratch, or general debugging sessions.
tags: [code, quality, security, devex]
version: 2.0.0
---

# Code Review Skill

Performs structured, actionable code reviews that prioritize correctness and
safety first, then maintainability, then style — in that order.

---

## Use this skill when
- User shares a diff, PR, or file and asks for a review
- User says "review my code", "check this PR", "audit this file"
- User asks "is this ready to merge?" or "any issues with this?"
- User pastes code and asks for feedback before shipping

## Do NOT use when
- User wants an explanation of how code works (use explanation mode)
- User wants new code written from scratch (use code generation)
- User is debugging a runtime error without asking for a full review
- The input is configuration/infra-as-code (needs a dedicated infra-review skill)

---

## Instructions

### 1. Orient yourself
Before reviewing, identify:
- **Language & runtime** — syntax rules, idioms, and common pitfalls vary
- **Context** — is this a library, service, CLI, or script? Affects severity of issues
- **Scope** — full file or a diff? Focus on changed lines for diffs

### 2. Review in priority order

Always surface issues in this order — highest severity first:

**🔴 P1 — Correctness & Safety** *(blocking)*
- Logic errors, off-by-one, wrong conditionals
- Unhandled errors, silent failures, missing null/bounds checks
- Security issues: injection, hardcoded secrets, unsafe deserialization, XSS

**🟠 P2 — Reliability & Edge Cases** *(blocking)*
- Missing error handling for expected failure modes
- Race conditions, uninitialized state, resource leaks
- Untested invariants that could fail in production

**🟡 P3 — Maintainability** *(non-blocking, suggest)*
- Functions doing more than one thing
- Poor naming that obscures intent
- Missing or misleading comments on complex logic
- Duplicated code that should be extracted

**🟢 P4 — Style & Conventions** *(non-blocking, optional)*
- Formatting inconsistencies
- Naming convention violations (camelCase vs snake_case, etc.)
- Unnecessary verbosity or overly clever one-liners

### 3. Write feedback per finding

For every issue found, produce a finding block (see Output Format).
Never give vague feedback. Always include:
- Where the problem is (file + line if possible)
- What the problem is
- Why it matters
- How to fix it (with a code snippet if helpful)

### 4. Write the summary

After all findings, produce a short summary block (see Output Format).

---

## Constraints

- **Never approve** code with any P1 finding outstanding
- **Never fabricate** issues — if the code is clean, say so clearly
- **Never nitpick style** without first addressing P1/P2 — don't bury blockers in noise
- **Always explain why**, not just what — "rename this" is not useful feedback
- **Do not rewrite** large sections of the author's code unprompted — suggest, don't replace

---

## Examples

### Example 1 — Security issue (P1)
**Input:**
```python
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return db.execute(query)
```
**Expected finding:**
```
🔴 P1 — SQL Injection [line 2]
Problem: user_id is interpolated directly into the query string.
Why: An attacker can pass `1 OR 1=1` to exfiltrate all users.
Fix: Use parameterized queries:
  db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

---

### Example 2 — Missing error handling (P2)
**Input:**
```javascript
const data = JSON.parse(rawInput);
processData(data);
```
**Expected finding:**
```
🟠 P2 — Unhandled Parse Error [line 1]
Problem: JSON.parse throws SyntaxError on malformed input, crashing the process.
Why: rawInput from external sources is never guaranteed to be valid JSON.
Fix: Wrap in try/catch or use a safe parse utility:
  let data;
  try { data = JSON.parse(rawInput); }
  catch (e) { return handleError(e); }
```

---

### Example 3 — Clean code
**Input:** A well-written, idiomatic function with proper error handling
**Expected action:** State clearly "No issues found. Code is correct and idiomatic."
Do NOT invent P4 nitpicks to appear thorough.

---

## Output Format

Structure every review exactly like this:
```
## Code Review — <filename or PR title>

### Findings

<for each issue:>
<severity emoji> <Priority> — <short title> [<location>]
Problem: <what is wrong>
Why: <why it matters>
Fix: <how to address it, with snippet if helpful>

---

### Summary
- 🔴 Blockers: <count> — <one-line description or "None">
- 🟠 Reliability: <count> — <one-line description or "None">
- 🟡 Suggestions: <count>
- 🟢 Style: <count>

Verdict: ✅ Approve / 🔁 Approve with suggestions / ❌ Request changes

<one sentence rationale for the verdict>
```

---

## Safety

- Never share or log secrets/credentials found in code — flag their existence only
- If you find evidence of a critical active vulnerability (e.g. a live API key), flag it as P1 and recommend immediate rotation before any other feedback