#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 11:00:59 2021

@author: hansb
"""

import pyaerocom as pya

"""
As a quick fix I will put this program in the data repository and then think 
pyaerocom integration later.
"""

# at the end of processing all coldata:


dummy_stats=pya.aeroval.coldatatojson_engine._init_stats_dummy()
    


regions = pya.aeroval.coldatatojson_engine.read_json('regions.json')

hm = pya.aeroval.coldatatojson_engine.read_json('hm/glob_stats_daily.json')

for k1,v1 in hm.items():
    for k2,v2 in v1.items():
        for k3,v3, in v2.items():
            for k4,v4 in v3.items():
                for k5,v5 in v4.items():
                    region_subkeys = list(v5['WORLD'].keys())
                    for region in regions.keys():
                        try:
                            v5[region]
                        except KeyError:
                            v5[region] = {}
                            for subkey in region_subkeys:
                                v5[region][subkey] = dummy_stats
                                
pya.aeroval.coldatatojson_engine.write_json(hm, '/home/hansb/lustre/storeA/project/fou/kl/CAMS61/postprocessed_data/repositories/aeroval/data/emep/2021-reporting/hm/glob_stats_daily.json',ignore_nan=True)