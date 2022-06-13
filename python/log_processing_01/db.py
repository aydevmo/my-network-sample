# reference: https://github.com/oreillymedia/essential-sqlalchemy-2e/blob/master/ch09/db.py

import os

from datetime import datetime
from enum import Enum

from sqlalchemy import (Column, Integer, Numeric, String, DateTime, Float, ForeignKey, Boolean, create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

#conn_string = 'sqlite:///aydevmo_net_log_01.db'
db_file_name = 'aydevmo_net_log_01.db'
db_path = '/'.join([os.getcwd(),"python","log_processing_01", db_file_name])
conn_string = 'sqlite:///' + db_path
Base = declarative_base()

class Protocol(Enum):
    tcp = 1
    udp = 2
    icmp = 3

class Helper:
    @classmethod
    def ipv4stoint(cls, string):
        '''Convert IPv4 string to integer'''
        token=string.strip().split('.')
        return (int(token[0]) << 24) + (int(token[1]) << 16) + (int(token[2]) << 8) + int(token[3])

    @classmethod
    def ipv4inttos(cls, num):
        '''Convert integer to IPv4 string'''
        result = []
        for i in range(4):
            result.append( str(num & 0xff) )
            if i == 3:
                break
            num >>= 8
        result.reverse()
        return '.'.join(result)

    @classmethod
    def icmptypecode_to_int(cls, type:int, code:int):
        '''Multiplex icmp type and code to 16-bit integer'''
        return (type << 8) + code


class Host(Base):
    __tablename__ = 'hosts'

    ipv4_id = Column(Integer, primary_key=True, autoincrement=False) 
            #ipv4_id is also an ipv4 address squeezed in a single integer
    ipv4_string = Column(String(20))
    hostname = Column(String(255), default='')
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)
    country_code = Column(String(4), default='')
    country = Column(String(50), default='')
    city = Column(String(50), default='')

    def __repr__(self):
        return "Host(ipv4_id={self.ipv4_id}, " \
            "ipv4_string='{self.ipv4_string}', " \
            "hostname='{self.hostname}', " \
            "latitude={self.latitude}, " \
            "longitude={self.longitude}, " \
            "country_code='{self.country_code}', " \
            "country='{self.country}', " \
            "city='{self.city}')".format(self=self)


class LogRecord(Base):
    __tablename__ = 'log_records'

    log_id = Column(Integer, primary_key=True)
    created_on = Column(DateTime(), default=datetime.now)  #log creation time
    log_number = Column(Integer, default=0)    #Cisco ASA log message number
    protocol = Column(String(10), default='')  # 'tcp' or 'udp' or 'icmp'
    source = Column(Integer)        #source ipv4 address squeezed in a single integer
    destination = Column(Integer)   #destination ipv4 address squeezed in a single integer
    destination_port = Column(Integer)
    occurrence = Column(Integer, default=1)
    sum_minutes = Column(Integer, default=0)  #whether to consolidate multiple occurrences in a single reccord 
                                              #and its summarization inteval in number of minutes

    def __repr__(self):
        return "LogRecord(log_id={self.log_id}, " \
            "created_on={self.created_on}, " \
            "log_number={self.log_number}, " \
            "protocol='{self.protocol}', " \
            "source={self.source}, " \
            "destination={self.destination}, " \
            "destination_port={self.destination_port}, " \
            "occurrence={self.occurrence}, " \
            "sum_minutes={self.sum_minutes}, " \
            "src_string='{src_string}', " \
            "dest_string='{dest_string}')".format(self=self, \
                src_string=Helper.ipv4inttos(self.source), dest_string=Helper.ipv4inttos(self.destination))

class DataAccessLayer:
    def __init__(self):
        self.engine = None
        self.session = None
        self.conn_string = conn_string

    def connect(self):
        self.engine = create_engine(self.conn_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

dal = DataAccessLayer()

def test_ipv4_conversion():
    test_string = "255.255.255.251"
    print("test_string: " + test_string)
    x = Helper.ipv4stoint(test_string)
    print("Converted to int: " + str(x))
    print("Converted from int to string: " + Helper.ipv4inttos(x))
    print()

def test_host_insertion():
    dal.connect()
    dal.session = dal.Session()

    host = Host(ipv4_id=Helper.ipv4stoint("255.255.255.251"), ipv4_string="255.255.255.251", \
        hostname="test.com", latitude=1.0, longitude=1.0, country_code="US", country="US", city="VA")
    print(host)
    dal.session.add(host)
    dal.session.commit()
    dal.session.close()

def test_db_host_query():
    # dal = DataAccessLayer()
    # dal.conn_string = 'sqlite:///aydevmo_net_log_01.db'
    dal.connect()
    dal.session = dal.Session()

    hosts = dal.session.query(Host).limit(50).all()
    for host in hosts:
        print(host)

    print("Number of hosts: " + str(len(hosts)))

    dal.session.close()

def test_db_log_record_query():
    dal.connect()
    dal.session = dal.Session()

    records = dal.session.query(LogRecord).limit(50).all()
    for rec in records:
        print(rec)

    print("Number of recordss: " + str(len(records)))

    dal.session.close()

def test_db_log_record_query_sort():
    dal.connect()
    dal.session = dal.Session()

    records = dal.session.query(LogRecord).order_by(LogRecord.source).limit(1000)
    for rec in records:
        print(rec)

    dal.session.close()


if __name__ == '__main__':
    print(__file__ + '=>')
    #test_ipv4_conversion()
    #test_host_insertion()
    #test_db_host_query()
    #test_db_log_record_query()
    test_db_log_record_query_sort()


    
    

