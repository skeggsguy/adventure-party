# Parked review notes — session-zero skill

Suggestions raised while replacing `skills/session-zero/SKILL.md` with the
new draft. None of them were applied: the draft ships as written, and these
are here for you to accept, reject, or rewrite later.

**This file sits in the repo root, so it ships with any clone of the plugin.
Review it and delete it before the next release.**

- [ ] **The description over-triggers.** "Load session zero for … any
  answering questions from the user" pulls one-shot factual questions into
  the full ceremony. Suggested tie-break, one clause in the description: a
  pure fact with no decision behind it → don't load; an answer whose purpose
  is a decision → load.

- [ ] **"Don't assume the user will retain the same decision"** invites the
  Guide to re-open calls the user already settled. Suggested flip, same
  length: decisions stay made until the *user* re-opens one — and when they
  do, explore freely and mark the old entry superseded.

- [ ] **"Always explain new concepts (ELI5)" has no depth governor.** This
  repo's own experience says an ungoverned explain-everything mandate buries
  trivial questions and stops the user asking a second one. Suggested fix:
  tie explanation depth to the draft's own calibration paragraph, so ELI5
  scales with the size of the request like everything else does.

- [ ] **Superseded-not-deleted decision entries accumulate forever** in a
  file that is injected into every session. Give `/party:consolidate`
  explicit license to prune long-superseded tombstones (it currently prunes
  them, but the rule lives only in the consolidate skill — the two rules
  should agree out loud).

- [ ] **Two scaffolds worth re-adding from the old skill, compressed** — the
  draft's purpose paragraph promises this teaching, but the body no longer
  carries the moves that produce it:
  - state the strongest case AGAINST your own recommendation;
  - the YAGNI asymmetry in one line — duplicated code is a refactor, a wrong
    abstraction is a rewrite.

  Note this one cuts both ways: README's "Session Zero" section still
  advertises both moves as core to the skill. Either re-add them to the
  skill or trim the claim from README — right now the README promises what
  the skill no longer instructs.
