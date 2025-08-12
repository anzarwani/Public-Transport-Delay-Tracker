def load_vehicle_position(session, vehicle_data, model):
    
    records = [model(**v) for v in vehicle_data]
    
    session.bulk_save_objects(records)
    
    session.commit()
    