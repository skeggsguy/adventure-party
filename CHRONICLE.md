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
