import re, yaml
from pymongo import MongoClient
from os import environ, pardir, path
import sys

from cgi_utils import *

################################################################################

def dataset_response_add_handovers(ds_id, byc):

    """podmd
    podmd"""

    h_o_server = _handover_select_server(**byc) 
    b_h_o = [ ]

    if not ds_id in byc["dataset_definitions"]:
        return b_h_o

    ds_h_o =  byc["dataset_definitions"][ ds_id ]["info"]["handoverTypes"]
    h_o_types = byc["handover_definitions"]["h->o_types"]

    for h_o_t in h_o_types.keys():

        # testing if this handover is active fo the specified dataset
        h_o_defs = h_o_types[ h_o_t ]

        if not h_o_t in ds_h_o:
            continue

        for h_o_key in byc[ "query_results" ].keys():
            h_o = byc[ "query_results" ][ h_o_key ]
            if h_o["target_count"] < 1:
                continue
            accessid = h_o["id"]
            if h_o_key == h_o_types[ h_o_t ][ "h->o_key" ]:
                this_server = h_o_server
                if "remove_subdomain" in h_o_types[ h_o_t ]:
                    this_server = re.sub(r'\/\/\w+?\.(\w+?\.\w+?)$', r'//\1', this_server)
                h_o_r = {
                    "handoverType": {
                        "id": h_o_defs[ "id" ],
                        "label": "{}".format(h_o_defs[ "label" ]),
                    },
                    "description": h_o_defs[ "description" ],
                }

                url_opts = ""
                if "url_opts" in h_o_defs:
                    url_opts = h_o_defs["url_opts"]

                if "bedfile" in h_o_defs[ "id" ]:
                    ucsc_pos = _write_variants_bedfile(h_o, **byc)
                    h_o_r.update( { "url": _handover_create_ext_url(this_server, h_o_defs, accessid, ucsc_pos ) } )
                else:
                    h_o_r.update( { "url": _handover_create_url(this_server, h_o_defs, accessid, url_opts) } )

                # TODO: needs a new schema to accommodate this not as HACK ...
                # the phenopackets URL needs matched variants, which it wouldn't know about ...
                if "phenopackets" in h_o_t:
                    if "variants._id" in byc[ "query_results" ].keys():
                        h_o_r["url"] += "&variantsaccessid="+byc[ "query_results" ][ "variants._id" ][ "id" ]

                b_h_o.append( h_o_r )

    return b_h_o

################################################################################

def query_results_save_handovers(byc):

    ho_client = MongoClient()
    ho_db = ho_client[ byc["config"]["info_db"] ]
    ho_coll = ho_db[ byc["config"][ "handover_coll" ] ]

    for h_o_k in byc[ "query_results" ].keys():
        h_o = byc[ "query_results" ][ h_o_k ]
        h_o_size = sys.getsizeof(h_o["target_values"])
        # print("Storage size for {}: {}Mb".format(h_o_k, h_o_size / 1000000))
        if h_o_size < 15000000:
            ho_coll.update_one( { "id": h_o["id"] }, { '$set': h_o }, upsert=True )

    ho_client.close()

    return True

################################################################################

def _handover_select_server( **byc ):

    s_uri = str(environ.get('SCRIPT_URI'))
    if "https:" in s_uri:
        return "https://"+str(environ.get('HTTP_HOST'))
    else:
        return "http://"+str(environ.get('HTTP_HOST'))

################################################################################

def _handover_create_url(h_o_server, h_o_defs, accessid, url_opts):

    if "script_path_web" in h_o_defs:
        server = h_o_server
        if "http" in h_o_defs["script_path_web"]:
            server = ""
        url = "{}{}?accessid={}".format(server, h_o_defs["script_path_web"], accessid)
        for p in ["method", "output"]:
            if p in h_o_defs:
                url += "&{}={}".format(p, h_o_defs[p])
        url += url_opts

        return url

    return ""

################################################################################

def _handover_create_ext_url(h_o_server, h_o_defs, accessid, ucsc_pos):

    if "ext_url" in h_o_defs:
        if "bedfile" in h_o_defs["id"]:
            return("{}&position={}&hgt.customText={}/tmp/{}.bed".format(h_o_defs["ext_url"], ucsc_pos, h_o_server, accessid))

    return False

################################################################################

def _write_variants_bedfile(h_o, **byc):

    """podmd
    #### `BeaconPlus::DataExporter::write_variants_bedfile`

    ##### Accepts

    * a Bycon `byc` object
    * a Bycon `h_o` handover object with its `target_values` representing `_id` 
    objects of a `variants` collection
        
    The function creates a basic BED file and returns its local path. A standard 
    use would be to create a link to this file and submit it as `hgt.customText` 
    parameter to the UCSC browser.

    ##### TODO

    * The creation of the different variant types is still rudimentary and has to be 
    expanded in lockstep with improving Beacon documentation and examples. The 
    definition of the types and their match patterns should also be moved to a 
    +separate configuration entry and subroutine.
    * evaluate to use "bedDetails" format

    podmd"""
 
    if len( h_o["target_values"] ) < 1:
        return()
    if not h_o["target_collection"] == "variants":
         return()
       
    ds_id = h_o["source_db"]
    accessid = h_o["id"]
    bed_file = path.join( *byc["config"][ "paths" ][ "web_temp_dir_abs" ], h_o["id"]+'.bed' )

    vs = { "DUP": [ ], "DEL": [ ], "LOH": [ ], "SNV": [ ]}

    data_client = MongoClient( )
    data_db = data_client[ ds_id ]
    data_coll = data_db[ h_o["target_collection"] ]

    for v in data_coll.find( { h_o["target_key"]: { '$in': h_o["target_values"] } }):

        if "variant_type" in v:
            v.update({"size": v["end"] - v["start"] })
            if v["variant_type"] == "DUP":
                vs["DUP"].append(v)
            elif  v["variant_type"] == "DEL":
                vs["DEL"].append(v)
            elif  v["variant_type"] == "LOH":
                vs["LOH"].append(v)
        elif "reference_bases" in v:
            vs["SNV"].append(v)

    b_f = open( bed_file, 'w' )

    pos = set()

    ucsc_chr = ""

    for vt in vs.keys():
        if len( vs[vt] ) > 0:
            try:
                vs[vt] = sorted(vs[vt], key=lambda k: k['size'], reverse=True)
            except:
                pass
            col_key = "color_var_"+vt.lower()+"_rgb"
            b_f.write("track name={} visibility=squish description=\"{} variants matching the query\" color={}\n".format(vt, vt, byc["config"]["plot_pars"][col_key]) )
            b_f.write("#chrom\tchromStart\tchromEnd\tbiosampleId\n")
            for v in vs[vt]:
                ucsc_chr = "chr"+v["reference_name"]
                ucsc_min = int( v["start"] + 1 )
                ucsc_max = int( v["end"] )
                l = "{}\t{}\t{}\t{}\n".format( ucsc_chr, ucsc_min, ucsc_max, v["biosample_id"] )
                pos.add(ucsc_min)
                pos.add(ucsc_max)
                b_f.write( l )
 
    b_f.close()
    ucsc_range = sorted(pos)
    ucsc_pos = "{}:{}-{}".format(ucsc_chr, ucsc_range[0], ucsc_range[-1])

    return ucsc_pos

