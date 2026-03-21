import pandas as pd
import random
from datetime import datetime, timedelta

# ----------------------------
# Helper Functions
# ----------------------------
def random_date(start, end):
    """Generate random datetime between two dates"""
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

# ----------------------------
# Generate Zones
# ----------------------------
zone_names = [
    "Downtown", "Midtown", "Uptown", "Eastside", "Westside",
    "North End", "South End", "Harbor", "Financial District",
    "Chinatown", "Little Italy", "University", "Airport",
    "Industrial Park", "Suburb A", "Suburb B", "Suburb C",
    "Market District", "Old Town", "Tech Park"
]

cities = ["Toronto", "Vancouver", "Montreal", "Calgary"]
regions = ["Ontario", "British Columbia", "Quebec", "Alberta"]

zones = []
for i in range(1, 21):
    zones.append({
        "zone_id": i,
        "zone_name": zone_names[i-1],
        "city": random.choice(cities),
        "region": random.choice(regions)
    })

zones_df = pd.DataFrame(zones)

# ----------------------------
# Generate Couriers
# ----------------------------
vehicle_types = ["bike", "car", "scooter", "ebike"]
courier_statuses = ["active", "active", "active", "inactive"]  # Bias toward active

couriers = []
start_signup = datetime(2020, 1, 1)
end_signup = datetime(2024, 12, 31)

for i in range(1, 101):
    couriers.append({
        "courier_id": i,
        "courier_name": f"Courier_{i}",
        "vehicle_type": random.choice(vehicle_types),
        "signup_date": random_date(start_signup, end_signup).date(),
        "status": random.choice(courier_statuses)
    })

couriers_df = pd.DataFrame(couriers)

# ----------------------------
# Generate Deliveries
# ----------------------------
delivery_statuses = ["completed", "completed", "completed", "completed", "cancelled"]  # Bias toward completed

deliveries = []
start_orders = datetime(2024, 1, 1)
end_orders = datetime(2025, 1, 1)

for i in range(1, 1001):
    order_time = random_date(start_orders, end_orders)
    delivery_time_minutes = random.randint(15, 60)
    delivery_time = order_time + timedelta(minutes=delivery_time_minutes)
    
    deliveries.append({
        "delivery_id": i,
        "courier_id": random.randint(1, 100),
        "zone_id": random.randint(1, 20),
        "restaurant_id": random.randint(1, 200),
        "order_timestamp": order_time,
        "delivery_timestamp": delivery_time,
        "tip_amount": round(random.uniform(0, 15), 2),
        "distance_km": round(random.uniform(0.5, 12), 2),
        "status": random.choice(delivery_statuses)
    })

deliveries_df = pd.DataFrame(deliveries)

# ----------------------------
# Save CSV Files
# ----------------------------
zones_df.to_csv("raw_zones.csv", index=False)
couriers_df.to_csv("raw_couriers.csv", index=False)
deliveries_df.to_csv("raw_deliveries.csv", index=False)

print("✅ CSV files generated:")
print("  - raw_zones.csv (20 zones)")
print("  - raw_couriers.csv (100 couriers)")
print("  - raw_deliveries.csv (1000 deliveries)")