#!/usr/local/bin/python3
import cgi, cgitb, sys
from os import pardir, path

# local
dir_path = path.dirname(path.abspath(__file__))
pkg_path = path.join( dir_path, pardir )
sys.path.append( pkg_path )

from beaconServer import *

"""podmd

* <https://progenetix.org/beacon/info/>

podmd"""

################################################################################
################################################################################
################################################################################

def main():

    info()
    
################################################################################

def info():

    byc = initialize_service()
    parse_beacon_schema(byc)
    select_dataset_ids(byc)
    check_dataset_ids(byc)
    create_empty_service_response(byc)
    byc["beacon_info"].update({"datasets": datasets_update_latest_stats(byc) })
    # TODO: Adjust to new format???
    populate_service_response( byc, [ byc["beacon_info"] ] )
    cgi_print_response( byc, 200 )

################################################################################
################################################################################

if __name__ == '__main__':
    main()
