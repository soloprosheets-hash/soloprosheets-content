# Content agent (daily)

Agent id: `content`. Workflow name: `Daily posts`. Read `agents/common.md` first and follow it.

## Mode

`DRAFT_MODE = true` — posts are saved as Buffer drafts for the owner to approve.
Only the owner changes this line (to `false`, which queues posts automatically).

## Steps

1. Read `content-plan.md` (links, voice, topics) and `post-log.csv`.
2. Pick the first topic, top to bottom, whose `#` has no `ok` row in `post-log.csv` in the last 30 days and whose Link key has a live URL. If the latest weekly report (`reports/` newest file) lists "post more of" topics, prefer those.
3. For each channel, `list_posts` with status `scheduled` (and `draft` when in draft mode). If that channel already has 10, mark it `skipped` for today.
4. Write the copy:
   - **Pin**: title ≤ 100 characters, keyword near the start; description 2–3 sentences; destination = the topic's link.
   - **Carousel** (Instagram + TikTok): 5 slides. Slide 1 = hook question; slides 2–4 = the tip in short steps; slide 5 = "Get the free calculator" or "See the full tracker" + "Link in bio". Body ≤ 25 words per slide.
   - **Caption**: 4–8 short lines, ends with the offer, then 5–8 hashtags. Instagram ends the offer with "Link in bio". **TikTok** is a personal account with no clickable bio link (business switch needs company documents), so its caption ends with "Free calculator: payhip.com/soloprosheets" instead, and its last slide's footer says "payhip.com/soloprosheets" rather than "Link in bio": render the same 5 slides a second time with `"cta": "payhip.com/soloprosheets"` on slide 5 and "Link in bio" removed from its body text into `images/<date>/tiktok/`, and use those 5 images for TikTok. Hashtags from: #lashtech #lashartist #lashbusiness #lashextensions #browartist #beautybusiness #lashtechtips #salonowner #smallbusinesstips #selfemployed.
5. Write the spec to `/tmp/spec.json` in this shape and render:
   `{"pin":{"kicker":..., "title":..., "points":[3-4 short lines], "footer":...}, "slides":[{"title":..,"body":..} ×5]}`
   `python3 tools/render.py /tmp/spec.json images/<YYYY-MM-DD>` (needs `pip install playwright` only if import fails; Chromium is preinstalled).
   Look at `pin.png` and `slide-1.png` once. If text is cut off or overlaps, shorten the copy and render again (max 2 tries).
6. Commit the images (`git add images/<date>`, message "Post images <date>") and push. Wait 5 seconds, then check one raw URL returns HTTP 200.
7. Create the Buffer posts (`schedulingType: automatic`; `saveToDraft: true` if DRAFT_MODE else `mode: addToQueue`):
   - **Instagram**: the 5 slide images (alt text = slide text), `metadata.instagram = {type:"post", shouldShareToFeed:true, isAiGenerated:true}`.
   - **TikTok**: the same 5 images and caption.
   - **Pinterest**: `pin.png`, `metadata.pinterest = {title, url:<topic link>, boardServiceId}`. Get boards with `get_channel`; pick the board whose name best matches the pillar. If there are no boards, skip Pinterest, log `skipped: no Pinterest boards`, and create an approval titled "Create Pinterest boards" (only if no pending one exists).
8. Append one line per channel to `post-log.csv`: `date,channel,topic#,status,buffer_post_id,image_url,error`. Commit and push.
9. Finish the run record (common.md step 4) and add an `events` doc per post: "Draft ready: <title> (<channel>)" or "Queued: ...".
