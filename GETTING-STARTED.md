# Getting started on your own machine

Paste these into Claude Code, Codex, or whichever agentic AI harness you like,
one prompt at a time. You do not need to understand git first. The prompts ask
the AI to explain as it goes, which is the point.

Ask for the explanation every time. Getting the command to run is the easy half.
Knowing what you just did is what you are here for.

---

## Before you start

You need three things:

1. **A GitHub account.** Free. [github.com/signup](https://github.com/signup).
2. **Push access to this repository.** Send Ying your username and she will add
   you. Anyone can read a public repository. Changing one takes an invitation,
   and you have to click accept before it works.
3. **An agentic AI harness** in your terminal. Claude Code, Codex, or whatever
   you prefer. Most need a subscription of around 20 USD a month.

---

## Prompt 1: Set up and clone

Run this once, ever.

```
I have never used git or GitHub before. Set me up, and explain each step in
plain language as you go.

1. Check whether git and the GitHub CLI (gh) are installed. If either is
   missing, tell me exactly what to install and stop until I have done it.
2. Check whether I am logged in, with `gh auth status`. If I am not, tell me to
   run `gh auth login` and wait for me.
3. Make a folder called Projects in my home folder, if it isn't already there.
4. Clone https://github.com/adaptiveinc/ladies-who-create into it.
5. Show me what is inside, and explain what a clone is, and what "origin" and
   "main" mean.

Don't change anything in the repository yet.
```

**What you learn:** a clone is your own full copy of the repository. `origin` is
the copy on GitHub that everyone shares. `main` is the version everyone sees.

---

## Prompt 2: Start a new project

```
I want to start a new project in this repository. It is: [one sentence about
what you want].

Work inside the ladies-who-create folder. Before anything else, get me to a
clean start: switch to main, pull the latest, then create a branch for this
work. Name the branch after the project, lowercase with hyphens.

Then:
- Make a folder at the top of the repository named after the project.
- Inside it write a rules file for your AI: CLAUDE.md for Claude Code,
  AGENTS.md for Codex. Put the rules in it: single HTML file, friendly design
  with big readable text, everything saved in the browser, keep every version
  working.
- Then write plan.md: 3 or 4 slices, each one leaving something I can open in
  the browser. For each slice, tell me what I will actually see on screen.

Don't build anything yet. Show me the plan so I can argue with it first.
```

**What you learn:** a branch is your own workspace. Nothing you do on it touches
what anyone else sees until you ask for it to be merged. That is why you can
experiment freely.

---

## Prompt 3: Change something that already exists

```
I want to change something in the [project-name] project: [what you want
different].

First get me to a clean start: switch to main, pull the latest, then create a
branch named after the change.

Then make the change, open the page in the browser, and let me test it before we
go any further. Tell me what you changed and where.
```

**What you learn:** always pull before you branch. Other people have been
working, and starting from an old copy is how you end up with a mess to untangle.

---

## Prompt 4: Save your work and ask for it to go live

```
Commit what I have changed on this branch, push the branch, and open a pull
request against main.

Follow these conventions exactly:

Commit messages on a branch
- One line only. No description underneath.
- Start with a capital letter.
- No prefix. "Add the freezer form", never "feat: add the freezer form".

Pull request title
- Start with a lowercase prefix, one of: feature: fix: build: docs: ci: perf:
  refactor: test:
- Then a capitalised title.
- For example: "feature: Add the freezer list"

Pull request description
- At most 5 bullet points, or one paragraph of at most 4 lines.
- If it will not fit, the change is probably too big. Say so instead of
  writing more.

Never
- No "Co-Authored-By" line, and no footer crediting an AI, on the commit, the
  title, or the description. Drop it even if your tool wants to add it.
- No names, account numbers or other personal details. This history is public
  and permanent.

Show me the commit message, the pull request title, and the description before
you create them, and explain why each one is shaped the way it is.
```

**What you learn:** a commit is a save point with a message attached. Pushing
sends your branch to GitHub. A pull request is you asking for your work to
become part of what everyone sees, and it is where somebody looks at it with you.

---

## Prompt 5: After it is merged

```
My pull request has been merged. Clean up and get me ready for the next thing:
switch back to main, pull the latest, delete my branch locally, and show me the
live link for my project.
```

**What you learn:** your work is on `main` now, and GitHub Pages publishes it
within a minute or two. Delete the branch. It has done its job.

---

## When something goes wrong

It will. Everyone's does. Git is genuinely confusing and the error messages are
written for people who already understand it.

```
Something has gone wrong with git and I don't understand it. Here is what I see:

[paste the whole error]

Explain what has happened in plain language, tell me what my options are, and
recommend one. Don't run anything destructive without asking me first.
```

The last sentence matters. Some git commands throw work away.

---

## Where your project ends up

A folder at the top of this repository with an `index.html` inside it becomes a
web page at:

```
https://adaptiveinc.github.io/ladies-who-create/your-folder-name/
```

No hosting account, no deployment step. Merging to `main` is the deployment.
