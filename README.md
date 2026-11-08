# SoloPro Sheets content

Working files for the SoloPro Sheets automation agents.

- `images/YYYY-MM-DD/` – post images the content agent renders (served via raw.githubusercontent.com so Buffer can fetch them)
- `ready/` – new trackers the product agent builds, waiting for a human test and Payhip listing
- `content-plan.md` – topics, keywords and the Payhip link each post points to
- `post-log.csv` – one line per post attempt
- `creative-log.csv` – angle, hook, layouts and quality scores of each carousel (used to avoid repeats and learn what works)
- `agents/creative-director.md` – how carousels are written, designed and quality-checked
- `tools/render.py` – free local renderer (HTML/CSS → PNG); `tools/fonts/` are open-licence fonts (Inter, Lora; SIL OFL)

Never put customer names, emails or order details in this repository: it is public.
