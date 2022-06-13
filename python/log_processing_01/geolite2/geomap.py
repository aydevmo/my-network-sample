# Please visit https://dev.maxmind.com/?lang=en
# to download the free GeoLite2 City database. (GeoLite2-City.mmdb)

# https://dev.maxmind.com/geoip/geolocate-an-ip/databases?lang=en

import os
import geoip2.database

path = os.sep.join([os.getcwd(), "python", "log_processing_01", "geolite2", "GeoLite2-City.mmdb" ])


# This reader object should be reused across lookups as creation of it is
# expensive.
with geoip2.database.Reader(path) as reader:
    response = reader.city('128.101.101.101')
    
    print(response.country.iso_code)
    print(response.country.name)
    print(str(response.location.latitude) + ',' + str(response.location.longitude))
    print(response.city.name)
    


