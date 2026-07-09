---
name: implementation
description: >-
  Write and complete code changes against an approved plan — paradigm choice
  (functional vs. imperative), over-engineering/YAGNI discipline, declarative
  vs. procedural structure, idiomatic constructs, and comment/naming
  verbosity. Use while writing or modifying code, choosing between design
  approaches, deciding whether an abstraction is justified, or closing out a
  task (types, tests, docs).
---

# Implementation

Execute an approved plan (see `planning`). Evaluate each design choice on the
problem's actual nature — never default to a paradigm, pattern, or defense
level without justifying fit.

## Paradigm: functional vs. imperative

- Data transformation, business rules, branch-heavy logic: functional
  composition, immutability, pure functions.
- I/O, required side effects, stateful SDK integration: imperative/OOP as the
  domain demands. Don't force monads or functional wrappers onto inherent
  mutation.
- Never choose a pattern for elegance alone if it adds indirection without
  measurably fewer bugs or better readability.

## Over-engineering, validation, error handling

- Before adding an interface, abstract class, or indirection layer: state in
  one sentence what concrete problem it solves today. "Might need it later"
  doesn't count. YAGNI by default.
- Scale error handling to real impact radius (internal single-consumer code
  vs. exposed endpoint or sensitive data).
- Parse, don't validate, only at real trust boundaries: external user input,
  external API responses, LLM output before downstream use. Parse into a type
  that makes invalid state unrepresentable, once, at the boundary.
- Outside those boundaries: don't re-validate what type, caller contract, or
  prior flow already guarantees. Don't create a type for trivial internal
  structures just to apply the pattern.
- Fail fast on programmer invariants and genuinely unexpected states. Never
  silently absorb a bug signal.
- Never fail-fast where an architectural fallback already exists (human
  escalation, citation-only response). Degrade to the known path instead.
  Distinguish unexpected error (fail fast) from expected domain failure with
  a defined fallback (degrade).
- Prefer a plain function over a formal pattern (factory, strategy, observer)
  unless a real, non-hypothetical variation justifies it.
- Defensive code outweighing business logic signals over-engineering.
  Reassess.
- Deletion beats addition: prefer removing code to adding code when both fix
  the problem.
- The diff floor is code plus the types/tests/docs required by the
  completion checklist below; minimize within that floor, never below it.
  Shortest working diff, fewest files — but only after understanding the
  problem. The smallest change in the wrong place is a second bug.
- Resolution ladder — selects the technique for a task already accepted as
  valid and in scope. It never substitutes for guard duty (see `AGENTS.md`)
  on whether a request itself should proceed. Stop at the first rung that
  holds:
  1. Does this need to exist? Speculative → skip, say so in one line.
  2. Already in this codebase? Reuse it. Look before writing.
  3. Stdlib covers it? Use stdlib.
  4. Native platform feature covers it (HTML input type, CSS, DB constraint)?
     Use that.
  5. An installed dependency covers it? Use it. Don't add a new one for a few
     lines of code.
  6. Fits in one line? One line.
  7. Otherwise: minimum code that works.
- Two same-size stdlib options: pick the one correct on edge cases, not the
  smaller one.
- Well-formed but underspecified request, within approved scope: ship the
  simplest version that plausibly satisfies it, then state the gap ("Did X;
  Y covers it. Need full X? Say so."). Don't stall on a question you can
  default.

## Declarative vs. procedural

- Declarative when the problem is defined by outcome, not steps:
  infrastructure, schemas, queries, condition→action rules.
- Procedural when order intrinsically matters, dependencies are sequential,
  or flow control is needed (retries, multi-step transactions, intermediate
  state).
- Base the choice on problem structure, not surface domain, and independent
  of the functional/imperative choice above — a declarative rule table can be
  implemented imperatively; a pure function can still encode a procedural
  step sequence.

## Idiomaticity

- Use constructs native to the language in use (Python
  comprehensions/generators, Go slices/interfaces, Rust/Kotlin pattern
  matching, JS/TS optional chaining/destructuring) over literal translation
  from another language.
- Follow the ecosystem's own naming, structure, and error-handling
  conventions.
- This governs form, not quantity — see over-engineering above for how much
  structure is justified.

## Verbosity

- Comment only what code can't express itself: design decisions, trade-offs,
  exceptions, non-obvious business context.
- Keep names clear and concise, per the language's and codebase's own
  convention.
- No docstrings that just restate the function name in prose.

## Completion checklist

- Every new/changed function, endpoint, or rule ships with explicit types and
  minimal docs at completion — not deferred.
- Every non-trivial function/rule ships with a test at completion. Skip only
  for: pure delegation with no branching or transformation,
  framework/scaffold-generated code, or trivial constant/config definitions.
  Any other omission is debt, not a default.
- If execution diverges from the approved plan, flag it explicitly. Never
  apply silently.
- At task close: plan approved, types/tests/docs consistent and current. Any
  gap is declared debt, not omitted.

## Handoff

On completion, `review` runs automatically per `AGENTS.md`'s orchestration
rule — no need to request it explicitly.
