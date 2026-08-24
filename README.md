# Ladies Who Create

We meet, pick one real problem, and build something that works before we go
home. Nobody needs to know how to code. The skill we practise is saying clearly
what you want.

Everything we build lives here, one folder per project, and all of it is online.

## What's here

| Project | Live | Built |
|---|---|---|
| [Family Meal Planner](meal-planner/) | [Open it ↗](https://adaptiveinc.github.io/ladies-who-create/meal-planner/) | Session 1, 23 August 2026 |

## How we work together

**One repository, one folder per project.** One place to look, one issue list,
one web address.

**Issues are the backlog.** One issue per problem. Nothing is ever rejected, and
nobody assigns them but you. Browse them: [open issues](../../issues).

**Assigning yourself is how you claim something.** Open the issue, comment
**"I'll take this"**, then click *assign yourself* in the sidebar.

- One name on an issue is a solo build.
- Two or three names is a group that formed itself, which is better. If somebody
  got there first, say you want in.

**A claim lasts until the next session.** If life got in the way it goes back to
the pool. No explanation owed, and you can pick it up again later.

**Every idea gets a plan, built or not.** Somebody runs the two prompts below on
the issue and pastes the result into it. Then it's ready the day you feel like
starting.

**Everyone's idea gets its turn.** Across a season we each get one afternoon on
our own problem. Voting decides the order, not whether.

### The five stages

Labels track where each idea is, and the board shows the same thing as columns:

| Stage | What it means |
|---|---|
| `submitted` | An idea, written down. Nothing has happened yet. |
| `has-a-plan` | Cut to one sentence, with slices. Ready for someone to start. |
| `claimed` | Somebody is on it. |
| `built` | It exists and it works. There's a folder and a link. |
| `in-use` | Somebody actually uses it. This is the one that counts. |

There is more than one way to finish. Building it alone counts. Somebody
actually using it counts most.

### New problems

[Open an issue](../../issues/new/choose). Small and annoying beats big and
impressive. "I hate renaming my photos" is a better starting point than "an app
for the whole family".

### No pull requests

Push straight to `main`. Stay inside your own project folder and you cannot get
in anybody's way. Forks and pull requests are where beginners drown, and we do
not need them here.

## How we build

Open [Claude Code](https://claude.com/claude-code) in an empty folder and use
these three, in order. This is close to what we actually typed in session one.

```
> Create a CLAUDE.md for this project. We are building: [your one sentence].
  Rules: single HTML file, friendly design with big readable text, everything
  saved in the browser, keep every version working.
```

```
> Read CLAUDE.md and write plan.md: break the build into 3-4 small slices, each
  one leaving a fully working app I can open in the browser. Keep it short and
  non-technical.
```

```
> Implement slice 1 from plan.md, then open it in the browser so we can test.
```

Repeat the last one, changing the number, until you run out of slices or
afternoon. Try to break each slice in the browser before you move on.

Four things that made the difference in session one:

- **Write the rules down first.** `CLAUDE.md` is the memory. The AI starts every
  conversation with a blank mind.
- **Make it plan before it builds.** Arguing with a plan is cheap.
- **Slices, never the whole app.** Each one leaves something that works.
- **Small on purpose.** No framework, no server, no database, no login. One file
  you can double-click.

## Put yours online

Make a folder at the top of this repository, named after your project, with an
`index.html` inside. Push it. It appears at:

```
https://adaptiveinc.github.io/ladies-who-create/your-folder-name/
```

That's the whole deployment story. No build step, no hosting account.

## House rules

- Finished and tiny beats ambitious and broken.
- Test it before you call it done. Try to break it yourself first.
- Write down what's still wrong in your project's `plan.md`. Known bugs are not
  embarrassing. Hidden ones are.
- Come and show it, working or not. How it went wrong is the interesting part.
