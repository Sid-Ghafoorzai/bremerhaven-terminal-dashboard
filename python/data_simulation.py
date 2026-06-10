import pandas as pd
import numpy as np
from pathlib import Path
from datetime import timedelta

np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# -------------------------
# Dimension tables
# -------------------------

shipping_lines = pd.DataFrame({
    "ShippingLine_ID": [1, 2, 3, 4, 5],
    "ShippingLine_Name": ["Maersk", "MSC", "Hapag-Lloyd", "CMA CGM", "ONE"]
})

terminals = pd.DataFrame({
    "Terminal_ID": [1],
    "Port_ID": [1],
    "Terminal_Name": ["Bremerhaven CT1"]
})

ports = pd.DataFrame({
    "Port_ID": [1],
    "Port_Name": ["Bremerhaven"]
})

berths = pd.DataFrame({
    "Berth_ID": [1, 2, 3],
    "Terminal_ID": [1, 1, 1],
    "Berth_Name": ["B1", "B2", "B3"]
})

cranes = pd.DataFrame({
    "Crane_ID": [1, 2, 3, 4, 5],
    "Terminal_ID": [1, 1, 1, 1, 1],
    "Crane_Name": ["C1", "C2", "C3", "C4", "C5"],
    "Max_Moves_Per_Hour": [30, 32, 28, 31, 29]
})

container_types = pd.DataFrame({
    "ContainerType_ID": [1, 2, 3, 4],
    "Size": ["20ft", "40ft", "40ft Reefer", "20ft Hazardous"],
    "Reefer": [0, 0, 1, 0],
    "Hazardous": [0, 0, 0, 1]
})

vessels = pd.DataFrame({
    "Vessel_ID": range(1, 51),
    "Vessel_Name": [f"Vessel_{i:02d}" for i in range(1, 51)],
    "Vessel_Type": ["Container"] * 50,
    "Capacity_TEU": np.random.choice([5000, 8000, 12000, 15000, 18000], 50)
})

dates = pd.DataFrame({
    "Date": pd.date_range("2024-01-01", "2025-12-31", freq="D")
})
dates["Year"] = dates["Date"].dt.year
dates["Month"] = dates["Date"].dt.month
dates["Month_Name"] = dates["Date"].dt.month_name()
dates["Quarter"] = dates["Date"].dt.quarter
dates["Week"] = dates["Date"].dt.isocalendar().week
dates["IsWeekend"] = dates["Date"].dt.weekday >= 5

# -------------------------
# Fact_VesselCalls
# -------------------------

n_calls = 500

arrival_dates = pd.to_datetime(
    np.random.choice(dates["Date"], size=n_calls)
).sort_values()

vessel_calls = []

for i, arrival in enumerate(arrival_dates, start=1):
    vessel_id = np.random.randint(1, 51)
    capacity = vessels.loc[vessels["Vessel_ID"] == vessel_id, "Capacity_TEU"].iloc[0]

    total_moves = int(np.random.normal(capacity * 0.025, capacity * 0.008))
    total_moves = max(100, min(total_moves, 700))

    import_moves = int(total_moves * np.random.uniform(0.45, 0.60))
    export_moves = total_moves - import_moves

    handling_hours = total_moves / np.random.uniform(55, 95)
    waiting_hours = np.random.uniform(2, 18)

    arrival_dt = arrival + pd.to_timedelta(np.random.randint(0, 24), unit="h")
    departure_dt = arrival_dt + timedelta(hours=waiting_hours + handling_hours)

    scheduled_departure = departure_dt - timedelta(hours=np.random.uniform(-8, 10))
    delay_minutes = max(0, int((departure_dt - scheduled_departure).total_seconds() / 60))

    vessel_calls.append({
        "VesselCall_ID": i,
        "Vessel_ID": vessel_id,
        "ShippingLine_ID": np.random.randint(1, 6),
        "Terminal_ID": 1,
        "Berth_ID": np.random.randint(1, 4),
        "ArrivalDateTime": arrival_dt,
        "DepartureDateTime": departure_dt,
        "ScheduledDeparture": scheduled_departure,
        "Total_Moves": total_moves,
        "Import_Moves": import_moves,
        "Export_Moves": export_moves,
        "Delay_Minutes": delay_minutes
    })

fact_vessel_calls = pd.DataFrame(vessel_calls)

# -------------------------
# Fact_ContainerMoves
# -------------------------

container_rows = []
container_id = 1

for _, call in fact_vessel_calls.iterrows():
    for _ in range(call["Total_Moves"]):
        container_type = np.random.choice([1, 2, 3, 4], p=[0.35, 0.50, 0.10, 0.05])
        teu = 1 if container_type in [1, 4] else 2

        move_type = np.random.choice(
            ["Import", "Export", "Transshipment"],
            p=[0.48, 0.42, 0.10]
        )

        move_date = call["ArrivalDateTime"].date() + timedelta(days=np.random.randint(0, 3))

        container_rows.append({
            "Container_ID": f"C{container_id:07d}",
            "VesselCall_ID": call["VesselCall_ID"],
            "ContainerType_ID": container_type,
            "Move_Type": move_type,
            "Move_Date": move_date,
            "Dwell_Time_Days": np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9], p=[0.05, 0.12, 0.20, 0.22, 0.16, 0.10, 0.07, 0.05, 0.03]),
            "TEU_Value": teu,
            "Weight_Tons": round(np.random.uniform(8, 28), 2)
        })

        container_id += 1

fact_container_moves = pd.DataFrame(container_rows)

# -------------------------
# Fact_CraneOperations
# -------------------------

crane_rows = []
operation_id = 1

for _, call in fact_vessel_calls.iterrows():
    cranes_used = np.random.choice(cranes["Crane_ID"], size=np.random.randint(2, 5), replace=False)
    moves_split = np.random.dirichlet(np.ones(len(cranes_used))) * call["Total_Moves"]

    for crane_id, moves in zip(cranes_used, moves_split):
        moves = int(moves)
        productivity = np.random.uniform(22, 34)
        hours = round(moves / productivity, 2)

        crane_rows.append({
            "CraneOperation_ID": operation_id,
            "VesselCall_ID": call["VesselCall_ID"],
            "Crane_ID": crane_id,
            "Operating_Hours": hours,
            "Moves_Completed": moves
        })

        operation_id += 1

fact_crane_operations = pd.DataFrame(crane_rows)

# -------------------------
# Export CSVs
# -------------------------

tables = {
    "Dim_Port": ports,
    "Dim_Terminal": terminals,
    "Dim_Berth": berths,
    "Dim_Crane": cranes,
    "Dim_ContainerType": container_types,
    "Dim_ShippingLine": shipping_lines,
    "Dim_Vessel": vessels,
    "Dim_Date": dates,
    "Fact_VesselCalls": fact_vessel_calls,
    "Fact_ContainerMoves": fact_container_moves,
    "Fact_CraneOperations": fact_crane_operations,
}

for name, df in tables.items():
    df.to_csv(DATA_DIR / f"{name}.csv", index=False)

print("Data generated successfully.")
print(f"Vessel calls: {len(fact_vessel_calls)}")
print(f"Container moves: {len(fact_container_moves)}")
print(f"Crane operations: {len(fact_crane_operations)}")