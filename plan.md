# Build Plan: Family Meal Planner

## Where we are

- [x] Slice 1 — Tell it about us, get a week
- [x] Slice 2 — No repeats across two weeks
- [x] Slice 3 — Thumbs up, thumbs down
- [x] Slice 4 — The shopping list and the recipes
- [x] Slice 5 — Real recipes, in a spreadsheet
- [ ] Slice 6 — Share it with everyone (not started)

Tick a box only when the group has tested the slice in the browser and agreed
it works. The rules every slice must obey live in `CLAUDE.md`.

## Progress, 23 August 2026

**The app works end to end.** One file, `index.html`, reading 420 real recipes
from `recipes.csv`. Every slice was tested in the browser before being ticked.

| Built | Checked by |
|---|---|
| Form → seven dinners, filtered by allergies, dislikes, prep time and children's ages | Ticking nuts leaks nothing; a 20-minute limit shows nothing longer |
| Cards that flip to the recipe, amounts scaled to your portions | 2 portions vs 8 doubles every amount; no fractional eggs anywhere |
| Rolling memory of the last 14 dinners | Two weeks back to back share nothing; the count tops out at 14 |
| 👍 / 👎 changing future weeks | A banned dish stayed gone across 8 fresh plans; loved dishes appear ~2× as often |
| Shopping list, one row per ingredient, grouped by aisle | Zero duplicate rows across 20 randomly generated weeks |
| Copy for WhatsApp, and a printable week | Copy confirms; print gives the list plus seven recipes |
| 420 real recipes with photos, method and source links | Gluten-and-dairy-free households went from 11 dinners to 86 |

**Still estimates, and labelled as such in the app:** prep time, calories,
protein, and whether a dish is kid-friendly.

**Known limits.** The memory counts dinners, not days — plan four weeks in one
sitting and week one becomes available again. Dislikes match words and groups,
not concepts, so "meat" works but "healthy" does not. Recipe amounts assume the
original serves four.

**Open points to work through next:** (add them here as they come up)

- [ ] _(waiting on the list from the room)_

## The whole stack, one line

One HTML file, opened by double-clicking it. Plain HTML for the page, CSS for
the looks, JavaScript for the thinking. No framework, no server, no database,
no install. The browser is the whole computer.

## Your requirement → what we're using

| You asked for | We build it with | Why this |
|---|---|---|
| A form: preferences, nutrition, age, prep time | Standard HTML form fields (tick boxes, slider, buttons) | Every browser already knows how to draw these. Zero build time. |
| Seven days of meals | A JavaScript list of ~60 recipes written into the file, filtered and picked by a small function | Instant, works offline, we can read it and fix it in the room |
| Real recipes, creative | Claude writes the dishes and looks up their photos while we build | Real food, nothing to break during the demo — but the amounts are estimates, not tested recipes |
| A picture of each dish | An `<img>` pointing at a photo link, with a coloured fallback tile | Keeps the file small; never shows a broken image |
| No overlap for two weeks | `localStorage` — the browser's own memory, saved on this computer | Survives closing the page. No database, no login. |
| Feedback on cooked dishes | 👍 / 👎 buttons, also saved in `localStorage`, read back when planning | Same memory, same trick |
| Shopping list | JavaScript adds up the ingredients, groups them by aisle; clipboard button | One function, no library |
| Recipe list to look at or print | A print stylesheet (`@media print`) — the browser makes the PDF | Free. The browser already has a print engine. |

**What we are not using, on purpose:** React, Node, npm, a database, a login
system, a hosting service. Any one of them costs more than an afternoon.

---

## Slice 5: Real recipes, in a spreadsheet

**You see.** A line under the title: *"420 real recipes, loaded from
recipes.csv."* Dishes with real photos, real method, and **the original
recipe ↗** on the back of every card.

**Build it:**
1. `tools/build_recipes.py` pulls every meal from TheMealDB, keeps the ones that
   are actually family dinners (no jams, cakes or drinks; something substantial
   on the plate), parses "800g" and "2 tablespoons" into numbers and units, sorts
   each ingredient into a supermarket aisle, and writes `recipes.csv`.
2. The app fetches `recipes.csv` at startup and falls back to the 65 built-in
   recipes when it cannot — which is what happens if you double-click the file
   instead of serving it. Neither way ever shows an error.
3. Allergens are still derived from the ingredients, so the real recipes are
   tagged by the same rule as the made-up ones.

**Run this:**
```
Implement slice 5 from plan.md, then open it in the browser so we can test.
```

**Tester checks:** the line says 420. Flip a card — the recipe links to its
source. Tick two allergies — the pool is far bigger than it used to be.

**Done when:** the app runs on real recipes and still passes every check from
slices 1 to 4.

---

## Slice 6: Share it with everyone

**You see.** A web address you can send to the group, and a repository they can
open, read and copy.

**Build it:**
1. Publish the folder to GitHub.
2. Turn on GitHub Pages so `index.html` is a link, not a download.
3. `README.md` explains what it is, how to run it, and how it was built.

**Done when:** someone who was in the room can open the link on their phone and
plan a week.

---

## Slice 1: Tell it about us, get a week

**You see.** A form — how many adults, children's ages, how many grown-up
portions to cook for, a dislikes box, allergy tick boxes (dairy, gluten, nuts,
eggs, fish), three goal buttons (balanced / lighter / high protein) and a
prep-time slider — then a **Plan my week** button. Beside it, seven cards,
Monday to Sunday.

**The cards flip.** Front: photo, day, dish name, prep time, nutrition per
person, kid-friendly mark. Tap it and it turns over: the ingredients with the
amounts scaled to your portions, and the steps. Tap again to turn back.

The portions box fills itself in from the household (an adult is one portion, a
child under 12 is half) and you can overrule it for guests — every amount in
the app follows that number.

**Build it:**
1. Make `index.html` — one file, page shell, big readable styling.
2. Claude writes ~60 real family dinners into the file as a list called
   `RECIPES`, and looks up a photo for each on the web. The amounts, steps and
   nutrition are Claude's own estimates, not sourced from tested recipes — the
   app says so on the card. Each is a complete meal — main, green, starch — and
   its name says so. Each is shaped like this:
   `{ id, name, photo, minutes, kidFriendly, profile, kcal, protein,
   allergens: [], ingredients: [{ item, qty, unit, aisle }], steps: [] }`
   Profile is `light`, `balanced`, `hearty` or `high-protein`. Aim for a spread: at least
   20 dishes under 25 minutes, at least 15 with no common allergens.
3. Build the form. Save its answers to `localStorage` under `mealplanner.prefs`
   so the page comes back filled in.
4. Work out allergens from the ingredients with one shared table, rather than
   tagging each recipe by hand — that is what stops gnocchi being sold as
   egg-free.
5. Write `filterRecipes(prefs)` — drop anything with a ticked allergen, anything
   matching a disliked word or its group ("pasta" catches tortellini), anything
   slower than the slider, and anything not kid-friendly when a child under 12
   is listed.
6. Write `planWeek(prefs)` — score what survives (goal match first), pick seven
   different ones, assign Monday to Sunday, save to `mealplanner.week`.
7. Render the cards, front and back — tap to flip, and the card grows to fit
   the recipe rather than hiding it behind a scrollbar. Each photo is an `<img>` with an `onerror` that swaps in a
   coloured tile showing the dish name.
8. Scale the amounts: pool recipes are written for 4 grown-up portions. The
   portions box defaults to the household (adult = 1, child under 12 = 0.5) and
   can be overridden. The back of each card shows the scaled ingredients and
   the steps.

**Run this:**
```
Implement slice 1 from plan.md. Search the web for real family dinner recipes
for the pool. Then open it in the browser so we can test.
```

**Tester checks:** tick nuts — no nut dishes appear. Drag the slider to 20
minutes — nothing longer shows. Plan twice — you get different weeks. Tap a
card — it flips to the recipe. Set portions to 8 — the amounts double.

**Done when:** the form gives us seven dish cards with photos, and tapping one
shows a recipe with amounts that match the number of people.

---

## Slice 2: No repeats across two weeks

**You see.** A line under the button — "Avoiding 7 dinners from the last two
weeks" — and a **Recently planned** strip at the bottom, dish names with the
date each was planned. If the rules leave fewer than seven dishes, a friendly
yellow box says which setting to loosen instead of breaking.

**Build it:**
1. On every plan, append the seven dishes to `mealplanner.history` as
   `{ id, date }`. The rule is a rolling memory: **the last 14 dinners planned**
   stay off the menu — two weeks' worth. Plan a third week and the first one
   rolls off and becomes available again. The count never runs past 14, however
   many times the button is pressed.
2. Write `recentIds()` — the ids of the last 14 entries in the history.
3. `planWeek` now removes those ids before picking.
4. Show the count in the line under the button, and render the strip from the
   history, newest first.
5. If fewer than seven dishes survive every filter, show the yellow box. Work
   out the tightest setting by trying each one loosened in turn and reporting
   whichever adds the most dinners.

**Run this:**
```
Implement slice 2 from plan.md, then open it in the browser so we can test.
```

**Tester checks:** plan a week — avoiding 7. Plan again — avoiding 14, zero
dishes in common. Keep planning — the count stays at 14 and week one starts
coming back. Close the tab, reopen the file —
the strip still shows week one. Set prep time to 15 minutes with three
allergies — the yellow box appears, no crash. Press "Forget my history",
confirm, and everything is available again.

**Done when:** two weeks back to back share nothing, the count tops out at 14,
and closing the page doesn't forget.

---

## Slice 3: Thumbs up, thumbs down

**You see.** 👍 and 👎 at the bottom of every dish card, next to the recipe
link. Tapping one lights it up and marks the card — a green edge for loved, a
faded card for banned — without flipping it. Below the week, a **Hits and
misses** panel: loved on the left, banned on the right, every entry with an
**undo**. Tapping the same thumb twice clears the verdict.

**Build it:**
1. Store verdicts in `mealplanner.ratings` as `{ recipeId: "up" | "down" }`.
2. Add the two buttons to the card. Clicking saves the verdict and repaints
   that card only — and must stop the click reaching the flip handler.
3. `planWeek` now reads ratings: `down` dishes are removed from the pool
   entirely; `up` dishes get a scoring boost so they return as soon as the
   14-day window allows.
4. Render the panel from the ratings. Undo deletes that dish's entry.

**Run this:**
```
Implement slice 3 from plan.md, then open it in the browser so we can test.
```

**Tester checks:** thumbs-down a dish, plan a fresh week — it's gone, and it's
in the banned column. Press undo — it can appear again. Thumbs-up a dish,
close and reopen the file — the thumb is still filled.

**Done when:** a banned dish never comes back until someone undoes it.

---

## Slice 4: The shopping list and the recipes

**You see.** Two buttons above the week. **Shopping list** opens a panel over
the page: every ingredient from the seven dinners in one list, amounts added
up, grouped under aisle headings, with **Copy for WhatsApp** at the top.
**Print recipes** gives the seven recipes — photo, ingredients, steps — ready
to print or save as PDF.

**Build it:**
1. Write `shoppingList(week)` — walk all seven recipes' ingredients **after
   scaling to the portions**, merge matching `item` names, add the quantities,
   and group by `aisle` (produce, meat and fish, dairy, dry goods, freezer).
   **One row per ingredient, always.** That means every unit has to reduce to a
   common one: kg to g, pieces to grams (a chicken breast is 175g), spoons to
   grams for dry things and to millilitres for liquids, a handful of basil to
   15g. Then it converts back to whatever a person would write down — spoons for
   small amounts, kg above a thousand grams, whole numbers for things you buy
   whole.
2. Render it in a panel with a close button.
3. Copy button uses `navigator.clipboard.writeText`, falling back to a hidden
   textarea when the page is opened straight off the disk, and confirms with
   "Copied — paste it into WhatsApp."
4. Build the print view: each recipe as a block with its photo, ingredients and
   numbered steps.
5. Add a `@media print` stylesheet — hide the form, the buttons and the panel,
   keep the food, break pages between recipes.

**Run this:**
```
Implement slice 4 from plan.md, then open it in the browser so we can test.
```

**Tester checks:** two dishes both using onions show one combined line. Press
copy, paste into any text box — a readable list appears. Press print and look
at the preview: no form, no buttons, seven readable recipes.

**Done when:** we press print and see a shopping list plus seven recipes we'd
take into the kitchen.

*(Print gives two pages: the shopping list, then the week's recipes with photos,
scaled amounts and steps.)*
