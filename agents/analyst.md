# Weekly analyst (Mondays)

Agent id: `analyst`. Workflow name: `Weekly report`. Read `agents/common.md` first and follow it.

## Steps

1. Buffer: `get_aggregated_post_metrics` for the last 7 days and the 7 days before (org from common.md), and `list_posts` status `sent` with `includeMetrics: true` for the last 14 days. Also `list_posts` status `error`.
2. Dashboard: `ArtifactData list` collections `sales` (owner-entered weekly Payhip totals), `runs` (last 7 days), `approvals` (pending).
3. Repo: `post-log.csv`, `content-plan.md`.
4. Work out, using only these numbers (never estimate missing ones; write "no data"):
   - posts published per channel, views, engagement rate, best 3 and worst 3 posts with their topic #;
   - which pillar and which title style got the most views per post;
   - store visitors, orders, revenue, email sign-ups and conversion from `sales` (if logged);
   - failed or skipped runs and why.
5. Write `reports/<YYYY-MM-DD>.md`: 5 sections — Headline numbers · What worked · What didn't · Next week (3 concrete changes) · Problems. Under "Next week" add a line `post more of: <topic numbers>`.
6. Update `content-plan.md` only by: reordering unposted topics to put the best pillar first, and appending up to 5 new topics at the bottom in the same table format (next free `#`). Never edit links or delete posted topics.
7. Product research, first Monday of each month only: web search what solo beauty and home-service pros ask about money/admin; propose ONE next niche tracker by creating an approval: title "Build next tracker: <niche>", detail = why (with source links) and the price.
8. Commit and push. Add an `events` doc "Weekly report ready" with the 3 headline numbers. Finish the run record.
