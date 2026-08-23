"""Build recipes.csv from TheMealDB (https://www.themealdb.com).

Real recipes: name, ingredients, method and photo all come from the API, along
with a link to the original source. What this script *estimates* — and labels as
estimated — is prep time, calories, protein and kid-friendliness, because the
API does not carry them.

Run:  python3 tools/build_recipes.py
"""
import csv, json, re, string, sys, urllib.request

API = "https://www.themealdb.com/api/json/v1/1/search.php?f="
SKIP_CATEGORIES = {"Dessert", "Side", "Starter", "Breakfast"}

# --- units -------------------------------------------------------------
UNIT_WORDS = [
    (r"\b(tablespoons?|tbsp?s?|tbs)\b", "tbsp"),
    (r"\b(teaspoons?|tsps?)\b", "tsp"),
    (r"\b(kilograms?|kgs?)\b", "kg"),
    (r"\b(grams?|gr?s?)\b", "g"),
    (r"\b(millilitres?|milliliters?|mls?)\b", "ml"),
    (r"\b(litres?|liters?|l)\b", "l"),
    (r"\b(ounces?|oz)\b", "oz"),
    (r"\b(pounds?|lbs?)\b", "lb"),
    (r"\b(cups?)\b", "cup"),
    (r"\b(cloves?)\b", "clove"),
    (r"\b(sprigs?)\b", "sprig"),
    (r"\b(slices?)\b", "slice"),
    (r"\b(sticks?)\b", "stick"),
    (r"\b(pinch(es)?|dash(es)?)\b", "pinch"),
    (r"\b(handfuls?)\b", "handful"),
    (r"\b(bunch(es)?)\b", "bunch"),
    (r"\b(cans?|tins?)\b", "tin"),
    (r"\b(fillets?)\b", "fillet"),
]
FRACTIONS = {"½": .5, "¼": .25, "¾": .75, "⅓": 1/3, "⅔": 2/3, "⅛": .125}
TO_METRIC = {"oz": ("g", 28.35), "lb": ("g", 453.6), "cup": ("ml", 240.0)}

def parse_measure(text):
    """'800g' -> (800, 'g');  '2 tablespoons' -> (2, 'tbsp');  'to taste' -> (1, '')"""
    t = (text or "").strip().lower()
    if not t:
        return 1.0, ""
    for sym, val in FRACTIONS.items():
        t = t.replace(sym, f" {val} ")
    t = re.sub(r"(\d)\s*([a-z])", r"\1 \2", t)      # "400g" -> "400 g"
    nums = re.findall(r"\d+\s*/\s*\d+|\d+\.\d+|\d+", t)
    qty = 0.0
    if nums:
        first = nums[0]
        qty = (float(first.split("/")[0]) / float(first.split("/")[1])) if "/" in first else float(first)
        if len(nums) > 1 and "/" in nums[1]:                       # "1 1/2"
            a, b = nums[1].split("/")
            qty += float(a) / float(b)
    unit = ""
    for pattern, name in UNIT_WORDS:
        if re.search(pattern, t):
            unit = name
            break
    if unit in TO_METRIC:
        unit, factor = TO_METRIC[unit]
        qty *= factor
        qty = round(qty)
    return (qty or 1.0), unit

# --- aisles ------------------------------------------------------------
AISLES = [
    ("meat and fish", ["chicken","beef","pork","lamb","mince","bacon","sausage","chorizo","ham",
                       "turkey","duck","steak","fish","salmon","tuna","cod","prawn","shrimp",
                       "haddock","anchov","squid","crab","mussel","gammon","veal"]),
    ("dairy",         ["milk","butter","cheese","cream","yoghurt","yogurt","egg","parmesan",
                       "mozzarella","mascarpone","creme","custard"]),
    ("freezer",       ["frozen","puff pastry","filo","ice cream"]),
    ("produce",       ["onion","garlic","tomato","pepper","carrot","potato","lemon","lime",
                       "spinach","mushroom","ginger","chilli","chili","lettuce","cucumber",
                       "courgette","zucchini","aubergine","eggplant","broccoli","celery","leek",
                       "cabbage","coriander","parsley","basil","thyme","rosemary","mint","sage",
                       "shallot","apple","banana","avocado","lime","orange","pear","kale",
                       "cauliflower","bean sprout","spring onion","scallion","squash","pumpkin",
                       "sweet potato","aubergine","asparagus","peas","corn","salad","cress",
                       "beetroot","turnip","parsnip","radish","fennel","dill","chive"]),
]
def aisle_for(name):
    low = name.lower()
    for aisle, words in AISLES:
        if any(w in low for w in words):
            return aisle
    return "dry goods"

# --- estimates (clearly labelled as such) ------------------------------
NUTRITION = {                       # kcal, protein per portion — rough
    "Beef": (650, 40), "Lamb": (680, 40), "Pork": (620, 38), "Chicken": (550, 38),
    "Seafood": (500, 35), "Pasta": (600, 25), "Vegetarian": (450, 18), "Vegan": (420, 15),
    "Goat": (600, 40), "Miscellaneous": (550, 28),
}
# Not every real recipe is a family dinner. These keep jams, cakes and drinks out.
NOT_DINNER = ["jam","marmalade","cake","cookie","biscuit","pudding","brownie","trifle","jelly",
              "fudge","smoothie","cocktail","punch","custard","scone","muffin","pancake","waffle",
              "doughnut","donut","ice cream","sorbet","cheesecake","crumble","flapjack",
              "shortbread","macaron","mousse","parfait","sundae","syrup","compote","eclair",
              "milkshake","lemonade","frappe","toast","porridge","granola","cupcake","tiramisu",
              "pavlova","meringue","fritter","truffles","brulee","banoffee","strudel","clafoutis",
              "rock cakes","tea","coffee","smoothy","dessert","sweet roll","bread and butter"]

# a dinner needs something to build the plate around
SUBSTANTIAL = ["chicken","beef","pork","lamb","fish","salmon","tuna","cod","prawn","shrimp","crab",
               "bean","lentil","chickpea","tofu","paneer","egg","pasta","spaghetti","macaroni",
               "rice","noodle","potato","quinoa","couscous","cheese","mince","sausage","bacon",
               "turkey","duck","mushroom","aubergine","haddock","gnocchi","tortilla","lasagne"]

SWEETS = ["sugar","honey","golden syrup","maple syrup","caster","icing"]

def is_dinner(meal, ingredients):
    name = meal["strMeal"].lower()
    if any(w in name for w in NOT_DINNER):
        return False
    names = " ".join(i[0].lower() for i in ingredients)
    if not any(w in names for w in SUBSTANTIAL):
        return False
    sweet = sum(q for i, q, u, a in ingredients
                if any(w in i.lower() for w in SWEETS) and u in ("g", "ml"))
    if sweet >= 150:
        return False
    return 4 <= len(ingredients) <= 18

SPICY = ["chilli","chili","jalape","cayenne","curry powder","harissa","sriracha","chipotle",
         "wasabi","horseradish","anchov","blue cheese","olives","wine","brandy","rum"]

def estimate(meal, ingredients, steps):
    kcal, protein = NUTRITION.get(meal["strCategory"], (550, 28))
    minutes = max(15, min(90, 15 + 5 * len(steps) + (15 if meal["strCategory"] in ("Beef","Lamb") else 0)))
    minutes = int(round(minutes / 5) * 5)
    names = " ".join(i[0].lower() for i in ingredients)
    kid = not any(w in names for w in SPICY)
    profile = "high-protein" if protein >= 38 else "light" if kcal < 480 else "balanced" if kcal <= 600 else "hearty"
    return minutes, kcal, protein, kid, profile

def slug(name):
    s = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return s[:60]

def fetch(letter):
    url = API + letter
    req = urllib.request.Request(url, headers={"User-Agent": "meal-planner-workshop/1.0"})
    return json.load(urllib.request.urlopen(req, timeout=45)).get("meals") or []

def main():
    rows, seen = [], set()
    for letter in string.ascii_lowercase:
        try:
            meals = fetch(letter)
        except Exception as exc:
            print(f"  {letter}: failed ({exc})", file=sys.stderr)
            continue
        print(f"  {letter}: {len(meals)}")
        for meal in meals:
            if meal["strCategory"] in SKIP_CATEGORIES:
                continue
            rid = slug(meal["strMeal"])
            if not rid or rid in seen:
                continue
            ingredients = []
            for n in range(1, 21):
                item = (meal.get(f"strIngredient{n}") or "").strip()
                if not item:
                    continue
                qty, unit = parse_measure(meal.get(f"strMeasure{n}"))
                ingredients.append((item.strip().lower(), qty, unit, aisle_for(item)))
            if not is_dinner(meal, ingredients):
                continue
            raw = re.sub(r"\r\n?", "\n", meal["strInstructions"])
            raw = re.sub(r"(?im)^\s*step\s*\d+\s*", "", raw)
            steps = [s.strip() for s in re.split(r"\n+|(?<=[.!?])\s{2,}", raw) if len(s.strip()) > 12]
            if not steps:
                continue
            minutes, kcal, protein, kid, profile = estimate(meal, ingredients, steps)
            seen.add(rid)
            rows.append({
                "id": rid,
                "name": meal["strMeal"],
                "photo": meal["strMealThumb"],
                "source": meal.get("strSource") or f"https://www.themealdb.com/meal/{meal['idMeal']}",
                "cuisine": meal.get("strArea") or "",
                "category": meal["strCategory"],
                "minutes_estimated": minutes,
                "kcal_estimated": kcal,
                "protein_estimated": protein,
                "kid_friendly_estimated": "yes" if kid else "no",
                "profile_estimated": profile,
                "serves": 4,
                "ingredients": ";".join(f"{q:g}|{u}|{i}|{a}" for i, q, u, a in ingredients),
                "steps": "||".join(steps),
            })
    rows.sort(key=lambda r: r["name"])
    with open("recipes.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nwrote recipes.csv — {len(rows)} recipes")

if __name__ == "__main__":
    main()
