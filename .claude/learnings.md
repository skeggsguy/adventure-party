# Learnings (inbox)

Append-only dated entries (`## YYYY-MM-DD — title`), distilled into the
curated experience files and archived by `/party:long-rest`. Never injected;
read on demand.

## 2026-07-29 — Shipped instructions must not name a specific built-in tool

`hooks/instructions.md` tells the session to count the learnings inbox "with
the Grep tool in count mode". That instruction is not always executable: the
tool roster served to a session is decided per-install by server-side rollout
bucketing, not by the user's config, and Grep can simply be absent.

Confirmed on this machine (WSL, 2.1.220) vs the same account's Windows install
(also 2.1.220): Grep is absent from the default roster here but present there.
Ruled out — settings/permission denies (none on either side), version skew
(identical), effort level (absent at low/medium/high), and a broken search
backend (ripgrep is embedded in the binary, and `claude --tools Grep,Read`
loads Grep and runs it successfully). The two installs cache 442 GrowthBook
feature flags each and exactly two differ, `tengu_umber_kestrel` being ON for
Windows and OFF for WSL; bucketing hashes on machineID/userID, which differ
per install even for one account. Not causally confirmed — flipping the cached
flag was blocked by the permission classifier.

The rule this implies for anything we ship: name the *outcome*, not the tool.
"Count the entries without reading the file" survives a roster change; "use
the Grep tool" does not. Same class of failure as assuming `jq` exists.

The blast radius is narrower than it first looked, though: only main-session
*prose* is exposed. An agent's frontmatter `tools:` list is an explicit
naming, and explicit naming resurrects a tool the default roster pruned —
verified twice, by `claude --tools Grep,Read` on the CLI and by spawning
`party:wizard` (frontmatter `tools: Read, Grep, Glob`) in a session with no
Grep, where it reported all three and ran a Grep count successfully. So
wizard needs no defensive change, and its read-only guarantee stands. The
asymmetry to remember: a *declared* tool list is honoured; an *instruction*
to use a tool is only a wish.

## 2026-07-29 — A text budget only holds where the argument is out of context

`decisions.md` reached 12.4k against a shipped "~2 lines per entry" rule that
every one of its 23 entries broke. The rule was not ignored — it was applied
at the only moment it cannot work. At write time the author still holds the
full argument, and every clause of it feels load-bearing; compression is only
possible for someone who no longer has it.

This falsifies the 2026-07-27 decision, which diagnosed `decisions.md` as
"inflow with an outflow gated on stopped-being-true, which a decision never
does" and concluded the bound "has to be a budget at write time, not a test
at prune time." Right about the diagnosis, wrong about the remedy — and the
evidence was immediate: entries written the same day, in the file that
defines the rule, ran 15 and 30 lines.

The general shape: a constraint enforced by the party who is motivated to
break it is a wish. Move it to a moment with different incentives. Here that
is `/party:long-rest`, which now compacts as well as distils — and *measures*
the tier, since the ~4k budget had existed for weeks with nothing weighing
it.

Second-order: the fix is not deletion. Only 5 of 23 entries carried a
`see learnings` pointer, so compressing in place would have destroyed 18
arguments outright. Move-then-shorten, into the archive that already existed.
The drain we needed had already shipped for a different purpose.

## 2026-07-29 — Ask which baseline a helper diffed before believing its diff

A read-only verification agent reported, with specificity and confidence,
that ~9 archived entries were not verbatim and the original held 25 entries
rather than 23. Both false. It had diffed against `HEAD`, but the file was
already modified-uncommitted at session start — the entries it flagged as
"missing" were exactly the ones the previous Long Rest had pruned, which
`CHRONICLE.md` records.

The failure is invisible at the finding level: a wrong-baseline diff produces
findings shaped exactly like real ones, and "fixing" them would have
*reverted* correct work. When a helper's claim is a diff, the first question
is never "is this true" but "against what". A dirty working tree makes `HEAD`
the wrong answer by default, and this repo's `.claude/` files are edited by
sessions, so they are dirty more often than not.

Corollary that made the audit possible: a pre-edit baseline of an uncommitted
file is recoverable from the session transcript's `toolUseResult` entries in
`~/.claude/projects/<proj>/<session>.jsonl`, even when git holds no copy. For
lossy compaction steps that is the only reliable audit path — file-history
directories only cover other sessions.

## 2026-07-29 — Renumbering a ceremony breaks the prose the list sits inside

Inserting a step into `/party:long-rest`'s numbered ceremony was mechanically
clean — renumber 4/5/6 to 5/6/7, update two cross-references. What broke was
prose stated elsewhere in the file: "the archive move happens last" and
"every earlier step is idempotent by design" were both invariants the new
step violated, and a pronoun in the new branch had lost its antecedent.

In a repo where prose *is* the executable, a numbered list is not a data
structure — it is a set of promises made about itself in surrounding text.
After renumbering, re-read the whole file for the claims the list is embedded
in, not just the references that name a number. Grep finds `step 4`; it does
not find "happens last".

