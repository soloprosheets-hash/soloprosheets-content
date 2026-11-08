# Carousel creative director (used by the content agent)

The owner's skill **Social Carousel Creative Director** is the source of these rules. If the run can load it
(`Skill` tool, name `social-carousel-creative-director`, possibly prefixed `anthropic-skills:`), load it first and
follow it. Either way, follow this file: it applies the skill to SoloPro Sheets and the repo's renderer.
Its limits always apply: no new paid tools, no invented facts, numbers, quotes or results.

## 1. Brief (write it down before any copy)

- Audience: a solo lash or brow artist running her own chair (see `content-plan.md` Voice).
- Today's topic row: keyword, title, angle, link.
- Her problem / misconception in one line.
- ONE takeaway. ONE intended response: **save** (reference/checklist/formula), **share** (relatable truth),
  **comment** (question/self-check) or **click** (tool). Pick one; it drives the hook, the layouts and the CTA.

## 2. Pick a fresh angle and shape

Read the last 7 rows of `creative-log.csv`. Today's post must differ from the previous **2 posts** in angle
AND from the previous **3** in `theme` and cover style (`type` / `number` / `story`), and must not reuse a hook
pattern from the last 7.

Angles: `myth-vs-reality` · `mistake-fix` · `formula` · `worked-example` · `checklist-audit` · `story-reveal` ·
`comparison` · `step-guide` · `diagnosis` (signs you…) · `self-check` (score yourself) · `framework` · `tool-tour`.
`tool-tour` (product showcase) at most once a week.

Hook patterns (log one): `direct-claim` ("Your refill price is probably a guess") · `number` ("9 costs…") ·
`story` ("She didn't leave because of your lashes") · `question` · `contrast` ("Busy diary, small profit?") ·
`mistake` ("Stop copying…") · `myth`.

Slide count: as many as the idea needs, **5–8**. Every slide adds something new. Cut filler.

## 3. Write the swipe journey

Cover → context (why it matters) → development (the useful part) → payoff (reveal, example, rule) → action.
- Cover: concrete, specific to lash/brow techs, readable in 2 seconds (title ≤ 10 words, sub ≤ 12).
  No "You won't believe", "Ultimate guide", "Stop scrolling". Never promise more than the post delivers.
- One idea per slide. Short sentences. Concrete over vague (€35, 50 minutes, 21 days).
- Use `*word*` to highlight one key word on the cover or a statement slide (max one per slide).
- Numbers: either from the owner's product (e.g. tracker defaults), or a clearly labelled example
  (`example` layout says "Example numbers"), or a verified fact with `source`. Otherwise don't use a number.
  Never income promises, client results, testimonials, or "most lash techs…" statistics without a source.
- CTA fits the value: a pricing post → "Get the free calculator"; a tracking post → "See the tracker";
  a self-check post can end on the question plus the tool. Do not write "Link in bio" in slide text:
  the renderer adds it on Instagram and the store URL on TikTok.

## 4. Art direction (renderer layouts)

Layouts: `cover` `statement` `number` `steps` `checklist` `compare` `mistake` `formula` `question` `example`
`summary` `cta` (`text` only as a last resort). Rules:
- Never two identical layouts in a row; at least **4 different layouts** per carousel.
- Max 2 "list" layouts (`steps`, `checklist`) per carousel.
- Rotate `theme` (`teal`, `mint`, `cream`) between posts; it sets which slides are dark/light/amber.
  Only override `tone` on a slide for a clear reason (e.g. a reveal).
- Lists: 2–6 items, each ≤ 7 words where possible.
- Word budget per slide: cover ≤ 18, statement ≤ 22, others ≤ 35.

## 5. Quality control (before anything goes to Buffer)

1. Render with `--sheet`. Fix every renderer warning (overflow, shrink below 85 %, too many words).
2. Look at `sheet.png` (all slides) and `tiktok/slide-1.png`. Check: legible at phone size, nothing cut off,
   no awkward single word on its own line in a title, contrast fine, layouts varied.
3. Score 1–5 and write the scores into the run log:
   `hook` · `relevance` · `usefulness` · `flow` · `visual` · `readability` · `accuracy` · `originality` · `cta`.
   - accuracy < 3 if any number/claim is not from the product, a labelled example, or a cited source.
   - originality < 3 if angle, hook pattern or cover style repeats the recent posts (see §2).
4. Any score < 3 → rewrite once and score again. Still < 3 → **do not create Buffer posts**; create an
   approval "Review carousel: <title>" with the failing scores and the reason, log status `held`.

## 6. Captions

- Instagram: line 1 repeats the hook in different words; 3–6 short lines with the gist (so it's useful
  without swiping); a save/share/comment prompt that matches the intended response (one line, natural,
  not "like & follow"); the offer line ending "Link in bio"; 5–7 hashtags chosen for this topic.
- TikTok: shorter (2–4 lines), same idea, ends "Free calculator: payhip.com/soloprosheets" (or the tracker line
  when the CTA is the tracker: "Tracker: payhip.com/soloprosheets"), 4–5 hashtags.
- Alt text per slide: the slide's text in one plain sentence.
- Hashtag pool (pick by topic, don't paste all): #lashtech #lashartist #lashbusiness #lashextensions
  #lashtechtips #browartist #browlamination #beautybusiness #salonowner #smallbusinesstips #selfemployed
  #lashlife #beautyentrepreneur.

## 7. Learn from results

The weekly analyst writes `reports/<date>.md` with "post more of" topics and, once there is data,
"creative notes" (which angles, hook patterns, layouts and slide counts got the most saves/shares per post).
Prefer what the latest report says works, but keep at least 1 post in 3 trying something different,
so the data keeps learning. Small samples (under 5 posts per group) are a hint, not a rule.
