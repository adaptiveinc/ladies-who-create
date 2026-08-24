# Ladies Who Create

We meet, we pick one real problem, and we build something that works before we
go home. Nobody needs to know how to code. The skill we're practising is saying
clearly what you want.

Everything we build lives in this repository, one folder per project, and every
one of them is online.

## What's here

| Project | Live | Built |
|---|---|---|
| [Family Meal Planner](meal-planner/) | [Open it ↗](https://adaptiveinc.github.io/ladies-who-create/meal-planner/) | Session 1 — 23 August 2026 |

## Pick up a problem

Every idea anyone has submitted is an [issue](../../issues). Nothing is
rejected and nothing is assigned by anyone but you.

1. Find one you like in the [issue list](../../issues).
2. Comment **"I'll take this"** and add yourself as an assignee.
3. If someone is already on it, say you want in — two or three people on one
   problem is better than one, not worse.
4. Build it. Come and show us, whether or not it's finished.

**Claims last until the next session.** If nothing happened, it goes back to
the pool. No explanation owed, and no shame in it — you can pick it up again.

Have a new problem? [Open an issue](../../issues/new/choose). Small and annoying
beats big and impressive. "I hate renaming my photos" is a better starting point
than "an app for the whole family".

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

Then repeat the last one, changing the number, until you run out of slices or
afternoon. Try to break each slice in the browser before moving to the next.

Four things that made the difference in session one:

- **Write the rules down first.** `CLAUDE.md` is the memory. The AI starts every
  conversation with a blank mind.
- **Make it plan before it builds.** Arguing with a plan is cheap.
- **Slices, never the whole app.** Each one leaves something that works.
- **Small on purpose.** No framework, no server, no database, no login. One file
  you can double-click.

## Put yours online

Make a folder at the top of this repository, named after your project, with an
`index.html` inside it. Push it. It appears at:

```
https://adaptiveinc.github.io/ladies-who-create/your-folder-name/
```

That's the whole deployment story. No build step, no hosting account.

You can push straight to `main` — there are no pull requests to learn here.
Just stay inside your own project folder.

## House rules

- Finished and tiny beats ambitious and broken.
- Test it before you call it done. Try to break it yourself first.
- Write down what's still wrong, in your project's `plan.md`. Known bugs are
  not embarrassing; hidden ones are.
- Come and show it, working or not. How it went wrong is the interesting part.
