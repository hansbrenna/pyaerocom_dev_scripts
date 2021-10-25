#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 14:16:27 2021

@author: hansb
"""

import os
import pyaerocom as pya
import xarray as xr
import pandas as pd

test=pya.ColocatedData('/home/hansb/lustre/storeA/project/fou/kl/CAMS61/postprocessed_data/repositories/aerocom_evaluation/coldata/cams61_p3/BASE/EMEP.cams61.hmixKz/concpm25_REF-EEA-diurnal-rural_MOD-EMEP-hmixKz_20180101_20181231_hourly_WORLD-wMOUNTAINS.nc')

year1 = test.data

year2 = year1.copy(deep=True)

replacement_time = pd.date_range(start='2019-01-01',end='2019-12-31T23:00:00',freq='H')

year2=year2.assign_coords(time=replacement_time)

inp = pya.ColocatedData(xr.concat([year1,year2], dim='time'))


out1=pya.aeroval.coldatatojson_helpers._create_diurnal_weekly_data_object(inp,'seasonal')
out2=pya.aeroval.coldatatojson_helpers._create_diurnal_weekly_data_object(inp,'yearly')

meta_glob={'obs_name':'EEA',
           'model_name':'EMEP',
           'var_name_web':'EEA-rural',
           'vert_code':'Surface',
           'blah':'blub',
           'foo':'bar'}

repw_res = {'seasonal':out1['rep_week'],'yearly':out2['rep_week'].expand_dims('period',axis=0),}

ts_objs = pya.aeroval.coldatatojson_helpers._process_weekly_object_to_station_time_series(repw_res, meta_glob)

ts_objs_reg = pya.aeroval.coldatatojson_helpers._process_weekly_object_to_country_time_series(repw_res, meta_glob,'country',{'WORLD':'WORLD'})


outdir = '/home/hansb/pyaerocom-dev-scripts/2021/test/dw/'
for ts_data_weekly in ts_objs:
    #writes json file
    pya.aeroval.coldatatojson_helpers._write_stationdata_json(ts_data_weekly, outdir)
if ts_objs_reg != None:
    for ts_data_weekly_reg in ts_objs_reg:
        #writes json file
        pya.aeroval.coldatatojson_helpers._write_stationdata_json(ts_data_weekly_reg, outdir)

# pya.aeroval.coldatatojson_engine.ColdataToJsonEngine().process_coldata(inp)
