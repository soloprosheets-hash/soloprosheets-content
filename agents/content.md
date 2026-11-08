# Content agent (daily)

Agent id: `content`. Workflow name: `Daily posts`. Read `agents/common.md` first and follow it.

## Mode

`DRAFT_MODE = true` — posts are saved as Buffer drafts for the owner to approve.
Only the owner changes this line (to `false`, which queues posts automatically).

## Steps

1. Read `content-plan.md` (links, voice, topics), `post-log.csv`, the last 7 rows of `creative-log.csv`,
   the newest file in `reports/` (if any) and `agents/creative-director.md`.
   Load the owner's skill **social-carousel-creative-director** with the `Skill` tool if it is available
   (try `anthropic-skills:social-carousel-creative-director`, then `social-carousel-creative-director`);
   if neither loads, `agents/creative-director.md` alone is enough. Note in the run log which one was used.
2. Pick the first topic, top to bottom, whose `#` has no `ok` row in `post-log.csv` in the last 30 days and whose
   Link key has a live URL. If the latest weekly report lists "post more of" topics, prefer those.
3. For each channel, `list_posts` with status `scheduled` (and `draft` when in draft mode). If that channel
   already has 10, mark it `skipped` for today.
4. **Creative.** Follow `agents/creative-director.md` §1–§4: write the brief, choose angle / hook pattern /
   theme / cover style that differ from recent posts, and write the slides (5–8) using the renderer layouts.
   Also write the Pinterest pin: `kicker`, `title` (≤ 100 characters, keyword near the start),
   3–4 `points`, `footer`; pin description 2–3 sentences; destination = the topic's link.
5. Write the spec to `/tmp/spec.json`:
   `{"theme": ..., "pin": {...}, "slides": [{"layout": ..., ...}, ...]}` (fields per layout: see the top of
   `tools/render.py`; worked examples in `tools/examples/` — use them for the format only, never copy their
   copy or slide order). Render:
   `python3 tools/render.py /tmp/spec.json images/<YYYY-MM-DD> --sheet`
   This writes `pin.png`, `slide-N.png` (Instagram 1080×1350), `tiktok/slide-N.png` (TikTok 1080×1920 with the
   store URL on the last slide) and `sheet.png`. Needs `pip install playwright` only if the import fails
   (Chromium is preinstalled).
6. **Quality control** — `agents/creative-director.md` §5. Fix warnings, look at `sheet.png`, score, rewrite
   once if needed. If it still fails: do not create Buffer posts; create the "Review carousel" approval,
   log `held` in `post-log.csv` for each channel, and go to step 10.
7. Commit the images except `sheet.png` (`git add images/<date> ':!images/<date>/sheet.png'`, message
   "Post images <date>") and push. Wait 5 seconds, then check one raw URL returns HTTP 200.
8. Create the Buffer posts (`schedulingType: automatic`; `saveToDraft: true` if DRAFT_MODE else
   `mode: addToQueue`), captions per `agents/creative-director.md` §6:
   - **Instagram**: `images/<date>/slide-N.png` (alt text per slide),
     `metadata.instagram = {type:"post", shouldShareToFeed:true, isAiGenerated:true}`.
   - **TikTok**: `images/<date>/tiktok/slide-N.png` and the TikTok caption (store URL as text; the account is
     personal, so it has no clickable bio link).
   - **Pinterest**: `pin.png`, `metadata.pinterest = {title, url:<topic link>, boardServiceId}`. Get boards with
     `get_channel`; pick the board whose name best matches the pillar. If there are no boards, skip Pinterest,
     log `skipped: no Pinterest boards`, and create an approval titled "Create Pinterest boards" (only if no
     pending one exists).
9. Append one line per channel to `post-log.csv`: `date,channel,topic#,status,buffer_post_id,image_url,error`.
10. Append one line to `creative-log.csv` (also for `held` posts):
    `date,topic,angle,hook_type,hook,theme,cover_style,layouts,slides,cta,intended_response,qc_min,qc_scores,status`
    — `layouts` joined with `|`, `qc_scores` as `hook4|relevance5|...`, `hook` = the cover title in quotes.
    Commit and push.
11. Finish the run record (common.md step 4; include the QC scores and skill-or-fallback in `log`) and add an
    `events` doc per post: "Draft ready: <title> (<channel>)", "Queued: ..." or "Held for review: ...".
