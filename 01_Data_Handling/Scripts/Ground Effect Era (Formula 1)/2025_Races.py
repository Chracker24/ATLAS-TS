import pandas as pd
import fastf1
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_ROOT = SCRIPT_DIR.parents[1]

cache_dir = DATA_ROOT / "Scripts" / "cache"
cache_dir.mkdir(parents=True, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

schedule = fastf1.get_event_schedule(2025)
listOfRaces = schedule["Country"].tolist()

cols = [
    "Driver",
    "LapTime",
    "LapNumber",
    "Stint",
    "Sector1Time",
    "Sector2Time",
    "Sector3Time",
    "Compound",
    "Team",
    "Deleted",
]

Season_Data2025 = []

logging.getLogger("fastf1").setLevel(logging.ERROR)
for i in range(len(listOfRaces)):
    session = fastf1.get_session(2025, listOfRaces[i], "R")
    session.load(laps=True, telemetry=False, weather=False)
    laps = session.laps
    Race_Data = laps[cols].copy()
    Race_Data = Race_Data.dropna(subset=["LapTime"]).copy()
    Race_Data["Season"] = 2025
    Race_Data["Race"] = listOfRaces[i]
    Race_Data[["LapTime","Sector1Time","Sector2Time","Sector3Time"]] = Race_Data[["LapTime","Sector1Time","Sector2Time","Sector3Time"]].apply(lambda x : x.dt.total_seconds())
    Race_Data = Race_Data[Race_Data["Deleted"]==False].copy()

    Season_Data2025.append(Race_Data)
    print(f"Race {i+1} Done")

season_2025 = pd.concat(Season_Data2025, ignore_index=True)

season_2025 = season_2025.sort_values("LapNumber").reset_index(drop=True)

archive_dir = DATA_ROOT / "Data" / "Archive"

archive_dir.mkdir(parents=True, exist_ok=True)

season_2025.to_csv(
    archive_dir / "season_2025.csv",
    index=False
)
print("Done")
