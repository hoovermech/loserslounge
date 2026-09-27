# The Oracle Laughs Last — Simple League Site

A tiny static fantasy-football league site.

## Run locally
cd oracle_league_site
python -m http.server 8080

Then open http://localhost:8080

## Files
- index.html
- manifesto.html — the mostly static Oracle Manifesto, linked from League HQ
- styles.css
- app.js
- league_data.json

Later, the Sleeper/Work workflow can overwrite league_data.json automatically.
No database is required for the MVP.

## Automatic Sleeper refresh on GitHub Pages

Upload `update_from_sleeper.py` and `.github/workflows/update-site.yml` to the
repository in addition to the site files. GitHub's web upload may omit a
hidden `.github` folder: create the workflow via **Add file → Create new file**
and enter `.github/workflows/update-site.yml` as the filename, then paste it.

In **Settings → Pages → Build and deployment**, change Source from
**Deploy from a branch** to **GitHub Actions**. Keep the existing custom domain
`loserslounge.ca` in Pages settings. GitHub's branch-based Pages setup may
have created a `CNAME` file; retain it in the repository. The workflow copies
it into the deployed site when present.

Run **Actions → Refresh Oracle site → Run workflow** once and check the job
result and live site. Subsequent scheduled refreshes run four times a day,
subject to GitHub scheduling delays. Pushes to main also trigger deployment.
The updater reads only public Sleeper data, needs no API key, and fails closed
on malformed/incomplete matchups rather than publishing partial standings.

Standings, records, team names and weekly matchup scores refresh. The Oracle's
Latest Word, Week 2 Awards, Hall of Shame and Manifesto remain editorial and
should be updated manually. Existing manager notes are kept until a manager's
record changes; then the dated note is cleared to avoid stale claims. During
an offseason or an empty Sleeper week the scheduled job may fail safely and
leave the last published site in place.
