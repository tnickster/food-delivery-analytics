import pandas as pd
import random
import logging
import argparse
from datetime import datetime, timedelta
from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def random_date(start, end):
    """Generate random datetime between two dates"""
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

def generate_zones(num_rows):
    """Generate zone data"""
    logger.info(f"Generating {num_rows} zones...")
    
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
    for i in range(1, num_rows + 1):
        zones.append({
            "zone_id": i,
            "zone_name": zone_names[(i-1) % len(zone_names)],
            "city": random.choice(cities),
            "region": random.choice(regions)
        })
    
    logger.info(f"Generated {len(zones)} zones")
    return pd.DataFrame(zones)

def generate_couriers(num_rows):
    """Generate courier data"""
    logger.info(f"Generating {num_rows} couriers...")
    
    vehicle_types = ["bike", "car", "scooter", "ebike"]
    courier_statuses = ["active", "active", "active", "inactive"]
    
    start_signup = datetime(2020, 1, 1)
    end_signup = datetime(2024, 12, 31)
    
    couriers = []
    for i in range(1, num_rows + 1):
        couriers.append({
            "courier_id": i,
            "courier_name": f"Courier_{i}",
            "vehicle_type": random.choice(vehicle_types),
            "signup_date": random_date(start_signup, end_signup).date(),
            "status": random.choice(courier_statuses)
        })
    
    logger.info(f"Generated {len(couriers)} couriers")
    return pd.DataFrame(couriers)

def generate_deliveries(num_rows):
    """Generate delivery data"""
    logger.info(f"Generating {num_rows} deliveries...")
    
    delivery_statuses = ["completed", "completed", "completed", "completed", "cancelled"]
    
    start_orders = datetime(2024, 1, 1)
    end_orders = datetime(2025, 1, 1)
    
    deliveries = []
    for i in range(1, num_rows + 1):
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
    
    logger.info(f"Generated {len(deliveries)} deliveries")
    return pd.DataFrame(deliveries)

def load_to_bigquery(df, table_name, project_id, dataset_id):
    """Load dataframe to BigQuery"""
    try:
        logger.info(f"Loading data to {project_id}.{dataset_id}.{table_name}...")
        
        client = bigquery.Client(project=project_id)
        table_id = f"{project_id}.{dataset_id}.{table_name}"
        
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",  # Overwrite table
        )
        
        job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )
        
        job.result()  # Wait for job to complete
        
        logger.info(f"Successfully loaded {len(df)} rows to {table_name}")
        return True
        
    except Exception as e:
        logger.error(f"Error loading to BigQuery: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate and load food delivery data')
    parser.add_argument('--deliveries', type=int, default=1000, help='Number of deliveries to generate')
    parser.add_argument('--couriers', type=int, default=100, help='Number of couriers to generate')
    parser.add_argument('--zones', type=int, default=20, help='Number of zones to generate')
    parser.add_argument(
        '--project', 
        type=str, 
        default=os.getenv('PROJECT_ID', 'food-delivery-analytics-489100'),
        help='BigQuery project ID'
    )
    parser.add_argument(
        '--dataset', 
        type=str, 
        default=os.getenv('DATASET', 'raw_data'),
        help='BigQuery dataset ID'
    )
    
    args = parser.parse_args()
    
    logger.info("Starting data generation pipeline...")
    
    try:
        # Generate data
        zones_df = generate_zones(args.zones)
        couriers_df = generate_couriers(args.couriers)
        deliveries_df = generate_deliveries(args.deliveries)
        
        # Load to BigQuery
        load_to_bigquery(zones_df, 'raw_zones', args.project, args.dataset)
        load_to_bigquery(couriers_df, 'raw_couriers', args.project, args.dataset)
        load_to_bigquery(deliveries_df, 'raw_deliveries', args.project, args.dataset)
        
        logger.info("Pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()