from datetime import datetime

def parse_bronze_to_silver(feed):
    vehicles = []
    for entity in feed.entity:
        vehicle = entity.vehicle
        if not vehicle:
            continue
        pos = vehicle.position
        trip = vehicle.trip
        vehicles.append({
            "vehicle_id": vehicle.vehicle.id if vehicle.vehicle else None,
            "route_id": trip.route_id if trip else None,
            "timestamp": datetime.fromtimestamp(vehicle.timestamp) if vehicle.timestamp else None,
            "latitude": pos.latitude if pos else None,
            "longitude": pos.longitude if pos else None,
            "delay": vehicle.delay if hasattr(vehicle, 'delay') else None,
            "occupancy_status": vehicle.occupancy_status if hasattr(vehicle, 'occupancy_status') else None,
            "trip_id": trip.trip_id if trip else None
        })
        
    vehicles = [v for v in vehicles if v["vehicle_id"] and v["route_id"] and v["timestamp"]]
    return vehicles


def save_silver(session, vehicles):
    from src.models import SilverVehiclePosition

    records = []
    for v in vehicles:
        record = SilverVehiclePosition(
            vehicle_id = v.get("vehicle_id"),
            route_id = v.get("route_id"),
            timestamp = v.get("timestamp"),
            latitude = v.get("latitude"),
            longitude = v.get("longitude"),
            delay = v.get("delay"),
            occupancy_status = v.get("occupancy_status"),
            trip_id = v.get("trip_id"),
        )
        records.append(record)

    session.bulk_save_objects(records)
    session.commit()

