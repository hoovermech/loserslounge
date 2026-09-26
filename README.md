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
