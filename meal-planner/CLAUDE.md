# Family Meal Planner

We are building the Family Meal Planner:

> "Tell it about your family (ages, allergies and food preferences, nutrition
> goal, how much time you have to cook) and get a full seven-day dinner plan.
> Nothing repeats across two weeks. Tell it what you actually cooked and how it
> went, and the next plan gets better. One click gives you the shopping list
> and the recipes."

## How we build

`plan.md` is the build plan — four slices. Read it before writing any code.
Build one slice at a time, never more, and stop when it works. When the group
agrees a slice is done, tick it off in the "Where we are" list at the top of
`plan.md` so the next conversation knows where to pick up.

## Rules

- Single HTML file. No install, no build step, no server. Double-click to open.
- Tapping a dinner opens its recipe as a full-size card over the week, not as a
  flip inside the small card — a recipe needs width to be readable.
- Never size a full-screen panel with `100vh` — on a phone the address bar makes
  it taller than the visible page and the top of the panel, close button and
  all, ends up off-screen. Use `100dvh`, and give anything full-screen a second
  way out that a thumb can reach.
- Friendly design, big readable text, works on a TV screen and prints cleanly.
- The recipes live in `recipes.csv`, not in the code. The app loads it at
  startup and falls back to the built-in pool when the browser blocks the read
  (which is what happens on a double-click). Rebuild the file with
  `tools/build_recipes.py`; never hand-edit recipes inside `index.html`.
- The dishes are real ones and their photos come from TheMealDB. The amounts, timings, steps and nutrition numbers are written by
  Claude from general knowledge — plausible, but not taken from a tested recipe
  and not measured. The app says so wherever it shows them. Anywhere it matters
  more than that, the fix is sourcing real recipes, not tidier wording.
- The finished app does not call out to the internet when it runs, so it always
  opens and always works. The pool must be big enough that two weeks of
  no-repeats always works, even after allergies and prep time filter it down.
- The shopping list shows one row per ingredient, never two. Units are reduced
  to a common measure before adding up (kg to g, pieces to grams, spoons to
  grams or millilitres) and converted back for display.
- Amounts are written the way a cook would say them: spoonable things
  (spices, oils, pastes, flour) show as tbsp or tsp up to four spoons and switch
  to weight above that; anything bought whole — eggs, peppers, garlic cloves —
  is a whole number, never 1.5.
- Every recipe carries tags: ingredients with amounts, prep time in minutes,
  kid-friendly flag, and a nutrition profile (light / balanced / hearty /
  high-protein) with rough calories and protein.
- Allergens are never typed in by hand per recipe. One table maps ingredients to
  allergens (soy sauce and egg noodles contain gluten, gnocchi and fresh pasta
  contain egg, prawns count as fish) and every recipe's allergens are worked out
  from its own ingredient list. A new recipe is tagged the moment it is written.
- Every dinner is a whole meal: a main, something green, and something starchy.
  The dish name says what is on the plate — "Pork souvlaki with roast potatoes",
  not "Pork souvlaki".
- Dislikes match through groups, so "pasta" also catches tortellini and gnocchi,
  and "meat" catches mince, bacon and chorizo.
- Recipe amounts are written for 4 grown-up portions. The app scales them to the
  household: each adult is one portion, each child under 12 is half a portion.
  Every screen that shows amounts says who they are for.
- Every recipe has a photo of the dish. Photos load from the web, and each card
  falls back to a drawn tile with the dish name if a photo does not load — so
  the app never shows a broken image, even with no wifi.
- Feedback is a thumbs up and a thumbs down on the dish card. Thumbs up means
  plan it again sooner; thumbs down means never plan it again. Nothing else.
- The plan, the history and the feedback live in the browser (localStorage),
  so the no-repeat rule and the ratings survive closing the page.
- The no-repeat rule is a rolling memory of the last 14 dinners planned — two
  weeks' worth. A fifteenth pushes the oldest back onto the menu. The number
  avoided never exceeds 14, however often the button is pressed.
- No browser dialogs (`confirm`, `alert`). Anything needing confirmation asks
  inline, because dialogs get blocked and then the button just looks broken.
- Keep every version working. Small steps, test after each one.

## Not in scope

- Accounts and login. No sign-up, no password. The plan, the history and the
  ratings live in this browser on this computer only — they do not follow the
  family to another device.
- The app fetching new recipes by itself while it runs (dish photos are the
  one thing it loads from the web)
- Automatic online shopping cart
- Breakfast and lunch — dinners only
