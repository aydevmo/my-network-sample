import re
import os
import uuid
from enum import Enum

from db import   Host, LogRecord, Helper, dal

log_dir = os.sep.join([os.getcwd(),"python","log_processing_01"])

class SortBy(Enum):
    country_code = 1
    ipv4 = 2

def summarize_by_ipv4(sortby:SortBy):

    dal.connect()
    dal.session = dal.Session()

    hosts = None
    if sortby == SortBy.country_code:
        hosts = dal.session.query(Host).order_by(Host.country_code, Host.city, Host.ipv4_id).limit(2000)
    else:
        hosts = dal.session.query(Host).order_by(Host.ipv4_id).limit(2000)

    postfix = ''
    if sortby == SortBy.country_code:
        postfix = '_by_Country_'
    else:
        postfix = '_by_IPv4_'

    html_file_name = "Port_Scan_Source" + postfix + str(uuid.uuid4()) + ".htm"
    html_path = os.sep.join([log_dir, html_file_name])

    with open(html_path,'w') as out:

        out.write('<html><head><title> IPv4 Port Scan Source Addresses </title>')
        out.write('    <style>body {background-color: #c0c0c0;}</style> \n')
        out.write('    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" ' \
            ' integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous"> \n')
        out.write('</head><body> \n')
        out.write('<table class="table table-dark"><thead><tr><th scope="col"> IPv4 Source </th><th scope="col"> Country </th><th scope="col"> Country <br/> Code </th> \n')
        out.write('    <th scope="col"> City </th><th scope="col"> Latitude </th><th scope="col"> Longitude </th></th><th scope="col"> Occurrence </th></th></thead><tbody> \n')

        line = ""
        
        for host in hosts:
            if(host.ipv4_string.startswith("192.168.")):
                continue
            print(host)

            rec_cnt = dal.session.query(LogRecord).filter(LogRecord.source == host.ipv4_id).count()

            city = ''  # Avoid 'None' when dispalying
            if host.city:
                city = host.city

            line = f'<tr><td> {host.ipv4_string} </td><td> {host.country} </td><td> {host.country_code} </td><td> {city} </td>' \
                   f'<td> {host.latitude} </td><td> {host.longitude} </td><td>{ rec_cnt }</td> </tr> \n'
            
            try: 
                out.write(line)
            except UnicodeEncodeError as uc_err:
                # use ascii() to convert city name to bypass unicode conversion error
                line = f'<tr><td> {host.ipv4_string} </td><td> {host.country} </td><td> {host.country_code} </td><td> {ascii(city)} </td>' \
                   f'<td> {host.latitude} </td><td> {host.longitude} </td><td>{ rec_cnt }</td> </tr> \n'
                out.write(line)

        out.write('</tbody></table></body></html>')

    dal.session.close()


if __name__ == '__main__':
    print(__file__ + "=>")

    summarize_by_ipv4(SortBy.country_code)

    summarize_by_ipv4(SortBy.ipv4)


