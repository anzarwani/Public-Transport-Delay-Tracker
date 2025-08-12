from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, BigInteger

Base = declarative_base()

class BronzeVehicleFeed(Base):
    __tablename__ = "bronze_vehicle_feed"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fetched_at = Column(DateTime, nullable=False)
    raw_feed = Column(JSON, nullable=False)

class SilverVehiclePosition(Base):
    __tablename__ = "silver_vehicle_positions"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    vehicle_id = Column(String, nullable=False)
    route_id = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    delay = Column(Integer)
    occupancy_status = Column(String)
    trip_id = Column(String)

class GoldRouteDelayStat(Base):
    __tablename__ = "gold_route_delay_stats"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    route_id = Column(String, nullable=False)
    hour = Column(DateTime, nullable=False)
    avg_delay = Column(Float)
    max_delay = Column(Integer)
    count_delays = Column(Integer)
