import yaml
from datetime import datetime
from src.db import get_engine, get_session
from src.extractor import fetch_raw_vehicle_feed, save_bronze
from src.transformer import parse_bronze_to_silver, save_silver
from src.aggregator import aggregate_delay_stats
from src.logger import setup_logger
from src.models import Base

def run_pipeline():
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    logger = setup_logger(config["logging"]["level"])
    engine = get_engine(config["database"]["url"])
    Base.metadata.create_all(engine)
    session = get_session(engine)

    vehicle_feed_url = config["api"]["vehicle_positions_url"]

    try:
        raw_feed = fetch_raw_vehicle_feed(vehicle_feed_url)
        logger.info(f"Fetched raw feed at {datetime.now()}")

        bronze_id = save_bronze(session, raw_feed)
        logger.info(f"Saved bronze record with ID {bronze_id}")

        vehicles = parse_bronze_to_silver(raw_feed)
        save_silver(session, vehicles)
        logger.info(f"Saved to Silver Layer")

        aggregate_delay_stats(session)
        logger.info("Gold delay stats aggregated")

    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")

    finally:
        session.close()

if __name__ == "__main__":
    run_pipeline()
