# Please visit https://dev.maxmind.com/?lang=en
# to download the free GeoLite2 City database. (GeoLite2-City.mmdb)

import os
import geoip2.database

from db import   Host, dal

geodb_path = os.sep.join([os.getcwd(), "python", "log_processing_01", "geolite2", "GeoLite2-City.mmdb" ])

def insert_loc_to_host_table():
    dal.connect()
    dal.session = dal.Session()

    with geoip2.database.Reader(geodb_path) as reader:
        for host in dal.session.query(Host):
            if not host.country_code:
                try:
                    geodata = reader.city(host.ipv4_string)
                    host.latitude = geodata.location.latitude
                    host.longitude = geodata.location.longitude
                    host.country_code = geodata.country.iso_code
                    host.country = geodata.country.name
                    host.city = geodata.city.name

                    dal.session.commit()
                    print("processed: " + host.ipv4_string)
                
                except BaseException as err:
                    print(f"Unexpected {err=}, {type(err)=}")
                
    dal.session.close()


if __name__ == '__main__':
    print(__file__ + "=>")

    insert_loc_to_host_table()

    