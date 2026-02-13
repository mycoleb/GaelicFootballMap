from __future__ import annotations

from pathlib import Path
import math
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from branca.colormap import linear

from utils.data import load_clubs

ROOT = Path(__file__).resolve().parents[1]
DATA_CSV = ROOT / "data" / "raw" / "gaa_clubs.csv"
OUT_HTML = ROOT / "outputs" / "maps" / "gaa_clubs_map.html"
print("start of file")
def radius_from_members(members: float) -> float:
    print("start of radius_from_members")
    # Smoothly scale marker radius; tweak to taste.
    # Ensures small clubs still visible.
    if members is None or (isinstance(members, float) and math.isnan(members)):
        return 6
    return max(5, min(22, 4 + math.sqrt(float(members)) / 3))

def build_map(df: pd.DataFrame) -> folium.Map:
    
    print("entering build_map function")
    # Center map on median point (robust-ish)
    center_lat = float(df["lat"].median())
    center_lon = float(df["lon"].median())

    m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles="OpenStreetMap")

    # Color scale for performance
    perf = df["performance"].dropna()
    vmin = float(perf.min()) if len(perf) else 0.0
    vmax = float(perf.max()) if len(perf) else 100.0
    colormap = linear.YlGnBu_09.scale(vmin, vmax)
    colormap.caption = "Performance (higher = better)"
    colormap.add_to(m)

    # Marker clusters per filter group (Province x League)
    # This gives you "filters" via layer control toggles.
    for (province, league), g in df.groupby(["province", "league"], dropna=False):
        layer_name = f"{province}  {league}"
        fg = folium.FeatureGroup(name=layer_name, show=False)
        cluster = MarkerCluster()

        for _, r in g.iterrows():
            members = r.get("members")
            performance = r.get("performance")
            color = colormap(performance) if pd.notna(performance) else "#666666"
            rad = radius_from_members(members)

            popup_html = f"""
            <div style="font-family: Arial; font-size: 13px;">
              <b>{r['club_name']}</b><br/>
              County: {r['county']}<br/>
              Province: {r['province']}<br/>
              League: {r['league']}<br/>
              Members: {int(members) if pd.notna(members) else 'NA'}<br/>
              Performance: {performance if pd.notna(performance) else 'NA'}
            </div>
            """

            folium.CircleMarker(
                location=[float(r["lat"]), float(r["lon"])],
                radius=rad,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.85,
                weight=2,
                popup=folium.Popup(popup_html, max_width=320),
                tooltip=f"{r['club_name']} ({r['county']})",


            ).add_to(cluster)

        cluster.add_to(fg)
        fg.add_to(m)

    # Optional: also show an "All clubs" layer by default
    all_fg = folium.FeatureGroup(name="All clubs", show=True)
    all_cluster = MarkerCluster()

    for _, r in df.iterrows():
        members = r.get("members")
        performance = r.get("performance")
        color = colormap(performance) if pd.notna(performance) else "#666666"
        rad = radius_from_members(members)

        popup_html = f"""
        <div style="font-family: Arial; font-size: 13px;">
          <b>{r['club_name']}</b><br/>
          County: {r['county']}<br/>
          Province: {r['province']}<br/>
          League: {r['league']}<br/>
          Members: {int(members) if pd.notna(members) else 'NA'}<br/>
          Performance: {performance if pd.notna(performance) else 'NA'}
        </div>
        """

        folium.CircleMarker(
            location=[float(r["lat"]), float(r["lon"])],
            radius=rad,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            weight=2,
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"{r['club_name']} ({r['county']})",

        ).add_to(all_cluster)

    all_cluster.add_to(all_fg)
    all_fg.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    return m

def main() -> None:
    print("start of main")
    df = load_clubs(DATA_CSV)

    # Basic sanity checks
    if df.empty:
        raise RuntimeError("No rows found after loading/cleaning the CSV.")

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    m = build_map(df)
    m.save(str(OUT_HTML))
    print(f"Saved map to: {OUT_HTML}")
print("reached end of file")
if __name__ == "__main__":
    main()
