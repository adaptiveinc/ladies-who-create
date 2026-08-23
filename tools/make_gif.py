"""Record a short GIF walkthrough of the meal planner.

Each frame is its own headless-Chrome page load driven to a fixed step, so the
plan never reshuffles mid-recording. Needs the local server on :8777.

Run:  /tmp/gifenv/bin/python tools/make_gif.py
"""
import csv, json, os, subprocess, sys
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE = "http://localhost:8777"
FRAMES = "/tmp/mealframes"
STEPS = [
    (0, 1400),   # the empty form
    (1, 1400),   # family filled in
    (2, 1600),   # nut allergy ticked
    (3, 2200),   # the week appears
    (4, 1800),   # first card flipped to its recipe
    (5, 1800),   # second card flipped
    (6, 1500),   # thumbs up
    (7, 2600),   # shopping list
]

DRIVER = """
<script>
(function(){
  var step = parseInt(new URLSearchParams(location.search).get('step') || '-1', 10);
  if(step < 0) return;
  var WEEK = __WEEK__;
  var waited = 0;
  var timer = setInterval(function(){
    waited += 60;
    var loaded = (typeof RECIPES !== 'undefined' && RECIPES.length > 100);
    if(!loaded && waited < 8000) return;
    clearInterval(timer);
    function set(id, v){ var e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('input')); }
    if(step >= 1){ set('adults', 2); set('kids', '6, 11'); set('mins', 45); }
    if(step >= 2){ document.querySelectorAll('#allergies .chip').forEach(function(b){ if(b.dataset.a === 'nuts') b.click(); }); }
    if(step >= 3){
      localStorage.setItem('mealplanner.week', JSON.stringify(WEEK));
      renderWeek(WEEK); document.getElementById('actions').hidden = false; showAvoiding();
    }
    if(step >= 4){ document.querySelectorAll('.dish')[0].querySelector('.inner').click(); }
    if(step >= 5){ document.querySelectorAll('.dish')[1].querySelector('.inner').click(); }
    if(step >= 6){ document.querySelectorAll('.dish')[2].querySelector('.thumb.up').click(); }
    if(step >= 7){ openSheet(); }
  }, 60);
})();
</script>
"""

def pick_week():
    rows = list(csv.DictReader(open("recipes.csv", encoding="utf-8")))
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    good = [r for r in rows
            if r["kid_friendly_estimated"] == "yes"
            and int(r["minutes_estimated"]) <= 45
            and "nut" not in r["ingredients"].lower()
            and len(r["name"]) < 30]
    good.sort(key=lambda r: r["name"])
    chosen = good[8:15]
    return [{"day": d, "id": r["id"]} for d, r in zip(days, chosen)]

def main():
    if not os.path.exists(CHROME):
        sys.exit("Chrome not found")
    os.makedirs(FRAMES, exist_ok=True)
    week = pick_week()
    html = open("index.html", encoding="utf-8").read()
    demo = html.replace("</body>", DRIVER.replace("__WEEK__", json.dumps(week)) + "</body>") \
        if "</body>" in html else html + DRIVER.replace("__WEEK__", json.dumps(week))
    open(".demo.html", "w", encoding="utf-8").write(demo)

    images = []
    try:
        for step, hold in STEPS:
            out = f"{FRAMES}/frame{step}.png"
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            f"--screenshot={out}", "--window-size=1512,1260",
                            "--virtual-time-budget=6000",
                            f"{BASE}/.demo.html?step={step}"],
                           check=True, capture_output=True, timeout=90)
            img = Image.open(out).convert("RGB")
            img = img.resize((1180, int(img.height * 1180 / img.width)), Image.LANCZOS)
            img = img.quantize(colors=128, method=Image.MEDIANCUT).convert("RGB")
            images.append((img, hold))
            print(f"  frame {step}: {img.size[0]}x{img.size[1]}")
    finally:
        if os.path.exists(".demo.html"):
            os.remove(".demo.html")

    frames = [i for i, _ in images]
    frames[0].save("meal-planner-demo.gif", save_all=True, append_images=frames[1:],
                   duration=[h for _, h in images], loop=0, optimize=True)
    kb = os.path.getsize("meal-planner-demo.gif") / 1024
    print(f"\nwrote meal-planner-demo.gif — {len(frames)} frames, {kb:.0f} KB")

if __name__ == "__main__":
    main()
