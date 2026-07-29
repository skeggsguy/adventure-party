# Chronicle

The party's saga, one entry per level. Plain language — what was built,
what was conquered, what was learned.

## Level 2 — Lanterns of the Gilded Ledger — 2026-07-26

The level the party stopped being a costume.

**What was built.** Adventure Party went from a themed wrapper to a real
framework. The three members took their final shape — fighter who
builds, cleric who reviews and fixes, wizard who advises and never
writes — and learned to call their own read-only helpers, capped so the
nesting can't run away. Around them grew the things that make a party
more than a roster: Session Zero, the conversation where a quest gets
shaped before any code is written; the experience system, where the
project's own memory is the party's XP and the statusline shows it; and
the Long Rest that turns a level-up into actual training rather than a
badge. This entry is the first one it has ever written.

**What was conquered.** The largest trap was one the party had been
carrying since its second version and had even written into the README
as advice: the belief that a project's own agent file quietly overrides
the plugin's. A live test with a decoy agent proved the opposite — the
two simply coexist, and a namespaced summon always reaches the plugin.
An entire mechanism had been designed on that assumption and was deleted
before it ever shipped. A second trap was subtler and cost nothing to
fix once seen: an approved plan was executed alone even though the rule
said to summon the party, because the rule was written somewhere the
executor was no longer looking.

Then the reviewer earned its keep, publicly. A feature the Guide built
alone passed every automated check — no errors, correct pixels on
screen, a screenshot that looked right — and cleric still found and
fixed four real bugs in it, two of which any player would have hit in
the first minute. That single episode is why the handoff to cleric is
now unconditional instead of a judgement call, and it repeated this very
level: the review of Session Zero caught stray markup that would have
shipped inside the skill itself.

**What the player learned.** Most of this level's insight was about
words, because in this project words *are* the machine. An instruction
only works if it is in front of the model at the moment it needs to act,
so a rule that must fire during execution belongs in the plan, not only
in the project's standing notes. Defaults matter more than exceptions:
silence should mean the thing you want, because silence is what happens
most often. Examples get copied wholesale, so a skill should show the
*shape* of a good answer and never a full worked one, or its topic
leaks into every unrelated question. And every mandate needs a governor
— "explain everything thoroughly" with no sense of proportion is how a
naming question earns eight hundred words and the user stops asking.

The quieter lesson sits underneath all of them: check the platform
before building on it. Careful criticism said the override design looked
fragile. Only the test showed it was impossible.

*Notes: 10 learnings entries distilled, none flagged as junk. Two entries
(the WSL/tailnet serving recipe and the canvas smoke-test harness)
recorded real traps from a different project and stay in the log without
curated counterparts here, apart from the missing-`jq`/`gh` trap they
surfaced, which now bites this repo directly. Nothing pruned — both
existing gotchas re-verified as still true (three skills still carry
`disable-model-invocation`; `jq` and `gh` still absent).*

*Distilled through 2026-07-26.*

## Level 3 — Wardens of the Azure Star — 2026-07-29

The level the party stopped shipping copies of itself.

**What was built.** Two demolitions and one rebuild. First the experience
display went — the little XP counter in the status bar and the level-up
banner. To print one line of text the plugin had been shipping a nine-step
hunt for a working shell, a script copied into every project, and a repair
path for when that went wrong. Three rounds of fixes had all landed in the
same block. The counter was replaced by something that costs nothing: the
Guide already knows when it writes a learning, so it simply counts then.

The larger rebuild followed. Until this level the plugin *wrote into* your
project — a setup command copied instructions, model config and version
markers into your files, and a whole apparatus existed to detect when those
copies had drifted from what the plugin later shipped. None of it fixed
drift; it only managed it. Now nothing is copied at all: the plugin reads
its own instructions aloud at the start of every session, along with your
project's memory files. Three commands disappeared with the machinery they
served. Updating the plugin now updates every project at once, and the
learnings log became an inbox that a Long Rest empties rather than a ledger
that had to grow forever.

**What was conquered.** The most instructive trap was invisible for three
versions. Two commands decided "is this project already set up?" by looking
for one particular phrase in the project's file — and a rewrite had quietly
stopped writing that phrase. Every correctly-configured project therefore
read as unconfigured, and the one action users are told is safe to repeat
was the one that broke things. Searching the repo for the phrase found it
easily, which is exactly why nobody caught it: an archive of *old* text
looks identical to current text when you search.

Two more came from the same family. A memory display went blank in this
repo because a path recorded once, on a different operating system, had
never been re-checked — and the failure showed nothing at all, in the one
file nobody reviews. A user's plain request to build a game skipped the
planning conversation entirely, and the instinct to fix it with more
instructions was wrong: the rule had been read and agreed with, then judged
not to apply. And 7.5 megabytes of image nearly shipped to every user on
the belief that images aren't part of the download. They are — this repo
*is* the download, permanently, including the parts later deleted.

**What the player learned.** When fix after fix lands in the same place,
the honest conclusion is usually not that you are one fix away — it is that
the machinery is too elaborate for what it delivers. Deleting was cheaper
than repairing, twice over.

Two rules of thumb outlast the specifics. Anything that can be recalculated
should be, and never remembered — a stored count drifts the moment a file
is edited by hand. And a search proves that a *name* is gone, never that
the *promise* is: prose describing a deleted feature contains none of its
words, so after removing something you have to read the neighbours, not
grep them.

The sharpest lesson is one this level failed rather than passed. Every
budget in this project is written down and none of them is measured — the
files loaded into every session are several times the size they are
supposed to be, and the ceremony meant to look after them counts a
different file entirely. A budget with no meter is a wish.

*Notes: 27 entries archived — 15 already distilled at Level 2 and moved
verbatim without re-reading, 12 newly distilled. No junk flagged; every
in-scope entry recorded something non-obvious. Distilled into 3 new
architecture notes and 3 new gotchas. Pruned hard: `decisions.md` fell
17.4KB → 12.4KB, with the interpreter-probe and XP-display-shell decisions
deleted outright (their subject no longer exists), the version-marker
decision collapsed to a one-line tombstone, and five entries amended where
0.7.0/0.8.0 had made half of each untrue. One gotcha narrowed. Not done,
and offered rather than taken: four decision entries remain well over the
file's own 3–5 line budget while still being entirely true — compressing
those is a separate call, not a prune. The `*Distilled through
2026-07-26.*` line above is left as Level 2's record; it is now inert,
since the inbox it bounded is empty.*
