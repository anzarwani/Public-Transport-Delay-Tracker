from sqlalchemy import func

def aggregate_delay_stats(session):
    from src.models import SilverVehiclePosition, GoldRouteDelayStat
    
    session.query(GoldRouteDelayStat).delete()

    results = session.query(
        SilverVehiclePosition.route_id,
        func.date_trunc('hour', SilverVehiclePosition.timestamp).label("hour"),
        func.avg(SilverVehiclePosition.delay).label("avg_delay"),
        func.max(SilverVehiclePosition.delay).label("max_delay"),
        func.count(SilverVehiclePosition.delay).label("count_delays")
    ).group_by("route_id", "hour").all()

    gold_records = []
    for r in results:
        gold_records.append(GoldRouteDelayStat(
            route_id=r.route_id,
            hour=r.hour,
            avg_delay=r.avg_delay,
            max_delay=r.max_delay,
            count_delays=r.count_delays
        ))

    session.bulk_save_objects(gold_records)
    session.commit()
    
    
