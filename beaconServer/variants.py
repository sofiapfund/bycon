#!/usr/local/bin/python3

import cgi, cgitb, sys
from os import path, environ, pardir

# local
dir_path = path.dirname( path.abspath(__file__) )
pkg_path = path.join( dir_path, pardir )
sys.path.append( pkg_path )

from beaconServer import *

################################################################################
################################################################################
################################################################################

"""
https://progenetix.test/beacon/variants/?filters=NCIT:C7712&output=pgxseg&debug=1
"""

def main():

    variants()
    
################################################################################

def variants():

    byc = initialize_service()
    run_beacon_init_stack(byc)
    run_beacon(byc)
    export_datatable(byc)
    query_results_save_handovers(byc)
    cgi_print_response( byc, 200 )

################################################################################
################################################################################
################################################################################

if __name__ == '__main__':
    main()
