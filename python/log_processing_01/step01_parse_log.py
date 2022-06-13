# The file cisco-2021-0621a.log will not be included. Please use file cisco-test01.log for testing.

import re
import os
from datetime import datetime

from db import   Host, LogRecord, Helper, Protocol, dal

batch_num_of_line = 500  #process this number of lines into memory and then write to database
log_dir = os.sep.join([os.getcwd(),"python","log_processing_01"])
log_file_name = "cisco-2021-0621a.log"
#log_file_name = "cisco-test01.log"

class LogRecordCache():
    def __init__(self, dt:datetime, lognum:int, protocol:str, src:int, dest:int, dest_port:int, occurrence:int):
        '''dt: date and time'''
        '''lognum: Cisco ASA log message number'''
        '''protocol: 'tcp' | 'udp' | 'icmp'  '''
        '''src:  Source IPv4 address in integer form'''
        '''dest: Destination IPv4 address in integer form '''
        '''dest_port: Destination port number. For ICMP, record (Type << 8) + Code.'''
        self.dt = dt
        self.lognum = lognum
        self.protocol = protocol
        self.src = src
        self.dest = dest
        self.dest_port = dest_port
        self.occurrence = occurrence

    def __repr__(self):
        return "LogRecordCache(dt={self.dt}, " \
            "lognum={self.lognum}, " \
            "protocol='{self.protocol}', " \
            "src={self.src}, " \
            "dest={self.dest}, " \
            "dest_port={self.dest_port}, " \
            "occurrence={self.occurrence} )".format(self=self)

def process_log():
    log_path = os.sep.join([log_dir, log_file_name])

    cache_list = []
    address_set = set()
    line_count = 0
    eof = False

    re_obj = re.compile('^(.{15}).*%ASA-4-106023: Deny (tcp|udp) src outside:(.*?)\/.*? dst .*?\:(.*?)/(\d*?) by access-group')

    re_obj_icmp = re.compile('^(.{15}).*%ASA-4-106023: Deny icmp src outside:(.*?) dst inside.*?\:(.*?) \(type (\d+), code (\d+)\) by access-group')

    with open(log_path) as f:
        while True:
            line = f.readline()
            
            if not line:
                eof = True

            if not eof:
                line_count +=1

                protocol = src = dest = ""
                dest_port = type = code = 0
                dt_obj = None

                tokens = re_obj.match(line)
                if tokens:
                    #matched tcp or udp
                    print(tokens.group(1))
                    protocol = tokens.group(2)
                    src = tokens.group(3)
                    dest = tokens.group(4)
                    dest_port = int(tokens.group(5))
                    print("protocol:" + protocol +" src:" + src + " dest:" + dest + " dest-port:" + str(dest_port) )

                else:
                    tokens = re_obj_icmp.match(line)
                    if tokens:
                        #matched icmp
                        print(tokens.group(1) + " icmp")
                        protocol = "icmp"
                        src = tokens.group(2)
                        dest = tokens.group(3)
                        type = int(tokens.group(4))
                        code = int(tokens.group(5))
                        dest_port = Helper.icmptypecode_to_int(type, code)  #use variable dest_port as a temp storage for db insertion
                        print("protocol:icmp" +" src:" + src + " dest:" + dest + " type:" + str(type) + " code:" + str(code) )

                if tokens:
                    #process shared properties
                    dt_obj = datetime.strptime(tokens.group(1), "%b %d %H:%M:%S")  #e.g. "Jun 21 20:58:26" or "Jan  2 07:49:12"
                    dt_obj = dt_obj.replace(year=datetime.today().year - 1)  #year field is not in the log files. Put a dummy year. 
                    print(dt_obj)
                    print()
                    address_set.add(src)
                    address_set.add(dest)

                    cache_list.append(  \
                        LogRecordCache(dt_obj, 106023, protocol, Helper.ipv4stoint(src), Helper.ipv4stoint(dest), dest_port, 1 )  \
                        )   #106023 is the Cisco log message number.
            
            if line_count >= batch_num_of_line or eof:
                dal.connect()
                dal.session = dal.Session()

                for addr in address_set:
                    addr_int = Helper.ipv4stoint(addr)
                    rec_cnt = dal.session.query(Host).filter(Host.ipv4_id == addr_int).count()

                    if not rec_cnt:
                        host = Host(ipv4_id=addr_int, ipv4_string=addr)
                        dal.session.add(host)
                        dal.session.commit()

                log_rec_bulk=[]
                for r in cache_list:
                    log_rec = LogRecord(created_on=r.dt, log_number=r.lognum, protocol=r.protocol, \
                        source=r.src, destination=r.dest, destination_port=r.dest_port)
                    log_rec_bulk.append(log_rec)

                if(len(log_rec_bulk)):
                    dal.session.bulk_save_objects(log_rec_bulk)
                    dal.session.commit()

                dal.session.close()
                line_count = 0
                cache_list = []
                address_set = set()

            if eof:
                break  #break file reading while loop 


if __name__ == '__main__':
    print(__file__ + '=>')

    process_log()

    

