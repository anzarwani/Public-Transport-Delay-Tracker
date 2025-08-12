import requests
from datetime import datetime
from google.transit import gtfs_realtime_pb2

def fetch_raw_vehicle_feed(url):
    response = requests.get(url)
    response.raise_for_status()
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    return feed

def save_bronze(session, feed):
    
    from src.models import BronzeVehicleFeed

    raw_bytes = feed.SerializeToString()
    # convert bytes to hex string for JSON-serializable storage
    raw_hex = raw_bytes.hex()

    record = BronzeVehicleFeed(
        fetched_at=datetime.now(),
        raw_feed=raw_hex
    )
    session.add(record)
    session.commit()
    return record.id
