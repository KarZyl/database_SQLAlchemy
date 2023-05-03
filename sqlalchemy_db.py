from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv

engine = create_engine('sqlite:///measurements.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    station = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
    name = Column(String)
    country = Column(String)
    state = Column(String)

class Measure(Base):
    __tablename__ = 'measures'
    id = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(String)
    percip = Column(String)
    tobos = Column(String)

Base.metadata.create_all(engine)

with open('clean_stations.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        station = Station(station=row[0], latitude=float(row[1]), longitude=float(row[2]), elevation=float(row[3]), name=row[4], country=row[5], state=row[6])
        session.add(station)

with open('clean_measure.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        measure = Measure(station=row[0], date=row[1], percip=row[2], tobos=row[3])
        session.add(measure)

session.commit()

result = session.execute("SELECT * FROM stations LIMIT 5")
print(result.fetchall())