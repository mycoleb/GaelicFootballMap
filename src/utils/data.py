from __future__ import annotations
from pathlib import Path
import pandas as pd

REQUIRED_COLS = [
    "club_name", "county", "province", "league",
    "lat", "lon", "members", "performance"
]

def load_clubs(csv_path: str | Path) -> pd.DataFrame:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f\"Missing data file: {csv_path}\")

    df = pd.read_csv(csv_path)

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f\"CSV missing required columns: {missing}\")

    # Basic cleanup
    df["province"] = df["province"].astype(str).str.strip()
    df["league"] = df["league"].astype(str).str.strip()
    df["members"] = pd.to_numeric(df["members"], errors="coerce")
    df["performance"] = pd.to_numeric(df["performance"], errors="coerce")
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

    df = df.dropna(subset=["lat", "lon"])
    return df
