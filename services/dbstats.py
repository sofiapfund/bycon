#!/usr/local/bin/python3

import cgi, cgitb
import re, json, yaml
from os import environ, pardir, path
import sys, os, datetime

# local
dir_path = path.dirname(path.abspath(__file__))
pkg_path = path.join( dir_path, pardir )
sys.path.append( pkg_path )
from beaconServer.lib.cgi_utils import cgi_parse_query,cgi_print_response,cgi_break_on_errors
from beaconServer.lib.read_specs import dbstats_return_latest
from beaconServer.lib.parse_filters import select_dataset_ids, check_dataset_ids
from beaconServer.lib.service_utils import *

"""podmd

* <https://progenetix.org/services/dbstats/>
* <https://progenetix.org/services/dbstats/?statsNumber=3&responseFormat=simple>
* <http://progenetix.org/cgi/bycon/services/dbstats.py?method=filtering_terms>

podmd"""

################################################################################
################################################################################
################################################################################

def main():

    dbstats()
    
################################################################################

def dbstats():

    byc = initialize_service()

    select_dataset_ids(byc)
    check_dataset_ids(byc)

    if "statsNumber" in byc["form_data"]:
        s_n = byc["form_data"]["statsNumber"]
        try:
            s_n = int(s_n)
        except:
            pass
        if type(s_n) == int:
            if s_n > 0:
                byc["stats_number"] = s_n

    create_empty_service_response(byc)

    ds_stats = dbstats_return_latest(byc)

    results = [ ]
    for stat in ds_stats:
        byc["service_response"]["response"]["info"].update({ "date": stat["date"] })
        for ds_id, ds_vs in stat["datasets"].items():
            if len(byc[ "dataset_ids" ]) > 0:
                if not ds_id in byc[ "dataset_ids" ]:
                    continue
            dbs = { "dataset_id": ds_id }
            for k in byc["these_prefs"]["methods"][ byc["method"] ]:
                dbs.update({k:ds_vs[k]})
            results.append( dbs )

    populate_service_response( byc, results )
    cgi_print_response( byc, 200 )

################################################################################
################################################################################

if __name__ == '__main__':
    main()
