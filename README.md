# GAA Clubs Nationwide GeoMap

This project generates geospatial visualizations of GAA clubs across Ireland:
- Interactive map (Folium) with marker sizing and color-coding by club size/performance
- Filters by province and league
- Optional GeoPandas plotting

## Quick start (Windows / PowerShell)
1. Create environment + install deps:
   \\\powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   \\\

2. Run the example map generator:
   \\\powershell
   python .\src\make_map.py
   \\\

Outputs:
- \outputs/maps/gaa_clubs_map.html\

## Data format
Place your club data in \data/raw/gaa_clubs.csv\ with columns:

- \club_name\
- \county\
- \province\ (Connacht/Leinster/Munster/Ulster)
- \league\ (e.g., Hurling/Football/Camogie/Ladies Football, etc.)
- \lat\, \lon\
- \members\ (numeric)
- \performance\ (numeric, e.g. 0100 or similar)

A small sample dataset is included to prove the pipeline works.
