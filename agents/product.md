# Product builder (1st and 15th)

Agent id: `product`. Workflow name: `Build next tracker`. Read `agents/common.md` first and follow it.

## Steps

1. `ArtifactData query` collection `approvals` where `status == "approved"`, `requestedBy == "analyst"`, title starts with "Build next tracker", and no `executedAt`. If none: finish as `skipped` ("nothing approved to build") and exit.
2. Take the oldest. Build it in a scratch folder, modelled on `Lash-Brow-Business-Tracker.xlsx` structure (Start Here, Dashboard, Clients, Appointments/Jobs, Services, Expenses, Settings), with the niche's own services, terms and example rows. Formulas must work in Google Sheets and Excel: no XLOOKUP/FILTER/SORT/UNIQUE; MINIFS/MAXIFS written with the `_xlfn.` prefix. Recalculate with LibreOffice and fix every error. Fill a copy with ~100 sample rows and check the dashboard totals by hand on 2 months.
3. Make: the .xlsx, a quick-start PDF, 3 preview images (cover, dashboard, clients) at 1600×1200, and a `listing.md` with title, price, description and FAQ in the same style as the Lash & Brow listing.
4. Commit only `ready/<niche>/listing.md` and the 3 preview images to the repo (public). **Do not commit the .xlsx or PDF** — the paid file must not be public. Instead attach the .xlsx and PDF to the run's final message so the owner can download them.
5. Create an approval: "List on Payhip: <niche> tracker" with the listing summary. Set `executedAt` on the build approval. Add an `events` doc "New product ready to test". Finish the run record.
