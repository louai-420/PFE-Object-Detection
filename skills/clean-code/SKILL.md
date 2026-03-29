---
name: clean-code
description: >
  Applies and enforces clean code principles when writing, reviewing, or
  refactoring code. Covers Uncle Bob's Clean Code, SOLID, DRY, KISS, YAGNI,
  functional programming principles, and modern 2025 best practices across
  all languages. Use when writing new code, reviewing PRs, refactoring legacy
  code, or auditing code quality. Do NOT use for architecture decisions without
  code, DevOps/infra tasks, or explaining algorithms without code output.
tags: [code-quality, refactoring, solid, clean-code, review, best-practices]
version: 2.0.0
---

# Clean Code Skill

> "Any fool can write code that a computer can understand.
> Good programmers write code that humans can understand." — Martin Fowler

This skill transforms code that *works* into code that is *clean, maintainable,
and professional*. It combines Uncle Bob's foundational principles with modern
2025 practices across all paradigms and languages — with the judgment to know
when to apply each rule and when a trade-off is justified.

**Core philosophy:** These principles are *tensions to manage*, not rigid rules.
Context always determines whether a principle should be applied or bent.

---

## Use this skill when
- Writing new code and wanting to ensure quality from the start
- Reviewing a PR or diff for code quality feedback
- Refactoring legacy or messy code
- Asked to "clean up", "improve", or "make this more readable"
- Evaluating if code follows professional standards
- Identifying code smells or anti-patterns

## Do NOT use when
- The task is pure architecture/system design with no code output
- User wants performance optimization only (use a perf-specific skill)
- User is asking about algorithms conceptually without wanting code written
- The task is DevOps, CI/CD, or infrastructure — no application code involved

---

## The Principles Hierarchy

Apply principles in this order of priority. Never sacrifice higher-tier rules
for lower-tier ones.

```
Tier 1 — CORRECTNESS:   Code must be correct before it is clean
Tier 2 — READABILITY:   Code is read 10x more than it is written
Tier 3 — SIMPLICITY:    The simplest solution is almost always best
Tier 4 — MAINTAINABILITY: Change should be easy and safe
Tier 5 — ELEGANCE:      Good code has a kind of beauty — optional, never at cost of above
```

---

## 1. Meaningful Names

The most impactful change you can make to any codebase.

### Rules
- **Intention-revealing**: Name should answer *what*, *why*, and *how*
- **Pronounceable**: If you can't say it out loud, rename it
- **Searchable**: Single-letter names are findable nowhere; use them only as loop counters
- **No disinformation**: `accountList` for a `Map` is actively harmful
- **Distinguish meaningfully**: `ProductData` vs `ProductInfo` — what is the actual difference?
- **Classes = nouns**: `Customer`, `Invoice`, `Parser`. Avoid `Manager`, `Handler`, `Data`
- **Methods = verbs**: `postPayment()`, `validateEmail()`, `parseDate()`
- **Booleans = questions**: `isValid`, `hasPermission`, `canRetry`

```python
# ❌ BAD
def calc(d, r):
    return d * (1 - r)

# ✅ GOOD
def calculate_discounted_price(original_price: float, discount_rate: float) -> float:
    return original_price * (1 - discount_rate)
```

```typescript
// ❌ BAD
const d = new Date();
const ymdstr = d.toISOString().split('T')[0];

// ✅ GOOD
const currentDate = new Date();
const formattedDate = currentDate.toISOString().split('T')[0];
```

---

## 2. Functions

### Core Rules
- **Do ONE thing**: A function that does two things should be two functions
- **One level of abstraction**: Don't mix business logic with low-level string parsing
- **Ideal argument count: 0–2**. Three requires justification. Four+ → use an object
- **No side effects**: A function named `isValidUser()` must not also save to the database
- **Command-Query Separation**: A function either *does* something OR *answers* something — never both
- **Stepdown rule**: Functions should read top-to-bottom like a newspaper — high-level then detail

```python
# ❌ BAD — does multiple things, mixed abstraction, side effects
def process(u, db):
    if u['email'] and '@' in u['email']:
        u['active'] = True
        db.execute(f"UPDATE users SET active=1 WHERE email='{u['email']}'")
        send_email(u['email'], "Welcome!")

# ✅ GOOD — single responsibility, no hidden side effects
def is_valid_email(email: str) -> bool:
    return bool(email) and '@' in email

def activate_user(user: User) -> User:
    return User(**{**user.__dict__, 'active': True})

def save_user(user: User, repository: UserRepository) -> None:
    repository.update(user)

def send_welcome_email(email: str, mailer: Mailer) -> None:
    mailer.send(to=email, template="welcome")
```

### The Locality of Behavior (Modern Balance)
> In 2025, frameworks like React, Svelte, and Tailwind encourage **colocating**
> related logic. Splitting everything into micro-functions across many files
> can hurt readability more than it helps. Ask: does splitting this actually
> help the next developer, or just satisfy a rule?

```tsx
// Sometimes colocated is cleaner — modern React example
// This is ONE component doing ONE thing — no need to split further
function UserCard({ user }: { user: User }) {
  const [isFollowing, setIsFollowing] = useState(false);

  const handleFollow = async () => {
    await followUser(user.id);
    setIsFollowing(true);
  };

  return (
    <div className="card">
      <h2>{user.name}</h2>
      <button onClick={handleFollow}>
        {isFollowing ? 'Following' : 'Follow'}
      </button>
    </div>
  );
}
```

---

## 3. SOLID Principles

The five principles of object-oriented design. Apply to class/module design.

### S — Single Responsibility Principle (SRP)
> A class should have only one reason to change.

```python
# ❌ BAD — User class does persistence AND formatting AND email
class User:
    def save_to_db(self): ...
    def format_as_json(self): ...
    def send_welcome_email(self): ...

# ✅ GOOD — each class has one responsibility
class User: ...                   # data only
class UserRepository: ...         # persistence
class UserSerializer: ...         # formatting
class UserNotificationService: .. # email
```

### O — Open/Closed Principle (OCP)
> Open for extension, closed for modification.

```python
# ❌ BAD — adding a channel requires editing this function
def notify(user, channel):
    if channel == 'email': send_email(user)
    elif channel == 'sms': send_sms(user)

# ✅ GOOD — new channels added without touching existing code
class Notifier(ABC):
    @abstractmethod
    def send(self, user: User) -> None: ...

class EmailNotifier(Notifier):
    def send(self, user: User) -> None: send_email(user)

class SMSNotifier(Notifier):
    def send(self, user: User) -> None: send_sms(user)

def notify_all(notifiers: list[Notifier], user: User) -> None:
    for notifier in notifiers:
        notifier.send(user)
```

### L — Liskov Substitution Principle (LSP)
> Subclasses must be substitutable for their base class without breaking behavior.

```python
# ❌ BAD — Square breaks Rectangle's contract
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h

class Square(Rectangle):
    def set_width(self, w): self.width = self.height = w  # Breaks LSP!

# ✅ GOOD — separate types when behavior differs
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Rectangle(Shape): ...
class Square(Shape): ...   # Own implementation, no forced inheritance
```

### I — Interface Segregation Principle (ISP)
> No code should depend on methods it doesn't use.

```typescript
// ❌ BAD — SimplePrinter forced to implement fax()
interface Machine {
  print(doc: Document): void;
  scan(): Document;
  fax(number: string): void;
}

// ✅ GOOD — small, focused interfaces
interface Printable { print(doc: Document): void; }
interface Scannable { scan(): Document; }
interface Faxable   { fax(number: string): void; }

class SimplePrinter implements Printable {
  print(doc: Document) { /* ... */ }
}
```

### D — Dependency Inversion Principle (DIP)
> Depend on abstractions, not concretions.

```python
# ❌ BAD — high-level module depends on low-level MySQL implementation
class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()  # Tightly coupled

# ✅ GOOD — depends on abstraction; any DB works
class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository  # Inject dependency
```

---

## 4. DRY — Don't Repeat Yourself

> "Every piece of knowledge must have a single, unambiguous representation
> in a system." — Hunt & Thomas, *The Pragmatic Programmer*

DRY is about **knowledge duplication**, not just code duplication. If two pieces
of code change for different reasons, duplication is acceptable. If they change
together, they should be one.

```python
# ❌ BAD — validation logic duplicated in two places
def create_user(email, password):
    if not email or '@' not in email:
        raise ValueError("Invalid email")
    ...

def update_user(email, password):
    if not email or '@' not in email:  # Same logic repeated
        raise ValueError("Invalid email")
    ...

# ✅ GOOD — single source of truth
def validate_email(email: str) -> None:
    if not email or '@' not in email:
        raise ValueError("Invalid email")

def create_user(email, password):
    validate_email(email)
    ...

def update_user(email, password):
    validate_email(email)
    ...
```

> ⚠️ **DRY trap**: Premature abstraction is worse than duplication.
> Wait until a pattern appears **3 times** before extracting it (Rule of Three).

---

## 5. KISS — Keep It Simple, Stupid

> The best solution is almost always the simplest one that fully works.

```python
# ❌ BAD — over-engineered for no benefit
class UserStatusStrategyFactory:
    def create_strategy(self, user_type: str) -> StatusStrategy:
        registry = {
            'admin': AdminStatusStrategy(),
            'user': UserStatusStrategy(),
        }
        return registry.get(user_type, DefaultStatusStrategy())

# ✅ GOOD — a dict is sufficient
USER_STATUS_MAP = {
    'admin': 'Administrator',
    'user': 'Standard User',
}

def get_user_status(user_type: str) -> str:
    return USER_STATUS_MAP.get(user_type, 'Unknown')
```

Ask before adding complexity: *"Does this abstraction solve a real problem
I have today, or one I imagine I might have?"*

---

## 6. YAGNI — You Ain't Gonna Need It

> Implement features when they become necessary — not when you think they will be.

```python
# ❌ BAD — built for a multi-currency future that may never arrive
class PriceCalculator:
    def calculate(self, price, currency='USD', exchange_rate=None,
                  rounding_strategy=None, tax_jurisdiction=None):
        # 80% of this is never used
        ...

# ✅ GOOD — solve today's problem
def calculate_price(price: float, tax_rate: float) -> float:
    return price * (1 + tax_rate)
```

> YAGNI doesn't mean poor architecture. It means **grounding change in
> evidence, not guesses.** Modularity and good abstractions are still required
> — just don't write the future code yet.

---

## 7. Comments

**The rule**: Code should be self-explanatory. Comments exist to explain the
*why*, never the *what*. If you need a comment to explain what code does,
rewrite the code.

```python
# ❌ BAD — comment restates the code
# Increment i by 1
i += 1

# ❌ BAD — comment exists because the code is unclear
# Check if employee is eligible for benefits
if e.flags & 0x01 and e.age > 65:

# ✅ GOOD — code is self-documenting
if employee.is_eligible_for_full_benefits():

# ✅ GOOD — comment explains WHY, which the code cannot
# Using milliseconds here because the legacy API rejects ISO 8601.
# See: https://github.com/org/repo/issues/1234
timestamp = int(datetime.now().timestamp() * 1000)
```

**Good comments:**
- Legal / license headers
- Explanation of *why* a non-obvious decision was made
- Reference to external constraint (API quirk, hardware limitation)
- TODO with owner and ticket: `# TODO(alice): Replace with streaming once #4521 is done`
- Warning of consequence: `# IMPORTANT: Do not cache — response changes per request`

**Bad comments:** Redundant, misleading, outdated, position markers (`// === HELPERS ===`),
commented-out code (use git blame instead).

---

## 8. Functional Programming Principles

Modern clean code draws heavily from FP — apply even in OOP languages.

### Pure Functions
```python
# ❌ BAD — depends on and mutates external state
total = 0
def add_to_total(amount):
    global total
    total += amount   # Side effect

# ✅ GOOD — pure: same input always produces same output, no side effects
def calculate_total(amounts: list[float]) -> float:
    return sum(amounts)
```

### Immutability
```typescript
// ❌ BAD — mutating state directly
const user = { name: 'Alice', role: 'user' };
user.role = 'admin';  // Mutation — hard to trace

// ✅ GOOD — create new object
const updatedUser = { ...user, role: 'admin' };
```

### Avoid Null — Use Optional/Result Types
```typescript
// ❌ BAD — null forces every caller to check
function findUser(id: string): User | null { ... }

// ✅ GOOD — explicit about absence
function findUser(id: string): Option<User> { ... }
// or in TypeScript:
function findUser(id: string): User | undefined { ... }
// and handle at call site:
const user = findUser(id) ?? createGuestUser();
```

---

## 9. Error Handling

```python
# ❌ BAD — return codes require caller discipline; easy to ignore
def parse_config(path: str) -> dict | None:
    if not os.path.exists(path):
        return None
    ...

# ✅ GOOD — exceptions can't be silently ignored
def parse_config(path: str) -> dict:
    if not os.path.exists(path):
        raise ConfigNotFoundError(f"Config file not found: {path}")
    ...

# ✅ GOOD — wrap in try-catch at the boundary
try:
    config = parse_config('./config.yaml')
except ConfigNotFoundError as e:
    logger.error("Startup failed: %s", e)
    sys.exit(1)
```

**Rules:**
- Use exceptions, not return codes
- Never return `None` for expected failures — throw a typed exception
- Never pass `None` as an argument — use Optional parameters with defaults
- Write `try/catch/finally` first when working with I/O or external systems
- Provide context: what failed, why, and how to fix it
- Log at boundaries, not inside every function

---

## 10. Unit Tests & TDD

**F.I.R.S.T Principles:**
- **Fast** — tests must run in milliseconds, not seconds
- **Independent** — no test depends on another test's state
- **Repeatable** — same result every run, in any environment
- **Self-Validating** — pass or fail, never "check the output manually"
- **Timely** — written just before production code (TDD) or immediately after

**AAA Pattern — Arrange, Act, Assert:**
```python
def test_calculate_discounted_price():
    # Arrange
    original_price = 100.0
    discount_rate = 0.20

    # Act
    result = calculate_discounted_price(original_price, discount_rate)

    # Assert
    assert result == 80.0
```

**The TDD cycle:**
```
1. RED   → Write a failing test that defines the desired behavior
2. GREEN → Write the minimum code to make it pass
3. REFACTOR → Clean the code — both test and implementation
```

**AI-era TDD warning:** AI-generated tests validate code *as it exists*, not
*as it should behave*. Always write tests before asking AI to implement. Tests
define the contract; AI fills it.

---

## 11. The Boy Scout Rule

> "Leave the campground cleaner than you found it."

Every time you touch a file, make at least one small improvement:
- Rename an unclear variable
- Extract a function from a complex conditional
- Delete a stale comment
- Add a missing type annotation

This prevents gradual code rot without requiring big refactor sprints.

---

## 12. Code Smells Reference

| Smell | Description | Fix |
|-------|-------------|-----|
| **Long Method** | Function > 20 lines | Extract smaller functions |
| **God Class** | Class with 20+ methods | Apply SRP, split responsibilities |
| **Feature Envy** | Method uses other class's data more than its own | Move method closer to the data |
| **Data Clumps** | Same 3+ parameters always travel together | Introduce a data class or object |
| **Primitive Obsession** | Using `str`/`int` for domain concepts | Wrap in a value object |
| **Switch Statements** | Large conditionals on type | Replace with polymorphism |
| **Parallel Hierarchies** | Two class trees that must change in sync | Merge hierarchies |
| **Lazy Class** | Class that does almost nothing | Collapse or inline |
| **Speculative Generality** | Unused abstraction "just in case" | YAGNI — delete it |
| **Temporary Field** | Instance variable only set in some cases | Extract Class or use null object |
| **Message Chains** | `a.getB().getC().doThing()` | Apply Law of Demeter |
| **Middle Man** | Class that only delegates | Remove and call directly |
| **Magic Numbers** | `if status == 3:` | Extract named constants |
| **Dead Code** | Code that is never executed | Delete it — git tracks history |
| **Duplicated Code** | Same logic in multiple places | Apply DRY |

---

## Anti-Patterns

### ❌ Over-Application of Clean Code
Splitting a 10-line function into 5 functions across 3 files because "functions
should be small" is worse than leaving it. Apply judgment: does this split
*actually* help the next reader, or just satisfy a rule?

### ❌ Premature Abstraction
Introducing an interface, factory, or strategy pattern before there are at
least two different implementations is speculative complexity. Wait for the
second implementation before abstracting.

### ❌ Comment-Driven Development
Comments that explain *what* the code does are a code smell.
The code should explain itself. Rewrite, don't comment.

### ❌ Cargo-Cult Patterns
Using a design pattern because you read about it, not because it solves your
actual problem. Singletons, Factories, and Observers used everywhere "because
best practice" are anti-patterns in disguise.

### ❌ TDD After the Fact (with AI)
Asking AI to generate tests for existing code produces tests that confirm
behavior, not tests that verify requirements. This gives false confidence.

---

## Constraints

- **Never approve code with God Classes or Long Methods** without flagging P1
- **Never add a comment that explains what the code does** — rewrite the code
- **Never return `null` / `None`** from a function that should throw on failure
- **Never apply a principle rigidly** when the trade-off makes the code worse — explain the judgment
- **Always apply the Boy Scout Rule** — leave every file touched slightly better
- **Always write tests** for non-trivial logic before considering it done

---

## Examples

### Example 1 — Naming + Function refactor (Python)
**Input:**
```python
def proc(lst, x):
    r = []
    for i in lst:
        if i > x:
            r.append(i)
    return r
```
**Expected output:**
```python
def filter_values_above_threshold(values: list[float], threshold: float) -> list[float]:
    return [value for value in values if value > threshold]
```
**What changed:** Names are intention-revealing, list comprehension is idiomatic Python,
type hints document the contract.

---

### Example 2 — Applying SRP (TypeScript)
**Input:** A single `UserService` class that handles authentication, DB persistence,
email notifications, and JSON serialization.

**Expected output:** Four focused classes — `AuthService`, `UserRepository`,
`UserNotificationService`, `UserSerializer` — each with a single reason to change.

---

### Example 3 — YAGNI violation
**Input:** Developer asks to add a plugin system, multi-tenancy support, and
internationalization to an MVP with 3 users.

**Expected response:** Flag as YAGNI violation. Recommend implementing only
what the 3 current users demonstrably need. Document the architectural decision
as a TODO for when the need becomes real.

---

### Example 4 — Clean Code + AI (Modern Context)
**Input:** "Generate tests for this function."

**Expected response:** Ask first — "Do you have requirements or expected
behaviors to test, or should I infer them from the implementation?" Then write
tests that verify *intended behavior*, not just current behavior. Flag any
discovered edge cases the implementation doesn't handle.

---

## Output Format

For every clean code review or refactor, structure output as:

```
## Clean Code Review — <filename / function>

### 🔴 P1 — Critical (readability/correctness blockers)
<issue> → <fix with code snippet>

### 🟠 P2 — Smells (patterns that will cause pain)
<issue> → <recommendation>

### 🟡 P3 — Style (minor improvements)
<issue> → <suggestion>

---

### Refactored Code
[Complete clean version]

---

### What Changed
- [Principle applied] → [specific change made]
- [Principle applied] → [specific change made]

### Boy Scout Rule Applied
[One small improvement made to surrounding context, if applicable]
```

---

## Pre-Delivery Checklist

### 🔴 P1 — Must fix before merge
- [ ] No God Classes (>10 methods or >300 lines)
- [ ] No functions doing more than one thing
- [ ] No magic numbers — all literals named
- [ ] No `null` / `None` returned where exception should be thrown
- [ ] No side effects in query functions
- [ ] No duplicated logic (DRY violations)

### 🟠 P2 — Fix before merge if time allows
- [ ] All names are intention-revealing and searchable
- [ ] No comment explains *what* the code does (only *why*)
- [ ] Function arguments ≤ 3 (or object introduced)
- [ ] Tests exist and follow AAA + F.I.R.S.T
- [ ] SOLID principles not violated

### 🟡 P3 — Track as tech debt
- [ ] Boy Scout Rule applied to touched files
- [ ] No speculative abstractions (YAGNI)
- [ ] No unnecessary complexity (KISS)
- [ ] Functional patterns used where appropriate (immutability, pure functions)

---

## Trigger Test

| Prompt | Activates? | Why |
|--------|-----------|-----|
| "Review this Python class for code quality" | ✅ Yes | Explicit code review request |
| "Refactor this legacy service" | ✅ Yes | Refactor = clean code task |
| "Is this code following best practices?" | ✅ Yes | Best practices audit |
| "How does quicksort work?" | ❌ No | Algorithm explanation, no code output |
| "Set up my Docker deployment pipeline" | ❌ No | DevOps — no application code |