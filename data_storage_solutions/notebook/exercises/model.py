"""
Database model definition
"""
from sqlalchemy import Column, Integer, String, DateTime, DDL, Float, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import validates
from sqlalchemy.event import listen
from geoalchemy2 import Geometry

from psycopg2.extensions import adapt, register_adapter, AsIs
from geoalchemy2.elements import WKBElement

Base = declarative_base()


form_tables = {}

for table in ['demo_case','demo_alert','demo_register']:
    form_tables[table] = type(table, (Base, ),
                              {"__tablename__": table,
                               "id": Column(Integer, primary_key=True),
                               "uuid": Column(String, index=True),
                               "data": Column(JSONB)})
    create_index = DDL("CREATE INDEX {} ON {} USING gin(data);".format(table + "_gin", table))
    listen(form_tables[table].__table__, 'after_create', create_index)


class DownloadDataFiles(Base):
    __tablename__ = 'download_data_files'

    uuid = Column(String, primary_key=True)
    generation_time = Column(DateTime)
    type = Column(String)
    status = Column(Float)
    success = Column(Integer)
    csvcontent = Column(String)
    xlscontent = Column(LargeBinary)


class Locations(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_location = Column(Integer, index=True)
    point_location = Column(Geometry("POINT"))
    area = Column(Geometry("MULTIPOLYGON"))
    other = Column(String)
    deviceid = Column(String)
    clinic_type = Column(String)
    case_report = Column(Integer, index=True)
    level = Column(String, index=True)
    start_date = Column(DateTime)
    case_type = Column(String, index=True)
    population = Column(Integer, default=0)

    def __repr__(self):
        return "<Location(name='%s', id='%s', parent_location='%s')>" % (
            self.name, self.id, self.parent_location)


class Devices(Base):
    __tablename__ = 'devices'
    device_id = Column(String, primary_key=True)
    tags = Column(JSONB)


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    type = Column(String, index=True)
    type_name = Column(String)
    date = Column(DateTime, index=True)
    country = Column(Integer, index=True)
    region = Column(Integer, index=True)
    district = Column(Integer, index=True)
    clinic = Column(Integer, index=True)
    clinic_type = Column(String)
    case_type = Column(String)
    links = Column(JSONB)
    tags = Column(JSONB, index=True)
    variables = Column(JSONB, index=True)
    categories = Column(JSONB, index=True)
    geolocation = Column(Geometry("POINT"))

    def __repr__(self):
        return "<Data(uuid='%s', id='%s'>" % (
            self.uuid, self.id )

create_index = DDL("CREATE INDEX variables_gin ON data USING gin(variables);")
listen(Data.__table__, 'after_create', create_index)
create_index2 = DDL("CREATE INDEX categories_gin ON data USING gin(categories);")
listen(Data.__table__, 'after_create', create_index2)

class DisregardedData(Base):
    __tablename__ = 'disregarded_data'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    type = Column(String, index=True)
    type_name = Column(String)
    date = Column(DateTime, index=True)
    country = Column(Integer, index=True)
    region = Column(Integer, index=True)
    district = Column(Integer, index=True)
    clinic = Column(Integer, index=True)
    clinic_type = Column(String)
    case_type = Column(String)
    links = Column(JSONB)
    tags = Column(JSONB, index=True)
    variables = Column(JSONB, index=True)
    categories = Column(JSONB, index=True)
    geolocation = Column(Geometry("POINT"))

    def __repr__(self):
        return "<DisregardedData(uuid='%s', id='%s'>" % (
            self.uuid, self.id
        )

create_index3 = DDL("CREATE INDEX disregarded_variables_gin ON disregarded_data USING gin(variables);")
listen(DisregardedData.__table__, 'after_create', create_index3)
create_index4 = DDL("CREATE INDEX disregarded_category_gin ON disregarded_data USING gin(categories);")
listen(DisregardedData.__table__, 'after_create', create_index4)

class Links(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    uuid_from = Column(String, index=True)
    uuid_to = Column(String, index=True)
    type = Column(String, index=True)
    data_to = Column(JSONB)

class AggregationVariables(Base):
    __tablename__ = 'aggregation_variables'

    id_pk = Column(Integer, primary_key = True)
    id = Column(String)
    name = Column(String)
    type = Column(String)
    form = Column(String)
    multiple_link = Column(String)
    db_column = Column(String)
    method = Column(String)
    condition = Column(String)
    category = Column(JSONB, index=True)
    alert = Column(Integer, index=True)
    alert_type = Column(String, index=True)
    calculation = Column(String)
    disregard = Column(Integer)
    calculation_group = Column(String)
    calculation_priority = Column(String)
    classification = Column(String)
    classification_casedef = Column(String)
    source = Column(String)
    source_link = Column(String)
    alert_desc = Column(String)
    case_def = Column(String)
    risk_factors = Column(String)
    symptoms = Column(String)
    labs_diagnostics = Column(String)

    def __repr__(self):
        return "<AggregationVariable(name='%s', id='%s'>" % (
            self.name, self.id)

    @validates("alert")
    def alert_setter(self, key, alert):
        if alert == "":
            return 0
        else:
            return alert

    @validates("daily")
    def daily_setter(self, key, daily):
        if daily == "":
            return 0
        else:
            return daily

    @validates("disregard")
    def disregard_setter(self, key, disregard):
        if disregard == "":
            return 0
        else:
            return disregard
