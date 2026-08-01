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

## 2026-07-30 — Large hook output is relocated to disk, not injected

Observed directly at this session's start: the SessionStart hook's second
`cat` (`architecture.md gotchas.md decisions.md`, 16,912 B) did not reach
context. It was replaced by `Output too large (16.3KB). Full output saved
to: …/tool-results/hook-<uuid>-stdout.txt` plus the first ~2,048 B inline —
so the session had four bullets of `architecture.md` and none of
`gotchas.md` or `decisions.md`. The first `cat` (`instructions.md`,
4,048 B) arrived verbatim, tail byte-identical to the file.

The mechanism is not hook-specific: the spill path is the generic
`tool-results/` directory, so hook stdout inherits the ordinary per-result
inline cap. The cap is **per result, not per session** — which means the
two-`cat` split chosen on 2026-07-29 for unrelated reasons is load-bearing.
One combined `cat` would put the 21 KB total over the cap and take
`instructions.md` — the party protocol itself — to disk with it, silently
disabling the plugin. Any future consolidation of those `cat`s reintroduces
that failure.

`gotchas.md` recorded the opposite on 2026-07-29: "injected verbatim … not
truncated at ~22k chars (tested)". Growth is not the explanation — the tier
was *larger* that day (25,576 B) than now (16,913 B). The test was aimed at
a hypothesised ~22k clipping ceiling, and the real behaviour is an
order of magnitude lower and works by relocation, so it was outside the
hypothesis space.

Two generalisations, both about the shape of the miss rather than the
number:

Relocation defeats every cheap check, because nothing fails. The hook exits
0, the text is retrievable on disk, and the content still exists — so
"did the hook fire?", "is the file there?" and the `lantern is lit` sentinel
all pass. Only absence *in the model's context* distinguishes the two
states, and no gate in this repo tested for that. Worse, every existing
gate probes `instructions.md`, the one file small enough to fit; the file
that doesn't fit had no gate at all. When a limit degrades by moving data
rather than erroring, the assertion has to name the consumer ("the model
can quote line N"), never the producer.

A budget expressed as one number hid two different limits. `~4k` was a
voluntary cost budget on shipped text with no enforcement behind it, while
the per-project tier — assumed unbounded — is the side with the real
ceiling. `architecture.md` had already blurred the two by attaching the 4k
to "that tier", and `/party:long-rest`'s 50k gauge calls a size "fine" that
is several times past the point where the files stop being injected. A
gauge inherits authority from being a number; it earns none of it unless
its thresholds were measured against the mechanism they claim to bound.

## 2026-07-30 — A read trigger is a capability floor, not a prose problem

Replacing hook injection with per-file read triggers made delivery
conditional on compliance for the first time — injection had no compliance
step at all. Measured on the fixture built for the change: the `gotchas.md`
trigger fired 3/3 on the default model and **0/4 on haiku**.

The useful part is the diagnosis. Asked with tools disallowed which file it
must read before its first change, haiku names `.claude/gotchas.md`
correctly, then edits without reading it. So "the rule didn't fire" splits
three ways — *didn't arrive*, *disputed the rule*, *disputed the case* — and
only the middle one is a wording problem. This was the third. Both documented
remedies were applied and both were null: strengthening the trigger to an
explicit precondition ("one-character changes included … 'too small to need
it' is the case it exists for"), and hoisting the whole section above the
muster protocol. That is this repo's own "every more-text fix feeds the step
that was already working", observed live rather than reasoned about.

Establish which of the three failures you have before writing a single word
of remedy, because two of the three cannot be written around. Shipped anyway:
the alternative was silent non-delivery for *every* model, and the default
party is opus/fable. But the trade is now explicit — the injected design had
a truncation cliff, the referenced design has a compliance floor, and the
floor is the one that varies per session without announcing itself.

## 2026-07-30 — A behavioral fixture can leak its own answer

The first attempt at the trigger test asked the model to edit a
`config.txt` whose *other* lines already carried the `-ZORB` suffix the
hidden rule in `gotchas.md` demanded. A pass proved nothing: the suffix was
inferable from the file being edited, so pattern-matching and rule-following
were indistinguishable. Discarded and rebuilt with a side-effect reachable
only through the file under test.

Same failure class as this repo's `lantern` sentinel, which passed for days
while the experience tier silently wasn't loading — it only ever exercised
the one file small enough to fit. A test of whether something was *consulted*
must make its expected evidence unobtainable by any other route, and the way
to check that is to ask what a model that never opened the file could still
produce.


## 2026-07-31 — A release marker with no distribution role has no feedback loop

0.7.0 and 0.8.0 both shipped untagged. Tags stop at v0.6.4 while
`plugin.json` had been bumped twice in plain commits, and the drift was
visible in the subject lines: 0.6.x read "Release X.Y.Z", 0.7.0/0.8.0 just
"X.Y.Z" — the word and the tagging step fell off together.

Nothing broke, and that is the point. `marketplace.json` sets
`"source": "./"` with no version pin, so `/plugin install` clones `main`
and keys its cache off `plugin.json`'s `version` field. Tags are not on the
distribution path at all: merging to `main` *is* the release, and the tag is
a pure marker. A step whose omission produces no symptom will be omitted,
and no amount of intending to remember it changes that — the only
reliable fix is to attach it to something that does fail loudly, or to
check it at the one moment someone is already looking (the version bump).

Caught only because the user asked "did we do a release" — an audit
question, not a build one. Worth asking directly at each bump instead:
`git tag -l` against `plugin.json`'s version is a two-second check.

## 2026-08-01 — A skill can flip a switch but cannot be one

Session-zero argument for the foreign-CLI ("hireling") design, recorded
before any build. The user's ask — swap a party member for another vendor's
coding CLI (codex, kimi, …) via a skill — hides a timing constraint:
`/party:long-rest`-style skills work because the user invokes them at the
moment the work happens, but the muster happens in a later turn or session,
when the skill body is inert. So the skill can only *write state*
(`party.json`), and something in context at muster time — the muster
sentence, or an agent body — must read it. The skill is a setup wizard whose
real job is the precondition check: verify the binary, probe its
non-interactive/write flags, smoke-test end-to-end at hire time, so failure
surfaces before a quest, not mid-build.

Second shape: wrapping any foreign CLI in any role is one job (read
experience files → build prompt → run binary in background past the 10-min
Bash cap → translate output into that role's handoff contract), so it is one
generic adapter agent parameterized by role at spawn — not an agent per tool
or per role. The role contracts are the party's interfaces; if the hireling
honors them, cleric never knows the hands changed. Per-CLI flag knowledge is
probed at hire time and stored in config, never shipped — a shipped flag
table is xp.sh in prose. Disclosure, not judgment: hiring wizard converts a
structural read-only guarantee (tool grant) into a sandbox flag, said once
at hire time.

## 2026-08-01 — A shipped prohibition gets lawyered at its adjective

Cleric's live find while running the hireling build's behavioral check: with
fighter hired to a broken command, the muster→hireling wire worked (hireling
spawned, refused, reported exit 127), but the Guide then spawned the native
fighter and built anyway — overriding the user's standing config. The first
fix, "never a *silent* fallback", failed the second headless run in the most
instructive way possible: the Guide fell back *loudly*. The prohibition was
obeyed at its adjective and violated at its verb. The wording that went
green bans the act and names whose call it is: "A hire whose command fails
ends the quest — report it and stop; falling back to the native member is
the user's call to make, never yours." Rule for shipped prose: a behavioral
ban must land on the act itself and assign the decision to a person; any
qualifier ("silent", "unnecessary", "routine") becomes the loophole.

## 2026-08-01 — disable-model-invocation skills are headlessly testable

They never appear in the model's skill list (known, correct), which had left
"absent from the list" as their only smoke signal. Fighter found the real
check: `claude --plugin-dir . -p '/party:hire'` invokes the skill and runs
its actual body headlessly — used this release to verify hire's status path
end to end, and it generalizes to long-rest. The list-absence gotcha and the
test technique are two halves: you can't ask *about* the skill, but you can
still *run* it.
