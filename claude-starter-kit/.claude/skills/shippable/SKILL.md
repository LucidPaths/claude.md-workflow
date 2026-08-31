---
name: shippable
description: Measure the gap between the work you did and the work a stranger can find, install, run and believe. Hunts empty default branches, unmerged work, manifests that do not install, no keyless path, committed junk that hides the real code, and histories that show nothing. Use before submitting, before a demo, before a handover, and before anyone judges your repository without you in the room.
---

# Shippable — can a stranger find, install, run and believe your work?

## The thesis

There is the work you did, and there is the work that **arrives**. The gap between them is invisible to
exactly one person: you. Your machine has the backend running, the key exported, the right branch checked
out, the packages installed and the missing file sitting in a folder you forgot is not committed. You are
the only human on earth for whom your project works.

Everyone who will ever judge it — a reviewer, an employer, a sponsor, a teammate, you in six months — sees
only what arrived.

**And this is not a tax on sloppy people. It is a tax on ambitious ones.** The most interesting work is
the most likely to be mid-integration when the clock runs out: two halves on two branches, a service that
lives on a laptop, a manifest that stopped tracking reality three features ago. In the corpus this skill
was built from, the single best piece of AI design at the event finished near the bottom because the
server it called was never committed, and another team with the widest provider work sat behind a default
branch containing one README. Neither was a skill problem. Both were transmission problems.

It is also the cheapest score in any assessment. Most of what follows is minutes.

## The stance: become the stranger

Not "review my repo". Adopt the mind of someone with **none of your context**:

> It is 2am. They have an empty machine, no keys, no access to you, and twenty minutes. They are deciding
> something about you — a placing, a job, whether to build on this. They will not ask you a question,
> because you are asleep.

Every time you catch yourself thinking *"well, obviously you'd also need to…"* — that is a defect. Write
it down.

## The seven gates

A stranger hits these in order. Work can fail to arrive at any one of them.

**1. Land.** They open the default branch. Is the work *here*?

```bash
git ls-tree -r --name-only HEAD | grep -v node_modules | wc -l
for b in $(git branch -r | grep -v HEAD); do
  echo "$b $(git ls-tree -r --name-only $b | grep -v node_modules | wc -l)"
done
```

If another branch has meaningfully more files than the default, your work is somewhere nobody will look.
Merging costs minutes; being judged on three quarters of your project costs everything.

**2. Understand.** Can they say what this is in thirty seconds? Open your README as a stranger. If it
still says `create-next-app` or `# Project`, you have written a product and shipped an anonymous folder.
Four sentences: what it does, who for, how to run it, what does not work yet.

**3. Install.** Does the manifest actually list what the code imports?

```bash
grep -rhoE "^(import|from) [a-zA-Z0-9_]+" --include=*.py . | awk '{print $2}' | sort -u
cat requirements.txt        # compare, honestly
```

A project that cannot be installed from its own manifest does not run for anyone but you. This is the
single most common way real work fails to arrive.

**4. Configure.** Are secrets read from the environment, and is there a `.env.example` with **names and
no values**? Two specific anti-patterns, both seen in real submissions:

- keys written as empty string literals in source (`api_key=""`) — the day someone pastes a real key in
  to test, it is committed forever;
- a URL pointing at `localhost` with no way to override it.

**5. Run.** Is there a path that works with **no key and no network**? Not the full product — a recorded
transcript, a seeded database, a fixture mode, clearly labelled as such. If your code raises at import
when a key is missing, nobody without your key ever sees a single screen.

**6. Believe.** Can they tell what is yours?

```bash
git ls-files | grep -E "node_modules/|\.venv/|dist/|build/|\.env$|\.db$" | wc -l
```

Committed dependencies, build output and virtualenvs bury twenty real files inside ten thousand. Nobody
reviews a ten-thousand-file diff; they guess, and they guess low. The same applies to inherited code from
an earlier project: say what is reused and what is new, or your line count misleads a reader who is trying
to be fair to you.

**7. Verify.** Is there anything that shows it works? One test, one seed script, one `docker-compose up`,
one committed sample input with its expected output. This is the difference between "they claim it works"
and "I watched it work without asking them".

## The cold-clone test

The gates are the checklist. This is the actual test, and it takes fifteen minutes:

1. Clone your repository into a **fresh empty directory** — not your working copy.
2. Follow your own README **literally**. Type only what it says.
3. Use nothing from your head. No key you happen to have exported, no service already running.
4. Time it, and write down every point where you had to know something the repository never told you.

That list is your defect list, in priority order. Nothing else you do this week will improve how your work
is received as much as fixing it.

## The verdict

```
GATE     which of the seven
HITS     what the stranger actually experiences
COSTS    what they conclude about the work because of it
FIX      the change, and roughly how many minutes
```

Sort by minutes ascending. Most of this list will be under ten each, which is the point.

## One thing that is not about the code

Your commit history is the only record of **how you work** — iterating, finding a bug, reverting a bad
direction, splitting tasks. It is what an employer reads that a finished artefact cannot show. A project
delivered as one bulk upload throws that away permanently: the work happened, and no evidence of it
survives.

Commit from the first hour, even scruffily. Ten rough commits beat one perfect upload, and the difference
is not tidiness — it is whether two days of your life left a trace.

## What good looks like

All of these are real, all from two-day builds, none of them expensive:

- a seed script and a `docker-compose.yml`, so a stranger gets a running system with data in it
- database migrations rather than a schema that exists only in someone's head
- a fixture or recorded-replay mode so the pipeline runs with no key and no network
- valid **and invalid** sample inputs committed, so both branches of a check can be demonstrated
- commit messages that name what changed and why — including the reverts
- a README that states plainly what is not built yet

## Where this came from

Distilled from a line-by-line review of seventeen repositories built at the AI Builder Hackathon in Addis
Ababa, August 2026. Every gate above is a failure that actually happened there, and every item under
*what good looks like* is something a team did under the same two-day pressure.

Same rule as its sibling skill: **the working patterns are credited, the failures are anonymous.** The
teams concerned received them privately, in detail, by name.

Run this with `unverified`. That one asks whether your system can admit what it does not know. This one
asks whether anyone but you will ever find out.
