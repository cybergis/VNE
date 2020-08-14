#!/usr/bin/env python
# coding: utf-8

import json, math, copy, sys
#from geosnap.data import store_ltdb
from geosnap.io import store_ltdb
#from geosnap.data import Community
from geosnap import Community, datasets
#from geosnap.data import store_census
from geosnap.io import store_census
#from geosnap.data import data_store
import pandas as pd
import shapely.wkt
import shapely.geometry
from datetime import datetime
from datetime import timedelta
from pathlib import Path
#from INCS import linc
import urllib.parse
import webbrowser
import os
import pprint
from sklearn.preprocessing import minmax_scale
import numpy as np
from scipy import stats
import geopandas as gpd
import csv


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def write_LOG(param):
    #Create a new folder where GEO_CONFIG.js GEO_JSON.js VARIABLES.js will be saved
    oDir = 'VNE_' + param['filename_suffix']
    path = Path(oDir + '/data')
    path.mkdir(parents=True, exist_ok=True)
    
    contents = pprint.pformat(param)
    #print(oDir+"/data/param.log")
    #print(contents)
    #write new outfiles: GEO_CONFIG.js GEO_JSON.js VARIABLES.js
    ofile = open(oDir+"/data/param.log", "w")
    create_at = datetime.now()
    ofile.write('%s %s\r\n' % (create_at.strftime('%Y-%m-%d'), create_at.strftime('%H:%M:%S')))
    #ofile.write('\r\n\r\n')
    ofile.write('  '+contents.replace('\n', '\n  '))
    ofile.close()


def write_INDEX_html(param):
    #Create a new folder where GEO_CONFIG.js GEO_JSON.js VARIABLES.js will be saved
    oDir = 'VNE_' + param['filename_suffix']
    path = Path(oDir + '/data')
    path.mkdir(parents=True, exist_ok=True)
    
    contents = []
    #open Neighborhood_Analysis_Mapper.html (the excutable file for the visualization)
    ifile = open("template/Neighborhood_Analysis_Mapper.html", "r", encoding="utf-8")
    contents = ifile.read()
    
    #Replace variables based on the user's selection in each of four files below.
    contents = contents.replace("Neighborhood Analysis Mapper", param['title'])
    contents = contents.replace("data/GEO_CONFIG.js", "data/GEO_CONFIG_"+param['filename_suffix']+".js")
    contents = contents.replace("data/GEO_JSON.js", "data/GEO_JSON_"+param['filename_suffix']+".js")
    contents = contents.replace("data/GEO_VARIABLES.js", "data/GEO_VARIABLES_"+param['filename_suffix']+".js")
    
    #write new outfiles: GEO_CONFIG.js GEO_JSON.js VARIABLES.js
    ofile = open(oDir+"/index.html", "w", encoding="utf-8")
    ofile.write(contents)
    ofile.close()


def write_ALL_METROS_INDEX_html(param):
    #Create a new folder where GEO_CONFIG.js GEO_JSON.js VARIABLES.js will be saved
    oDir = 'VNE_' + param['filename_suffix']
    path = Path(oDir + '/data')
    path.mkdir(parents=True, exist_ok=True)
    
    contents = []
    #open Adaptive_Choropleth_Mapper.html (the excutable file for the visualization)
    ifile = open("template/Adaptive_Choropleth_Mapper.html", "r")
    contents = ifile.read()
    
    #Replace variables based on the user's selection in each of four files below.
    contents = contents.replace("Adaptive Choropleth Mapper", param['title'])
    contents = contents.replace("data/GEO_CONFIG.js", "data/GEO_CONFIG_"+param['filename_suffix']+".js")
    contents = contents.replace("data/GEO_JSON.js", "data/GEO_JSON_"+param['filename_suffix']+".js")
    contents = contents.replace("data/GEO_VARIABLES.js", "data/GEO_VARIABLES_"+param['filename_suffix']+".js")
    
    #write new outfiles: GEO_CONFIG.js GEO_JSON.js VARIABLES.js
    ofile = open(oDir+"/index.html", "w")
    ofile.write(contents)
    ofile.close()


def write_GEO_CONFIG_js(param):
    # read ACM_GEO_CONFIG.js
    ifile = open("template/VNE_GEO_CONFIG.js", "r")
    contents = ifile.read()
    
    SubjectName = "";
    allMetros = False;
    Index_of_neighborhood_change = True;
    Maps_of_neighborhood = True;               
    Distribution_INC1 = True;                  
    Distribution_period = False; 
    Distribution_cluster = False;
    Temporal_change_in_neighborhoods = True;
    Parallel_Categories_Diagram_in_neighborhoods = True;
    Chord_Diagram_in_neighborhoods = True;
    Zscore_Means_across_Clusters = True;
    Zscore_Means_of_Each_Cluster = True;
    Number_of_Barcharts_for_Subject_Clusters = 0;
    Number_of_BoxPlots_for_Subject_Clusters = 0;
    
    if ('subject' in param): SubjectName =  param['subject']
    if ('allMetros' in param): allMetros =  param['allMetros']
    if ('Index_of_neighborhood_change' in param): Index_of_neighborhood_change =  param['Index_of_neighborhood_change']
    if ('Maps_of_neighborhood' in param): Maps_of_neighborhood =  param['Maps_of_neighborhood']
    if ('Distribution_INC1' in param): Distribution_INC1 =  param['Distribution_INC1']
    if ('Distribution_INC2_different_period' in param): Distribution_period =  param['Distribution_INC2_different_period']
    if ('Distribution_INC2_different_cluster' in param): Distribution_cluster =  param['Distribution_INC2_different_cluster']
    if ('Temporal_change_in_neighborhoods' in param): Temporal_change_in_neighborhoods =  param['Temporal_change_in_neighborhoods']
    if ('Parallel_Categories_Diagram_in_neighborhoods' in param): Parallel_Categories_Diagram_in_neighborhoods =  param['Parallel_Categories_Diagram_in_neighborhoods']
    if ('Chord_Diagram_in_neighborhoods' in param): Chord_Diagram_in_neighborhoods =  param['Chord_Diagram_in_neighborhoods']
    if ('Zscore_Means_across_Clusters' in param): Zscore_Means_across_Clusters =  param['Zscore_Means_across_Clusters']
    if ('Zscore_Means_of_Each_Cluster' in param): Zscore_Means_of_Each_Cluster =  param['Zscore_Means_of_Each_Cluster']
    if ('Number_of_Barcharts_for_Subject_Clusters' in param): Number_of_Barcharts_for_Subject_Clusters =  param['Number_of_Barcharts_for_Subject_Clusters']
    if ('Number_of_BoxPlots_for_Subject_Clusters' in param): Number_of_BoxPlots_for_Subject_Clusters =  param['Number_of_BoxPlots_for_Subject_Clusters']
    
    # perpare parameters
    #NumOfMaps = len(param['years']) + 1
    #NumOfMaps = len(param['years']) + 1 if Index_of_neighborhood_change else len(param['years'])
    #InitialLayers = ["INC"]
    InitialLayers = ["INC"] if Index_of_neighborhood_change else []
    if (len(param['years']) <= 1): InitialLayers = []
    if (len(InitialLayers) == 0):
        if ('diseaseInputCSV' in param):
            df_disease = pd.read_csv(param['diseaseInputCSV'], dtype={'geoid':str})
            df_disease['geoid'] = df_disease['geoid'].astype(str)
            df_disease = df_disease.set_index('geoid')
            if (len(df_disease.columns) >= 1): InitialLayers.append(" "+df_disease.columns[0])
    for i, year in enumerate(param['years']):
        InitialLayers.append(str(year))
    NumOfMaps = len(InitialLayers)
    
    # Automatically set Map_width, Map_height. 
    Map_width = "300px"
    Map_height = "300px"
    if (NumOfMaps <= 6):
        Map_width = "300px"
        Map_height = "300px"	
    if (NumOfMaps <= 5):
        Map_width = "350px"
        Map_height = "350px"
    if (NumOfMaps <= 4):
        Map_width = "400px"
        Map_height = "400px"
    if (NumOfMaps <= 3):
        Map_width = "400px"
        Map_height = "400px"
    if (NumOfMaps <= 2):
        Map_width = "450px"
        Map_height = "450px"
    if (NumOfMaps ==	1):
        Map_width = "800px"
        Map_height = "800px"	
    # replace newly computed "NumOfMaps", "InitialLayers", "Map_width", "Map_height" in CONFIG.js. See the example replacement below
    '''
        'years': [1980, 1990, 2000, 2010]            ->    'var InitialLayers = ["INC", "1980", "1990", "2000", "2010"];'
    '''
    NumOfMaps = "var NumOfMaps = " + str(NumOfMaps) + ";"
    SubjectName = 'var SubjectName = "' + SubjectName + '";'
    InitialLayers = "var InitialLayers = " + json.dumps(InitialLayers) + ";"
    allMetros = "var allMetros = " + json.dumps(allMetros)+ ";"
    Index_of_neighborhood_change = "var Index_of_neighborhood_change = " + json.dumps(Index_of_neighborhood_change)+ ";"
    Maps_of_neighborhood = "var Maps_of_neighborhood = " + json.dumps(Maps_of_neighborhood)+ ";"
    Distribution_INC1 = "var Distribution_INC1 = " + json.dumps(Distribution_INC1)+ ";"
    Distribution_period = "var Distribution_INC2_different_period = " + json.dumps(Distribution_period)+ ";"
    Distribution_cluster = "var Distribution_INC2_different_cluster = " + json.dumps(Distribution_cluster)+ ";"
    Temporal_change_in_neighborhoods = "var Temporal_change_in_neighborhoods = " + json.dumps(Temporal_change_in_neighborhoods)+ ";"
    Parallel_Categories_Diagram_in_neighborhoods = "var Parallel_Categories_Diagram_in_neighborhoods = " + json.dumps(Parallel_Categories_Diagram_in_neighborhoods)+ ";"
    Chord_Diagram_in_neighborhoods = "var Chord_Diagram_in_neighborhoods = " + json.dumps(Chord_Diagram_in_neighborhoods)+ ";"
    Zscore_Means_across_Clusters = "var Zscore_Means_across_Clusters = " + json.dumps(Zscore_Means_across_Clusters)+ ";"
    Zscore_Means_of_Each_Cluster = "var Zscore_Means_of_Each_Cluster = " + json.dumps(Zscore_Means_of_Each_Cluster)+ ";"
    Number_of_Barcharts_for_Subject_Clusters = "var Barchart_of_Subject_Clusters = " + str(Number_of_Barcharts_for_Subject_Clusters) + ";"
    Number_of_BoxPlots_for_Subject_Clusters = "var BoxPlot_of_Subject_Clusters = " + str(Number_of_BoxPlots_for_Subject_Clusters) + ";"
    Map_width = 'var Map_width  = "' + Map_width + '";'
    Map_height = 'var Map_height = "' + Map_height + '";'
    
    
    contents = contents.replace('var SubjectName = "";', SubjectName)
    contents = contents.replace("var InitialLayers = [];", InitialLayers)
    contents = contents.replace("var allMetros = false;", allMetros)
    contents = contents.replace("var Index_of_neighborhood_change = true;", Index_of_neighborhood_change)
    contents = contents.replace("var Maps_of_neighborhood = true;", Maps_of_neighborhood)
    contents = contents.replace("var Distribution_INC1 = true;", Distribution_INC1)
    contents = contents.replace("var Distribution_INC2_different_period = true;", Distribution_period)
    contents = contents.replace("var Distribution_INC2_different_cluster = true;", Distribution_cluster)
    contents = contents.replace("var Temporal_change_in_neighborhoods = true;", Temporal_change_in_neighborhoods)
    contents = contents.replace("var Parallel_Categories_Diagram_in_neighborhoods = true;", Parallel_Categories_Diagram_in_neighborhoods)
    contents = contents.replace("var Chord_Diagram_in_neighborhoods = true;", Chord_Diagram_in_neighborhoods)
    contents = contents.replace("var Zscore_Means_across_Clusters = true;", Zscore_Means_across_Clusters)
    contents = contents.replace("var Zscore_Means_of_Each_Cluster = true;", Zscore_Means_of_Each_Cluster)
    contents = contents.replace("var Barchart_of_Subject_Clusters = 0;", Number_of_Barcharts_for_Subject_Clusters)
    contents = contents.replace("var BoxPlot_of_Subject_Clusters = 0;", Number_of_BoxPlots_for_Subject_Clusters)
    contents = contents.replace('var Map_width  = "400px";', Map_width)
    contents = contents.replace('var Map_height = "400px";', Map_height)
    
    #Write output including the replacement above
    filename_GEO_CONFIG = "VNE_" + param['filename_suffix'] + "/data/GEO_CONFIG_"+param['filename_suffix']+".js"
    ofile = open(filename_GEO_CONFIG, 'w')
    ofile.write(contents)
    ofile.close()


def write_ALL_METROS_GEO_CONFIG_js(param):
    # read GEO_CONFIG.js
    ifile = open("template/ACM_GEO_CONFIG.js", "r")
    contents = ifile.read()
    
    Stacked_Chart = False;
    Correlogram = False;
    Scatter_Plot = False;               
    Parallel_Coordinates_Plot = False;                  
    
    # perpare parameters
    NumOfMaps = 1
    InitialLayers = ["INC"]
    
    # Automatically set Map_width, Map_height. 
    Map_width = "1400px"
    Map_height = "800px"
    
    # replace newly computed "NumOfMaps", "InitialLayers", "Map_width", "Map_height" in CONFIG.js. See the example replacement below
    NumOfMaps = "var NumOfMaps = " + str(NumOfMaps) + ";"
    InitialLayers = "var InitialLayers = " + json.dumps(InitialLayers) + ";"
    Initial_map_center = "var Initial_map_center = [37, -98.5795];"
    Initial_map_zoom_level = "var Initial_map_zoom_level = 5;"
    Map_width = 'var Map_width  = "' + Map_width + '";'
    Map_height = 'var Map_height = "' + Map_height + '";'
    
    contents = contents.replace("var NumOfMaps = 1;", NumOfMaps)
    contents = contents.replace("var InitialLayers = [];", InitialLayers)
    contents = contents.replace("//var Initial_map_center = [34.0522, -117.9];", Initial_map_center)
    contents = contents.replace("//var Initial_map_zoom_level = 8;", Initial_map_zoom_level)
    contents = contents.replace('var Map_width  = "400px";', Map_width)
    contents = contents.replace('var Map_height = "400px";', Map_height)
    
    #Stacked_Chart = "var Stacked_Chart = false;"
    #Correlogram = "var Correlogram = false;"
    #Scatter_Plot = "var Scatter_Plot = false;"
    #Parallel_Coordinates_Plot = "var Parallel_Coordinates_Plot = false;"
    
    #contents = contents.replace("var Stacked_Chart = false;", Stacked_Chart)
    #contents = contents.replace("var Correlogram = false;", Correlogram)
    #contents = contents.replace("var Scatter_Plot = false;", Scatter_Plot)
    #contents = contents.replace("var Parallel_Coordinates_Plot = false;", Parallel_Coordinates_Plot)
    
    #Write output including the replacement above
    filename_GEO_CONFIG = "VNE_" + param['filename_suffix'] + "/data/GEO_CONFIG_"+param['filename_suffix']+".js"
    ofile = open(filename_GEO_CONFIG, 'w')
    ofile.write(contents)
    ofile.close()


def write_GEO_JSON_js(community, param):
    
    # open GEO_JSON.js write heading for geojson format
    filename_GEO_JSON = "VNE_" + param['filename_suffix'] + "/data/GEO_JSON_"+param['filename_suffix']+".js"
    ofile = open(filename_GEO_JSON, 'w')
    ofile.write('var GEO_JSON =\n')
    ofile.write('{"type":"FeatureCollection", "features": [\n')
    
    
    geoid = community.gdf.columns[0]
    #if (geoid != ""): geoid = "geoid"
    
    if ('geometry' in community.gdf):                                       # query geometry for each tract
        # Convert geometry in GEOJSONP to geojson format
        tracts = community.gdf[[geoid, 'geometry']].copy()
        tracts.drop_duplicates(subset=geoid, inplace=True)					# get unique geoid
        #print(tracts)
        aSeries = tracts.iloc[0]
        #print(aSeries)
        #print("geoid:", aSeries['geoid'], type(aSeries['geoid']))
        #print("geometry:", type(aSeries['geometry']))
        wCount = 0
        for tract in tracts.itertuples():
            feature = {"type":"Feature"}
            #print(type(tract.geometry))
            if (type(tract.geometry) is float):								# check is NaN?
                #print(tract.geometry)
                continue
            if (isinstance(tract.geometry, str)):                           # if input is from csv files.
                geometry = shapely.wkt.loads(tract.geometry)
            else:
                geometry = tract.geometry
            feature["geometry"] = shapely.geometry.mapping(geometry)
            #print(type(feature["geometry"]))
            #feature["properties"] = {geoid: tract.__getattribute__(geoid), "tractID": tract.__getattribute__(geoid)}
            feature["properties"] = {geoid: tract.__getattribute__(geoid)}
            wCount += 1
            ofile.write(json.dumps(feature)+',\n')
        #print("GEO_JSON.js write count:", wCount)
    else:                                                                   # use shape file
        # read shape file to df_shape
        df_shape = gpd.read_file(param['shapefile'])
        df_shape = df_shape.astype(str)     
        print("shapefile:  " + df_shape.GEOID10)        
        df_shape = df_shape.set_index("GEOID10")
        #print(df_shape)
        #aGeoSeries = df_shape.iloc[0]
        #print(aGeoSeries)
        #print("GEOID10:", aGeoSeries['GEOID10'], type(aGeoSeries['GEOID10']))
        #print("NAME:", aGeoSeries['NAME'], type(aGeoSeries['NAME']))
        #print("COUNTY_ID:", aGeoSeries['COUNTY_ID'], type(aGeoSeries['COUNTY_ID']))
        #print("geometry:", type(aGeoSeries['geometry']))
        # Convert geometry in shape file to geojson format
        wCount = 0
        for index, row in community.gdf.iterrows():
            feature = {"type":"Feature"}
            tractid = row[geoid]
            #print("tractid", tractid, type(tractid))
            try:
                tract = df_shape.loc[tractid]
                #print(tract)
                if (type(tract.geometry) is float):		                    # check is NaN?
                    print("Tract ID [{}] has no geometry value in the shape file {}".format(tractid, param['shapefile']))
                    continue
                if (isinstance(tract.geometry, str)):                       # if input is from csv files.
                    geometry = shapely.wkt.loads(tract.geometry)
                else:
                    geometry = tract.geometry
            except KeyError:
                print("Tract ID [{}] is not found in the shape file {}".format(tractid, param['shapefile']))
                continue
            
            #tract = df_shape.loc[tractid]
            #print(tract)
            #if (tract.size == 0 or type(tract.geometry) is float):		    # check is NaN?
            #	print("Tract ID [{}] is not found in the shape file {}".format(tractid, param['shapefile']))
            #	continue
            #if (isinstance(tract.geometry, str)):                           # if input is from csv files.
            #	geometry = shapely.wkt.loads(tract.geometry)
            #else:
            #	geometry = tract.geometry
            feature["geometry"] = shapely.geometry.mapping(geometry)
            #feature["properties"] = {geoid: int(tractid)}
            feature["properties"] = {geoid: tractid}
            wCount += 1
            ofile.write(json.dumps(feature)+',\n')
        #print("GEO_JSON.js write count:", wCount)
        
    # complete the geojosn format by adding parenthesis at the end.	
    ofile.write(']}\n')
    ofile.close()


def write_ALL_METROS_JSON_js(metros, param):
    # query geometry for each tract
    geoid = metros.columns[0]
    tracts = metros[[geoid, 'name', 'geometry']].copy()
    tracts.drop_duplicates(subset=geoid, inplace=True)					# get unique geoid
    #print(tracts)
    
    # open GEO_JSON.js write heading for geojson format
    filename_GEO_JSON = "VNE_" + param['filename_suffix'] + "/data/GEO_JSON_"+param['filename_suffix']+".js"
    ofile = open(filename_GEO_JSON, 'w')
    ofile.write('var GEO_JSON =\n')
    ofile.write('{"type":"FeatureCollection", "features": [\n')
    
    #Convert geometry in GEOJSONP to geojson format
    wCount = 0
    for tract in tracts.itertuples():
        feature = {"type":"Feature"}
        if (type(tract.geometry) is float):								# check is NaN?
            #print(tract.geometry)
            continue
        feature["geometry"] = shapely.geometry.mapping(tract.geometry)
        #feature["properties"] = {geoid: tract.__getattribute__(geoid), "tractID": tract.__getattribute__(geoid)}
        feature["properties"] = {geoid: tract.geoid, 'metro': tract.name}
        wCount += 1
        ofile.write(json.dumps(feature)+',\n')
    #print("GEO_JSON.js write count:", wCount)
    # complete the geojosn format by adding parenthesis at the end.	
    ofile.write(']}\n')
    ofile.close()


def write_GEO_VARIABLES_js(community, param):
    #print(param)
    geoid       = community.gdf.columns[0]
    method      = param['method']
    nClusters   = param['nClusters']
    years       = param['years']
    variables   = param['variables']
    labels      = param['labels']
    
    rate1_surfix = ""
    rate1_dividend_surfix = ""
    rate1_divisor_surfix = ""  
    if ('rate1' in param):
        #print(param['rate1'])
        rate1_surfix = "_" + param['rate1'].split('=')[0].strip()
        rate1_dividend_surfix = param['rate1'].split('=')[1].split('/')[0].strip()
        rate1_divisor_surfix = param['rate1'].split('=')[1].split('/')[1].strip()
        #print("rate1_surfix:", rate1_surfix)
        #print("rate1_dividend_surfix:", rate1_dividend_surfix)
        #print("rate1_divisor_surfix:", rate1_divisor_surfix)
    
    rate2_surfix = ""
    rate2_dividend_surfix = ""
    rate2_divisor_surfix = ""  
    if ('rate2' in param):
        #print(param['rate2'])
        rate2_surfix = "_" + param['rate2'].split('=')[0].strip()
        rate2_dividend_surfix = param['rate2'].split('=')[1].split('/')[0].strip()
        rate2_divisor_surfix = param['rate2'].split('=')[1].split('/')[1].strip()
        #print("rate2_surfix:", rate2_surfix)
        #print("rate2_dividend_surfix:", rate2_dividend_surfix)
        #print("rate2_divisor_surfix:", rate2_divisor_surfix)
    
    sb_surfix = ""                               # sb: subject Normalization
    sb_variables = ""
    sb_multiplier = 0.0
    sb_divisor = {}                              # key: denominator,  value: divisor
    df_divisor = None
    df_normalization = None
    if ('subjectNormalization' in param and 'subjectNormalizationCSV' in param):
        df_normalization = pd.read_csv(param['subjectNormalizationCSV'])
        #print(df_normalization)
	
        denominator = df_normalization.columns[0]
        divisor = df_normalization.columns[1]
        
        sb0 = param['subjectNormalization'].split('=')[0].strip()
        sb1 = param['subjectNormalization'].split('=')[1].strip()
        sb10 = sb1.split('*')[0].strip()
        sb11 = sb1.split('*')[1].strip()
        sb110 = sb11.split('/')[0].strip()
        sb111 = sb11.split('/')[1].strip()
        sb_surfix = " " + sb0
        sb_variables = sb10
        sb_multiplier = float(sb110)
        #sb_divisor = sb111
        sb_divisor = pd.Series(df_normalization[divisor].values,index=df_normalization[denominator]).to_dict()
        #print("{} = {} * {} / {}".format(sb_surfix, sb_variables, sb_multiplier, sb111))
        #print(sb_divisor)
        
        # get columns list for df_divisor from df_normalization[divisor]
        sb_divisors = df_normalization[divisor].values.tolist()
        seen = set()
        seen_add = seen.add
        sb_columns = [x for x in sb_divisors if not(x in seen or seen_add(x))]
        sb_columns.insert(0, "geoid")
        #print("sb_columns:", sb_columns)
        
        # create df_divisor from community.gdf with sb_columns
        df_divisor = community.gdf[community.gdf['year'] == param['years'][-1]]    # last year
        df_divisor = df_divisor[sb_columns]
        df_divisor = df_divisor.set_index('geoid')
    
    seqClusters = 5
    distType    = 'tran'
    #if ('Sequence' in param and type(param['Sequence']) is dict and 'seq_clusters' in param['Sequence']): 
    #	seqClusters = param['Sequence']['seq_clusters']
    #if ('Sequence' in param and type(param['Sequence']) is dict and 'dist_type' in param['Sequence']): 
    #	distType = param['Sequence']['dist_type']
    
    if ('Sequence' in param and type(param['Sequence']) is dict):
        if ('seq_clusters' in param['Sequence']): seqClusters = param['Sequence']['seq_clusters']
        if ('dist_type' in param['Sequence']): distType = param['Sequence']['dist_type']
    
    # filtering by years
    community.gdf = community.gdf[community.gdf.year.isin(years)]
    #print(community.gdf)
    #community.gdf.to_csv(r'output.csv')    
    
    
    # clustering by method, nClusters with filtering by variables
    #clusters = geosnap.analyze.cluster(community, method=method, n_clusters=nClusters, columns=variables)
    #df = clusters.census[['year', method]]
    
    if (method == 'kmeans' or method == 'ward' or method == 'affinity_propagation' or method == 'spectral' or method == 'gaussian_mixture' or method == 'hdbscan'):
        clusters = community.cluster(columns=variables, method=method, n_clusters=nClusters)
    if (method == 'ward_spatial' or method == 'spenc' or method == 'skater' or method == 'azp' or method == 'max_p'):
        clusters = community.cluster_spatial(columns=variables, method=method, n_clusters=nClusters)		
    #print(clusters.gdf.columns)
    #print(clusters.gdf)
    #print(clusters.gdf[['year', 'geoid', 'kmeans']])
    nClusters = -1
    clusterDic = {}
    for i, row in clusters.gdf.iterrows():
        c = row[method]
        #print(type(c), c)
        if (isinstance(c, str)):
            if (nClusters < int(c)): nClusters = int(c)
        else:
            c = "None"
        if (c in clusterDic):
            clusterDic[c] += 1
        else:
            clusterDic[c] = 1
    nClusters += 1
    #print("nClusters:", nClusters)
    #print(clusterDic)
    
    
    # Use the sequence method to obtain the distance matrix of neighborhood sequences
    gdf_new, df_wide, seq_dis_mat = clusters.sequence(seq_clusters=seqClusters, dist_type=distType, cluster_col=method)
    #print(df_wide)
    
    # pivot by year column
    #df_pivot = df.reset_index().pivot(geoid, "year", method)
    df_pivot = df_wide
    lastColumn = df_pivot.columns[df_pivot.shape[1]-1]					# get the last column name as like 'tran-5'
    df_pivot.rename(columns={lastColumn: 'Sequence'}, inplace=True)		# change the last column name to 'Sequence'
    #print(df_pivot)
    
    if (len(years) > 1):
        # convert df_pivot to list for INCS.linc
        yearList = []
        #for year in df_pivot.columns:
        for year in years:
            aYearList = df_pivot[year].values.tolist()
            aYearList = list(map(float, aYearList)) 
            yearList.append(aYearList)
        #print(yearList)
        # calculate INC
        incs = linc(yearList)
        #print(incs)
        #incs = minmax_scale(incs, feature_range=(0,1), axis=0)
        #print(incs)		
        # insert INC to first column of df_pivot
        df_pivot.insert(loc=0, column='INC', value=incs)
    
    if ('Sequence' not in param or not param['Sequence']): df_pivot.drop(columns=['Sequence'], inplace=True)
    #if ('Sequence' not in param or type(param['Sequence']) is not dict): df_pivot.drop(columns=['Sequence'], inplace=True)
    #print(df_pivot)
    
    # calculate zscore
    clusters_flattened = pd.DataFrame(df_pivot.to_records())                   # convert pivot to data frame
    geoids = clusters_flattened["geoid"].tolist()                              # get list of geoids from pivot
    valid_gdf = community.gdf[community.gdf.geoid.isin(geoids)]                # get all rows of valid geoids from community.gdf
    #print("clusters_flattened:", clusters_flattened)
    #print("geoids: ", len(geoids))
    #print("geoids:", geoids)
    #print("valid_gdf:", valid_gdf)
    
    lastClusterNo = 0
    for y, year in enumerate(years):
        maxClusterNo_theYear = clusters_flattened[str(year)].max()
        if (lastClusterNo < maxClusterNo_theYear): 
            lastClusterNo = maxClusterNo_theYear
    #print("lastClusterNo:", lastClusterNo)
    nGeneratedClusters = lastClusterNo + 1
    
    # get sum of the each cluster and count of the each cluster
    zValue = [[0 for v in range(len(variables))] for c in range(nGeneratedClusters)]
    zCount = [[0 for v in range(len(variables))] for c in range(nGeneratedClusters)]
    for v, variable in enumerate(variables):
        #if (v > 0): break
        theVariable_pivot = valid_gdf.pivot(index='geoid', columns='year', values=variable)
        theVariable_flattened = pd.DataFrame(theVariable_pivot.to_records())   # convert pivot to data frame
        #print(theVariable_pivot)
        #print("theVariable_flattened: ", variable)
        #print(theVariable_flattened)
        if (theVariable_flattened.shape[0] != len(geoids)):                    # check number of pivot and valid geoids
            #print("Number of valid geoid not equal pivot of '" + variable +"'")
            #print("Number of geoids: ", len(geoids))
            #print("Number of pivot : ", theVariable_flattened.shape[0])
            continue
        
        # make a variable list of all years from pivot
        theVariableList = np.array([])
        for y, year in enumerate(years):
            theYearList = theVariable_flattened[str(year)].tolist()
            theVariableList = np.append(theVariableList, theYearList)
        #print("theVariableList: ", theVariableList.shape[0], theVariableList)
        
        theVariableZscore = stats.zscore(theVariableList)                      # calculate zscore
        #print("theVariableZscore: ", theVariableZscore.shape[0], theVariableZscore)
        for y, year in enumerate(years):
            i = y * clusters_flattened.shape[0]
            #print(y, clusters_flattened.shape[0], i)
            for j, row in clusters_flattened.iterrows():
                cluster = int(row[str(year)])
                #print("zValue[%d][%d] += theVariableZscore[%d]" % (cluster, v, i+j))
                zValue[cluster][v] += theVariableZscore[i+j]                   # accumulate zscore to the position of cluster
                zCount[cluster][v] += 1                                        # count up by 1 to the position of cluster
    #print(zValue)
    #print(zCount)
    
    # calculate average of zscore
    zScore = [[0 for v in range(len(variables))] for c in range(nGeneratedClusters)]
    for v, variable in enumerate(variables):
        for c in range(nGeneratedClusters):
            if (zCount[c][v] != 0): zScore[c][v] = round(zValue[c][v] / zCount[c][v], 2)
    #print(zScore)
    
    # calculate zScore_wAHb with white, Asian, Hispanic, black
    variables_wAHb = ["% white", "% Asian", "% Hispanic", "% black"]
    position_wAHb = []
    for j, variable in enumerate(variables_wAHb):
        p = next((k for k, v in enumerate(variables) if (v == variable)), -1)
        if (p != -1): position_wAHb.append(p)
    #print("position_wAHb:", position_wAHb)
    zScore_wAHb = None
    if (len(position_wAHb) == len(variables_wAHb)):        # if all 4 variables are found in the variables
        zScore_wAHb = [[None for v in range(len(variables_wAHb))] for c in range(nGeneratedClusters)]
        #print(zScore_wAHb)
        for c in range(nGeneratedClusters):
            m = sys.float_info.min
            j = -1
            for k, p in enumerate(position_wAHb):
                v = zScore[c][p]
                if (v > m): 
                    m = v
                    j = k
            zScore_wAHb[c][j] = m
        #print(zScore_wAHb)
        changeCluster = []
        for k in range(len(variables_wAHb)):
            maxValues = []
            for j in range(nGeneratedClusters):
                #print(k, j, zScore_wAHb[j], zScore_wAHb[j][k])
                if (zScore_wAHb[j][k] is not None):
                    maxValues.append([j, zScore_wAHb[j][k]])
            #print(k, maxValues)
            maxValues = sorted(maxValues, key=lambda l:l[1], reverse=True)
            #print(k, maxValues)
            for value in maxValues:
                changeCluster.append(value)
        #print(changeCluster)
        clusterChange = {c: -1 for c in range(nGeneratedClusters)}
        for c in range(len(changeCluster)):
            p = changeCluster[c][0]
            row = clusterChange[p]
            row = c
            clusterChange[p] = row
        #print(clusterChange)
    
    
    #for c in range(nGeneratedClusters):
    #	print("Cluster", c, zScore[c])
    #for v, variable in enumerate(variables):
    #	scores = []
    #	for c in range(nGeneratedClusters): 
    #		scores.append(zScore[c][v])
    #	print(variable, scores)
        
    df_disease = None
    if ('diseaseInputCSV' in param):
        df_disease = pd.read_csv(param['diseaseInputCSV'], dtype={'geoid':str})
        df_disease['geoid'] = df_disease['geoid']
        #print("df_disease:   " + df_disease.geoid)        
        df_disease = df_disease.set_index(geoid)
    
    
    
    # write df_pivot to GEO_VARIABLES.js
    filename_GEO_VARIABLES = "VNE_" + param['filename_suffix'] + "/data/GEO_VARIABLES_"+param['filename_suffix']+".js"
    geoVariablesList = []
    ofile = open(filename_GEO_VARIABLES, 'w')
    ofile.write('var GEO_VARIABLES =\n')
    ofile.write('[\n')
    #heading = [geoid, 'INC']
    #if (len(years) <= 1): heading = [geoid]
    #heading.extend(list(map(str, years)))
    heading = [geoid]
    heading.extend(list(map(str, df_pivot.columns.tolist())))
    dividends1 = []
    dividends2 = []
    if (df_disease is not None):                 # append heading and set dividends1 list
        for j, column in enumerate(df_disease.columns):
            heading.append(" "+column)
            #if (sb_surfix != ""):
            #    heading.append(" "+column+sb_surfix)
            if (sb_surfix != "" and column in sb_divisor):
                heading.append(" "+column+sb_surfix)
            dividends1.append(-1)
            if (rate1_surfix != "" and column[-len(rate1_divisor_surfix):] ==  rate1_divisor_surfix):
                rateColumnName = column[:-len(rate1_divisor_surfix)] + rate1_surfix
                dividendColName = column[:-len(rate1_divisor_surfix)] + rate1_dividend_surfix
                divisorColName = column
                d = next((k for k, v in enumerate(df_disease.columns) if (v == dividendColName)), -1)
                #print("{} = {} / {}  [{}]".format(rateColumnName, dividendColName, divisorColName, d))
                if (d >= 0):
                    heading.append(" "+rateColumnName)
                    dividends1[-1] = d
            dividends2.append(-1)
            if (rate2_surfix != "" and column[-len(rate2_divisor_surfix):] ==  rate2_divisor_surfix):
                rateColumnName = column[:-len(rate2_divisor_surfix)] + rate2_surfix
                dividendColName = column[:-len(rate2_divisor_surfix)] + rate2_dividend_surfix
                divisorColName = column
                d = next((k for k, v in enumerate(df_disease.columns) if (v == dividendColName)), -1)
                #print("{} = {} / {}  [{}]".format(rateColumnName, dividendColName, divisorColName, d))
                if (d >= 0):
                    heading.append(" "+rateColumnName)
                    dividends2[-1] = d
            #print(heading)
        #print(heading)
        #print(dividends1, dividends2)
        
        #for column in df_disease.columns:
        #	heading.append(" "+column)
    geoVariablesList.append(heading)
    ofile.write('  '+json.dumps(heading)+',\n')
    #print("df_disease:", df_disease.columns)
    wCount = 0
    for i, row in df_pivot.reset_index().iterrows():
        aLine = row.tolist()
        #aLine[0] = int(aLine[0])    # convert geoid to int
        #print("aLine:", aLine)
        if (df_disease is not None):
            try:
                aDisease = df_disease.loc[aLine[0]].tolist()
            except KeyError:
                #aDisease = [-9999] * df_disease.shape[1]
                aDisease = [0] * df_disease.shape[1]                 # 2020-07-05 page3
            #aLine.extend(aDisease)
            #if (sb_surfix != ""): populations = df_divisor.loc[aLine[0]][sb_divisor]
            for j, v in enumerate(aDisease):
                column = df_disease.columns[j]
                #print(j, column)
                aLine.append(v)
                #if (sb_surfix != ""):
                if (sb_surfix != "" and column in sb_divisor):
                    populations = df_divisor.loc[aLine[0]][sb_divisor[column]]
                    r = 0.0 if (populations == 0 or populations == -9999) else v * sb_multiplier / populations
                    aLine.append(round(r,2))
                if (dividends1[j] >= 0):
                    d = dividends1[j]
                    r = 0.0 if (v == 0) else aDisease[d] * 100.0 / v
                    if (r > 100): print("{}  {:<25}  {}%".format(aLine[0], df_disease.columns[d], round(r,2)))
                    aLine.append(round(r,2))
                if (dividends2[j] >= 0):
                    d = dividends2[j]
                    r = 0.0 if (v == 0) else aDisease[d] * 100.0 / v
                    if (r > 100): print("{}  {:<25}  {}%".format(aLine[0], df_disease.columns[d], round(r,2)))
                    aLine.append(round(r,2))
        for j, col in enumerate(aLine[2:], 2):
            try:
                #aLine[j] = int(col)                                 # convert float to int
                dummy = int(col)                                     # just check the value is Nan
            except ValueError:
                aLine[j] = -9999                                     # if Nan, set -9999
        wCount += 1
        geoVariablesList.append(aLine)
        if (i != df_pivot.shape[0]-1): ofile.write('  '+json.dumps(aLine)+',\n')
        else:                          ofile.write('  '+json.dumps(aLine)+'\n')
    #print("GEO_VARIABLES.js write count:", wCount)
    ofile.write(']\n')
    #print(df_pivot)              
    years = [str(year) for year in df_pivot.columns.tolist()]        # years must be column names as like ["2018", ..]
    #print("years:", type(years), years)
    df_geoVariables = pd.DataFrame(geoVariablesList[1:], columns=geoVariablesList[0])
    #print(df_geoVariables)
    #print(df_geoVariables[years])
    # convert values of df_geoVariables[years] using clusterChange dictionary
    for year in years:
        changedClusters = []
        for l, row in df_geoVariables.iterrows():
            changedClusters.append(clusterChange[row[year]])
        df_geoVariables[year] = changedClusters
    #print(df_geoVariables)
    filename_GEO_VARIABLES_CSV = "VNE_" + param['filename_suffix'] + "/data/CSV_VARIABLES_"+param['filename_suffix']+".csv"
    df_geoVariables.to_csv(filename_GEO_VARIABLES_CSV, index=False)
    
    # write zscore to GEO_VARIABLES.js
    geoZscoresList = []
    ofile.write('\n')
    ofile.write('var GEO_ZSCORES =\n')
    ofile.write('{\n')
    ofile.write('  "xAxis": [\n')
    for v, variable in enumerate(labels):
        if (v != len(labels)-1): ofile.write('    "'+variable+'",\n')
        else:                    ofile.write('    "'+variable+'"\n')
    ofile.write('  ],\n')
    heading = copy.deepcopy(labels)
    heading.insert(0, "Cluster")
    geoZscoresList.append(heading)
    ofile.write('  "yAxis": '+json.dumps(["C"+str(c) for c in range(nGeneratedClusters)])+',\n')
    ofile.write('  "data" : [\n')
    for z, row in enumerate(zScore):
        if (z != len(zScore)-1): ofile.write('    '+json.dumps(row)+',\n')
        else:                    ofile.write('    '+json.dumps(row)+'\n')
        aLine = copy.deepcopy(row)
        aLine.insert(0, "C"+str(z))
        geoZscoresList.append(aLine)
    ofile.write('  ]\n')
    ofile.write('}\n')
    #print(geoZscoresList)
    df_geoZscores = pd.DataFrame(geoZscoresList[1:], columns=geoZscoresList[0])
    #print(df_geoZscores)
    changedClusters = []
    for l, row in df_geoZscores.iterrows():
        changedClusters.append("C"+str(clusterChange[int(row['Cluster'][1:])]))
    df_geoZscores['Cluster'] = changedClusters
    #print(df_geoZscores)
    df_geoZscores = df_geoZscores.sort_values(df_geoZscores.columns[0])
    #print(df_geoZscores)
    filename_GEO_ZSCORES_CSV = "VNE_" + param['filename_suffix'] + "/data/CSV_ZSCORES_"+param['filename_suffix']+".csv"
    df_geoZscores.to_csv(filename_GEO_ZSCORES_CSV, index=False)
    
    if (df_disease is not None):
        #print(df_pivot)
        df_disease = df_disease.reset_index()
        #print(df_disease)
        countbycluster = {}
        for year in df_pivot.columns:
            #print("year:", year, type(year))
            #if (year == "INC" or year =="Sequence"): continue
            if (isinstance(year, str)): continue
            
            #populationsbycluster = [0] * nClusters
            populationsbycluster = {}            # key: colums,  value: [0] * nClusters
            #print(populationsbycluster)
            if (sb_surfix != ""): 
                df_divisor = community.gdf[community.gdf['year'] == year]
                #populations = df_divisor.loc[aLine[0]][sb_divisor[column]]
                #df_divisor = df_divisor[['geoid', sb_divisor]]
                df_divisor = df_divisor[sb_columns]
                df_divisor = df_divisor.set_index('geoid')
                #print(df_divisor)
                
                for i, row in df_disease.iterrows():
                    #if (i > 5): break
                    if (row['geoid'] in df_pivot.index):
                        c = df_pivot.loc[row['geoid']][year]
                        #print(c, df_pivot.loc[row['geoid']])
                        #populations = df_divisor.loc[row['geoid']][sb_divisor]
                        #if (populations != -9999):
                        #    populationsbycluster[c] += populations
                        for column in sb_columns[1:]:
                            populations = df_divisor.loc[row['geoid']][column]
                            if (populations != -9999):
                                if (column not in populationsbycluster):
                                    populationsbycluster[column] = [0] * nClusters
                                populationsbycluster[column][c] += populations
                #print(populationsbycluster)	
            
            countbycluster[year] = {i:[i]+[0]*(df_disease.shape[1]-1) for i in range(nClusters)}
            #print(countbycluster[year])
            for i, row in df_disease.iterrows():
                #if (i > 5): break
                if (row['geoid'] in df_pivot.index):
                    c = df_pivot.loc[row['geoid']][year]
                    for k in range(1, row.size):
                        countbycluster[year][c][k] += row.iloc[k]
            #print(countbycluster[year])
            
            #if ('countbyClusterCSV' in param):
            #	p = param['countbyClusterCSV'].rfind('.')                  # get start position of the file surfix
            #	countCSV = param['countbyClusterCSV']
            #	if (p > 1): countCSV = param['countbyClusterCSV'][:p]      # delete the file surfix
            #	countCSV = countCSV + "_" + str(year) + ".csv"
            #	csvfile = open(countCSV, 'w', newline='\n', encoding='utf-8')
            #	csvwriter = csv.writer(csvfile)
            #	header = [h for h in df_disease.columns]
            #	header[0] = "cluster " + str(year)
            #	#print(header)
            #	csvwriter.writerow(header)
            #	for i in range(len(countbycluster[year])):
            #		#print(countbycluster[year][i])
            #		csvwriter.writerow(countbycluster[year][i])
            #	csvfile.close()
        #print(countbycluster)
        
        # write disease cluster to GEO_VARIABLES.js
        geoClusterList = []
        ofile.write('\n')
        ofile.write('var GEO_CLUSTER =\n')
        ofile.write('{\n')
        
        dividends1 = []
        dividends2 = []
        for j, column in enumerate(df_disease.columns):
            #heading.append(" "+column)
            dividends1.append(-1)
            if (rate1_surfix != "" and column[-len(rate1_divisor_surfix):] ==  rate1_divisor_surfix):
                rateColumnName = column[:-len(rate1_divisor_surfix)] + rate1_surfix
                dividendColName = column[:-len(rate1_divisor_surfix)] + rate1_dividend_surfix
                divisorColName = column
                d = next((k for k, v in enumerate(df_disease.columns) if (v == dividendColName)), -1)
                #print("{} = {} / {}  [{}]".format(rateColumnName, dividendColName, divisorColName, d))
                if (d >= 0):
                    #heading.append(" "+rateColumnName)
                    dividends1[-1] = d
            dividends2.append(-1)
            if (rate2_surfix != "" and column[-len(rate2_divisor_surfix):] ==  rate2_divisor_surfix):
                rateColumnName = column[:-len(rate2_divisor_surfix)] + rate2_surfix
                dividendColName = column[:-len(rate2_divisor_surfix)] + rate2_dividend_surfix
                divisorColName = column
                d = next((k for k, v in enumerate(df_disease.columns) if (v == dividendColName)), -1)
                #print("{} = {} / {}  [{}]".format(rateColumnName, dividendColName, divisorColName, d))
                if (d >= 0):
                    #heading.append(" "+rateColumnName)
                    dividends2[-1] = d
        #print(dividends1, dividends2)
        
        yCount = 0
        for year, value in countbycluster.items():
            yCount += 1
            #print(year)
            #print(value)
            heading = ["C"+str(c) for c in range(nClusters)]
            heading.insert(0, year)
            geoClusterList.append(heading)
            ofile.write('  "' + str(year) + '":\n')
            ofile.write('    [\n')
            for l in range(1,df_disease.shape[1]):
                aLine = [df_disease.columns[l]]
                column = df_disease.columns[l]
                #print(aLine)
                for c in range(nClusters):
                    aLine.append(value[c][l])
                #print(l, aLine)
                geoClusterList.append(aLine)
                #ofile.write('      '+json.dumps(aLine)+',\n')
                if (sb_surfix != "" and column in sb_divisor):
                    aLine = [df_disease.columns[l] + sb_surfix]
                    for c in range(nClusters):
                        r = 0.0 if (populationsbycluster[sb_divisor[column]][c] == 0) else value[c][l]*sb_multiplier/populationsbycluster[sb_divisor[column]][c]
                        #aLine.append(value[c][l]*sb_multiplier/populationsbycluster[c])
                        aLine.append(round(r,2))
                    #print(l, aLine)
                    geoClusterList.append(aLine)
                    #ofile.write('      '+json.dumps(aLine)+',\n')
                    
                if (dividends1[l] >= 0):
                    aLine = [df_disease.columns[l][:-len(rate1_divisor_surfix)] + rate1_surfix]
                    #rateColumnName = column[:-len(rate1_divisor_surfix)] + rate1_surfix
                    d = dividends1[l]
                    for c in range(nClusters):
                        #aLine.append(value[c][l])
                        v = value[c][l]
                        r = 0.0 if (v == 0) else value[c][d] * 100.0 / v
                        if (r > 100): print("{}  {:<25}  {}%".format(aLine[0], df_disease.columns[d], round(r,2)))
                        aLine.append(round(r,2))
                    #print(l, aLine)
                    geoClusterList.append(aLine)
                    #ofile.write('      '+json.dumps(aLine)+',\n')
                if (dividends2[l] >= 0):
                    aLine = [df_disease.columns[l][:-len(rate2_divisor_surfix)] + rate2_surfix]
                    #rateColumnName = column[:-len(rate1_divisor_surfix)] + rate2_surfix
                    d = dividends2[l]
                    for c in range(nClusters):
                        #aLine.append(value[c][l])
                        v = value[c][l]
                        r = 0.0 if (v == 0) else value[c][d] * 100.0 / v
                        if (r > 100): print("{}  {:<25}  {}%".format(aLine[0], df_disease.columns[d], round(r,2)))
                        aLine.append(round(r,2))
                    #print(l, aLine)
                    geoClusterList.append(aLine)
                    #ofile.write('      '+json.dumps(aLine)+',\n')
            for l in range(1, len(geoClusterList)):
                aLine = geoClusterList[l]
                #print('      '+json.dumps(aLine)+',/n')
                if (l != len(geoClusterList)-1): ofile.write('      '+json.dumps(aLine)+',\n')
                else:                            ofile.write('      '+json.dumps(aLine)+'\n')
            if (yCount != len(countbycluster)): ofile.write('    ],\n')
            else:                               ofile.write('    ]\n')	
        
            #print(geoClusterList)
            df_geoCluster = pd.DataFrame(geoClusterList[1:], columns=geoClusterList[0])
            #print(df_geoCluster)
            changedClusters = []
            for column in df_geoCluster.columns:
                if (isinstance(column, str)): column = "C" + str(clusterChange[int(column[1:])])
                else: column = str(column)
                changedClusters.append(column)
            #print(changedClusters)
            df_geoCluster.columns = changedClusters
            df_geoCluster = df_geoCluster.reindex(sorted(df_geoCluster.columns), axis=1)
            #print(df_geoCluster)
            filename_GEO_ZSCORES_CSV = "VNE_" + param['filename_suffix'] + "/data/CSV_CLUSTER_"+param['filename_suffix']+"_"+str(year)+".csv"
            df_geoCluster.to_csv(filename_GEO_ZSCORES_CSV, index=False)
        ofile.write('}\n')
        
        if (zScore_wAHb is not None):
            aLine = "var CHANGE_CLUSTER = "
            #aLine += json.dumps(clusterChange).replace('"','') + ";"
            aLine += json.dumps(clusterChange)
            #print(aLine)
            ofile.write('\n'+aLine+'\n')
    
        
    ofile.close()



def write_ALL_METROS_VARIABLES_js(metros, param):
    geoid       = metros.columns[0]
    method      = param['method']
    nClusters   = param['nClusters']
    years       = param['years']
    variables   = param['variables']
    seqClusters = 5
    distType    = 'tran'
    
    if ('Sequence' in param and type(param['Sequence']) is dict):
        if ('seq_clusters' in param['Sequence']): seqClusters = param['Sequence']['seq_clusters']
        if ('dist_type' in param['Sequence']): distType = param['Sequence']['dist_type']
    
    #msas = data_store.msa_definitions
    #for column in msas.columns:
    #	print(column)
    #print(msas)
    
    #community = Community.from_ltdb(years=years, msa_fips="10220")
    #community = Community.from_ltdb(years=years)
    #community.gdf = community.gdf[['geoid', 'year']]
    #print(community.gdf)
    #print(variables)
    #print(variables.append(['geoid', 'year']))
    #print(variables)
    #return
    
    # Initial call to print 0% progress
    printProgressBar(0, len(metros.index), prefix = 'Progress:', suffix = 'Complete', length = 50)
    
    readCount = 0
    outList = []
    for index, metro in metros.iterrows():
        #if (index > 10): break
        #if (index != 3): continue
        #print(index, metro['geoid'], metro['name'])
        metroid = metro['geoid']
        p = metro['name'].rfind(', ')
        #if (p < 0): print(index, metro['geoid'], metro['name'], p)
        metroname = metro['name'][:p]
        stateabbr = metro['name'][p+2:]
        #print(index, metroid, stateabbr, metroname)
        
        try:
            community = Community.from_ltdb(years=years, msa_fips=metroid)
        except ValueError:
            continue
        #printProgressBar(index, len(metros.index), prefix = 'Progress:', suffix = 'Complete', length = 50)
        #continue
        
        if (len(community.gdf.index) <= 0): continue
        #print(community.gdf.columns)
        #for column in community.gdf.columns:
        #	print(column)
        #print(community)
        #print(community.gdf)
        
        # clustering by method, nClusters with filtering by variables
        try:
            clusters = community.cluster(columns=variables, method=method, n_clusters=nClusters)
        except KeyError:
            continue
        #print(clusters.gdf)
        #print(clusters.gdf[['year', 'geoid', 'kmeans']])
        
        # get pivot from clusters
        df_pivot = clusters.gdf.pivot(index='geoid', columns='year', values='kmeans')
        #print(df_pivot)
        #print(len(df_pivot.index))
        #print(df_pivot.columns)
        
        if (len(df_pivot.columns) > 1):										# 1980, 1990, 2000, 2010
            # convert df_pivot to list for INCS.linc
            yearList = []
            for year in df_pivot.columns:
                aYearList = df_pivot[year].values.tolist()
                aYearList = list(map(float, aYearList)) 
                yearList.append(aYearList)
            #print(yearList)
            # calculate INC
            incs = linc(yearList)
            #print(incs)
            ave = sum(incs) / len(incs) if (len(incs) != 0) else -9999
            #print("ave:", ave)
            #print(index, metroid, ave, stateabbr, metroname)
            readCount += len(incs)
            outList.append([metroid, ave])
            printProgressBar(index, len(metros.index), prefix = 'Progress:', suffix = 'Complete', length = 50)
    printProgressBar(len(metros.index), len(metros.index), prefix = 'Progress:', suffix = 'Complete', length = 50)
    #print(outList)
    print("readCount:", readCount)
    
    # write df_pivot to GEO_VARIABLES.js
    filename_GEO_VARIABLES = "VNE_" + param['filename_suffix'] + "/data/GEO_VARIABLES_"+param['filename_suffix']+".js"
    ofile = open(filename_GEO_VARIABLES, 'w')
    ofile.write('var GEO_VARIABLES =\n')
    ofile.write('[\n')
    heading = [geoid, 'INC']
    ofile.write('  '+json.dumps(heading)+',\n')
    wCount = 0
    for i, row in enumerate(outList):
        wCount += 1
        ofile.write('  '+json.dumps(row)+',\n')
    #print("GEO_VARIABLES.js write count:", wCount)
    ofile.write(']\n')
    ofile.close()


def write_ALL_METROS_VARIABLES_js(metros, param):
    geoid       = metros.columns[0]
    method      = param['method']
    nClusters   = param['nClusters']
    years       = param['years']
    variables   = param['variables']
    seqClusters = 5
    distType    = 'tran'
    
    if ('Sequence' in param and type(param['Sequence']) is dict):
        if ('seq_clusters' in param['Sequence']): seqClusters = param['Sequence']['seq_clusters']
        if ('dist_type' in param['Sequence']): distType = param['Sequence']['dist_type']
    
    printProgressBar(-1, len(metros.index), prefix = 'Progress:', suffix = 'Initializing', length = 50)
    
    #states = data_store.states(convert=False)								# [56 rows x 3 columns]
    states = datasets.states(convert=False)
    #print(states)
    #print(states["geoid"].tolist())
    
    #counties = data_store.counties(convert=False)							# [3233 rows x 2 columns]
    counties = datasets.counties(convert=False)
    #print(counties)
    
    #ltdb = data_store.ltdb													# [330388 rows x 192 columns]
    ltdb = datasets.ltdb
    #for column in ltdb.columns:
    #	print(column)
    #print(ltdb.memory_usage(index=True, deep=True).sum())
    #print(ltdb)
    
    #msas = data_store.msa_definitions										# [1915 rows x 13 columns]
    msas = datasets.msa_definitions
    #for column in msas.columns:
    #	print(column)
    msas.set_index('stcofips', inplace=True)
    #print(msas)
    #print(msas.loc['48505', 'CBSA Code'])
    
    community = Community.from_ltdb(years=years, state_fips=states["geoid"].tolist())
    #community = Community.from_ltdb(state_fips=states["geoid"].tolist())	# [330388 rows x 194 columns]
    #community = Community.from_ltdb(years=years)
    #community.gdf = community.gdf[['geoid', 'year']]
    #for column in community.gdf.columns:
    #	print(column)
    
    #community.gdf['metroid'] = None
    metroids = []
    for index, row in community.gdf.iterrows():
        stcofips = row['geoid'][:5]
        try:
            metroids.append(msas.loc[stcofips, 'CBSA Code'])
        except KeyError:
            metroids.append(None)
    community.gdf.insert(0, "stcofips", metroids, True)
    #print(community.gdf.memory_usage(index=True, deep=True).sum())
    #print(community.gdf)
    #print(variables)
    #print(['geoid', 'year'] + variables)
    #print(variables)
    
    allgdf = community.gdf[['stcofips', 'geoid', 'year'] + variables].copy()
    allgdf.set_index('stcofips', inplace=True)
    #print(allgdf.memory_usage(index=True, deep=True).sum())
    #print(allgdf)
    
    #community.gdf = allgdf.loc['10220']
    #clusters = community.cluster(columns=variables, method=method, n_clusters=nClusters)
    #print(clusters.gdf)
    
    # Initial call to print 0% progress
    printProgressBar(0, len(metros.index), prefix = 'Progress:', suffix = 'Complete      ', length = 50)
    
    readCount = 0
    outList = []
    for index, metro in metros.iterrows():
        #if (index > 10): break
        #if (index != 3): continue
        #print(index, metro['geoid'], metro['name'])
        metroid = metro['geoid']
        p = metro['name'].rfind(', ')
        #if (p < 0): print(index, metro['geoid'], metro['name'], p)
        metroname = metro['name'][:p]
        stateabbr = metro['name'][p+2:]
        #print(index, metroid, stateabbr, metroname)
        
        #msa_fips = metroid
        #fips_list = []
        #if msa_fips:
        #	fips_list += data_store.msa_definitions[
        #		data_store.msa_definitions["CBSA Code"] == msa_fips
        #	]["stcofips"].tolist()
        ##print(metroid, fips_list)
        #
        #dfs = []
        #for fips_code in fips_list:
        #	#dfs.append(data[data.geoid.str.startswith(index)])
        #	dfs.append(allgdf[allgdf.geoid.str.startswith(fips_code)])
        #if (len(dfs) == 0): continue
        ##print(type(dfs))
        ##print(dfs)
        
        try:
            #community = Community.from_ltdb(years=years, msa_fips=metroid)
            community.gdf = allgdf.loc[metroid]
            #community.gdf = allgdf.loc[allgdf['stcofips']==metroid]
            #community.gdf = pd.concat(dfs)
            #print(community.gdf)
        #except ValueError:
        except KeyError:
            continue
        #printProgressBar(index, len(metros.index), prefix = 'Progress:', suffix = 'Complete', length = 50)
        #continue
        
        if (len(community.gdf.index) <= 0): continue
        #print(community.gdf.columns)
        #for column in community.gdf.columns:
        #	print(column)
        #print(community)
        #community.gdf.to_csv(r'output.csv')
        #print(community.gdf)
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")		
        # clustering by method, nClusters with filtering by variables
        #try:
        if (method == 'kmeans' or method == 'ward' or method == 'affinity_propagation' or method == 'spectral' or method == 'gaussian_mixture' or method == 'hdbscan'):
            try:
                clusters = community.cluster(columns=variables, method=method, n_clusters=nClusters)
            except KeyError:
                continue
                
        if (method == 'ward_spatial' or method == 'spenc' or method == 'skater' or method == 'azp' or method == 'max_p'):
            try:
                clusters = community.cluster_spatial(columns=variables, method=method, n_clusters=nClusters) #, spatial_weights='rook'
            except KeyError:
                continue
        #except KeyError:
        #	continue
        #print(clusters.gdf)
        #print(clusters.gdf[['year', 'geoid', 'kmeans']])
        
        # get pivot from clusters
        df_pivot = clusters.gdf.pivot(index='geoid', columns='year', values='kmeans')
        #print(df_pivot)
        #print(len(df_pivot.index))
        #print(df_pivot.columns)
        
        if (len(df_pivot.columns) > 1):										# 1980, 1990, 2000, 2010
            # convert df_pivot to list for INCS.linc
            yearList = []
            for year in df_pivot.columns:
                aYearList = df_pivot[year].values.tolist()
                aYearList = list(map(float, aYearList)) 
                yearList.append(aYearList)
            #print(yearList)
            # calculate INC
            incs = linc(yearList)
            #print(incs)
            ave = sum(incs) / len(incs) if (len(incs) != 0) else -9999
            #print("ave:", ave)
            #print(index, metroid, ave, stateabbr, metroname)
            readCount += len(incs)
            outList.append([metroid, ave])
            printProgressBar(index, len(metros.index), prefix = 'Progress:', suffix = 'Complete', length = 50)
    printProgressBar(len(metros.index), len(metros.index), prefix = 'Progress:', suffix = 'Complete', length = 50)
    #print(outList)
    #print("readCount2:", readCount)
    
    # write df_pivot to GEO_VARIABLES.js
    filename_GEO_VARIABLES = "VNE_" + param['filename_suffix'] + "/data/GEO_VARIABLES_"+param['filename_suffix']+".js"
    ofile = open(filename_GEO_VARIABLES, 'w')
    ofile.write('var GEO_VARIABLES =\n')
    ofile.write('[\n')
    heading = [geoid, 'INC']
    ofile.write('  '+json.dumps(heading)+',\n')
    wCount = 0
    for i, row in enumerate(outList):
        wCount += 1
        ofile.write('  '+json.dumps(row)+',\n')
    #print("GEO_VARIABLES.js write count:", wCount)
    ofile.write(']\n')
    ofile.close()


def Clustering_viz(param):
    write_LOG(param)
    
    # select community by state_fips, msa_fips, county_fips
    metros = None
    community = None
    if ('allMetros' in param and param['allMetros']):
        #metros = data_store.msa_definitions
        #metros = data_store.msas()
        metros = datasets.msas() 
    elif ('msa_fips' in param and param['msa_fips']):
        community = Community.from_ltdb(years=param['years'], msa_fips=param['msa_fips'])
        #community = Community.from_ltdb(msa_fips=param['msa_fips'])
    elif ('county_fips' in param and param['county_fips']):
        community = Community.from_ltdb(years=param['years'], county_fips=param['county_fips'])
    elif ('state_fips' in param and param['state_fips']):
        community = Community.from_ltdb(years=param['years'], state_fips=param['state_fips'])
    
    # input CSV file
    if (community is None and 'inputCSV' in param and param['inputCSV']):
        community = Community()
        community.gdf = pd.read_csv(param['inputCSV'], dtype={'geoid':str})
        geoid = community.gdf.columns[0]
        #community.gdf = community.gdf.astype(str)
        #print("inputCSV:  " + community.gdf.geoid)        
        community.gdf['geoid'] = community.gdf['geoid'].astype(str)
        #print("community.gdf.columns[0]:", community.gdf.columns[0])
        if (community.gdf.columns[0] != "geoid"):
            print("The first column of {} is not a 'geoid'.".format(param['inputCSV']))
            print("Please check your input CSV file header.")
            print(community.gdf.columns)
            return
        
        # read shape file to df_shape
        df_shape = gpd.read_file(param['shapefile'])
        df_shape = df_shape.astype(str)     
        #print("shapefile:  " + df_shape.GEOID10)        
        df_shape = df_shape.set_index("GEOID10")
        
        # insert geometry to community.gdf
        geometry = []
        for index, row in community.gdf.iterrows():
            tractid = row[geoid]
            try:
                tract = df_shape.loc[tractid]
                geometry.append(shapely.wkt.loads(tract.geometry))
            except KeyError:
                #print("Tract ID [{}] is not found in the shape file {}".format(tractid, param['shapefile']))
                geometry.append(None)
        community.gdf.insert(len(community.gdf.columns), "geometry", geometry)
    
    # param2
    #if ('inputCSV' in param and param['inputCSV'] == "Illinois_2010.csv"):
    #	community = Community()
    #	#df_San_Diego = pd.read_csv("San_Diego_1980_1990_2000_2010.csv", index_col=0)
    #	df_San_Diego = pd.read_csv("Illinois_2010.csv", index_col=0)
    #	#print(df_San_Diego)
    #	community.gdf = df_San_Diego
    #	print(community.gdf)
    
    community.gdf = community.gdf.replace([np.inf, -np.inf], np.nan)
    
    # check if geometry is not null for Spatial Clustering
    if ('geometry' in community.gdf):
        community.gdf = community.gdf[pd.notnull(community.gdf['geometry'])]
        #print(community.gdf)
    
    # filtering if geometry is not null
    #community.gdf = community.gdf[pd.notnull(community.gdf['geometry'])]
    #community.gdf = community.gdf.dropna()
    #print(community.gdf.dropna())
    #community.gdf = community.gdf[pd.notnull(community.gdf['p_household_recent_move'])]
    #community.gdf = community.gdf.replace([np.inf, -np.inf], np.nan)
    #p_household_recent_move = community.gdf[['geoid', 'p_household_recent_move']].copy()
    #print(p_household_recent_move)
    #for aTract in p_household_recent_move.itertuples():
    #	print(aTract)
    #print(community.gdf.replace([np.inf, -np.inf], np.nan))
    
    codebook = pd.read_csv('template/conversion_table_codebook.csv')
    codebook.set_index(keys='variable', inplace=True)
    labels = copy.deepcopy(param['variables'])
    label = 'short_name'                                             # default
    if ('label' in param and param['label'] == 'variable'): label = 'variable'
    if ('label' in param and param['label'] == 'full_name'): label = 'full_name'
    if ('label' in param and param['label'] == 'short_name'): label = 'short_name'
    if (label != 'variable'):
        for idx, variable in enumerate(param['variables']):
            try:
                codeRec = codebook.loc[variable]
                labels[idx] = codeRec[label]
            except:
                print("variable not found in codebook.  variable:", variable)
    param['labels'] = labels
    
    #write_INDEX_html(param)
    #write_GEO_CONFIG_js(param)
    #if (community): write_GEO_VARIABLES_js(community, param)
    #if (community): write_GEO_JSON_js(community, param)
    #if (metros is not None): write_ALL_METROS_VARIABLES_js(metros, param)
    #if (metros is not None): write_ALL_METROS_JSON_js(metros, param)
    
    if (community):
        write_INDEX_html(param)
        write_GEO_CONFIG_js(param)
        write_GEO_VARIABLES_js(community, param)
        write_GEO_JSON_js(community, param)
    
    if (metros is not None):
        write_ALL_METROS_INDEX_html(param)
        write_ALL_METROS_GEO_CONFIG_js(param)
        write_ALL_METROS_VARIABLES_js(metros, param)
        write_ALL_METROS_JSON_js(metros, param)
    
    local_dir = os.path.dirname(os.path.realpath(__file__))
    #print(local_dir)
    fname =urllib.parse.quote('index.html')
    template_dir = os.path.join(local_dir, 'VNE_' + param['filename_suffix'])
    url = 'file:' + os.path.join(template_dir, fname)
    #print(url)
    webbrowser.open(url)	
    
    print('Please run ' + '"VNE_' + param['filename_suffix']+'/index.html"'+' to your web browser.')
    print('Advanced options are available in ' + '"VNE_' + param['filename_suffix']+'/data/GEO_CONFIG.js"')


def Clustering_log():
    # build array of logs from directory of 'VNE_'
    logs = []
    dirname = os.getcwd()
    subnames = os.listdir(dirname)
    for subname in subnames:
        fullpath = os.path.join(dirname, subname)
        if (not os.path.isdir(fullpath)): continue
        if (not subname.startswith('VNE_')): continue
        #print(os.path.join(fullpath, 'index.html'))
        indexfile = os.path.join(fullpath, 'index.html')
        logfile = os.path.join(fullpath, 'data/param.log')
        if (not os.path.exists(indexfile)): continue
        if (not os.path.exists(logfile)): continue
        #print(fullpath, logfile)
        # read param.log
        ifile = open(logfile, "r")
        wholetext = ifile.read()
        contents = wholetext.split('\n', maxsplit=1)
        if (len(contents) != 2): continue
        create_at = contents[0]
        param     = contents[1]
        #print(create_at)
        #print(param)
        logs.append({'indexfile': os.path.join(subname, 'index.html'), 'create_at': create_at, 'param': param})
    logs = sorted(logs, key=lambda k: k['create_at']) 
    #print(logs)
    
    #Write output to log.html
    filename_LOG = "log.html"
    ofile = open(filename_LOG, 'w')
    ofile.write('<!DOCTYPE html>\n')
    ofile.write('<html>\n')
    ofile.write('<head>\n')
    ofile.write('  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n')
    ofile.write('  <title>Neighborhood Analysis Logging</title>\n')
    ofile.write('</head>\n')
    ofile.write('<body>\n')
    ofile.write('  <header>\n')
    ofile.write('    <h1>Neighborhood Analysis Logging</h1>\n')
    ofile.write('  </header>\n')
    
    for idx, val in enumerate(logs):
        params = val['param'].split('\n')
        html = '\n'
        html += '<div style="margin:10px; float:left; border: 1px solid #99CCFF; border-radius: 5px;">\n'
        html += '  <table>\n'
        html += '    <tr>\n'
        html += '      <td>\n'
        html += '        <button id="global_submit" type="button" style="margin:0px 20px 0px 5px;" onclick="window.open(\'' + val['indexfile'] + '\')">' + str(idx+1) + '. Show This</button>\n'
        html += '        ' + val['create_at'] + '\n'
        html += '      </td>\n'
        html += '    </tr>\n'
        html += '    <tr>\n'
        html += '      <td>\n'
        html += '<pre>\n'
        for param in params:
            html += param + '\n'
        html += '</pre>\n'
        html += '      </td>\n'
        html += '    </tr>\n'
        html += '  </table>\n'
        html += '</div>\n'
        ofile.write(html)
    
    ofile.write('</body>\n')
    ofile.write('</html>')
    ofile.close()
    
    local_dir = os.path.dirname(os.path.realpath(__file__))
    fname =urllib.parse.quote(filename_LOG)
    url = 'file:' + os.path.join(local_dir, fname)
    webbrowser.open(url)


if __name__ == '__main__':
    started_datetime = datetime.now()
    print('VulnerablePOP start at %s' % (started_datetime.strftime('%Y-%m-%d %H:%M:%S')))
    
    #sample = "downloads/LTDB_Std_All_Sample.zip"
    #full = "downloads/LTDB_Std_All_fullcount.zip"
    #store_ltdb(sample=sample, fullcount=full)
    #store_census()
       
    param = {
        'title': "Vulnerable Neighborhood to COVID-19, Chicago",
        'subject': "COVID-19",
        'filename_suffix': "Chicago_extended_kmeans_C5",
        'inputCSV': "ACS_2018_5year__zipcode_extended_Chicago_byZipcode_normalized.csv",
        'shapefile': "Chicago_extended.shp",
        'diseaseInputCSV': "COVID_IL_20200711.csv",
        'rate1': 'Confirmed (%) = _count/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1. 
        'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # denominator, per number of pop. 		
		'subjectNormalizationCSV': "Decision_Normalization_Chicago.csv",            # divisor instead of population from CSV file	
        'years': [2018],        
        'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                             # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
        'nClusters': 5,     # This option should be commented out for affinity_propagation and hdbscan
        'label': "short_name",
        'variables': [	
            "Median monthly housing costs",
            "% below poverty",				
            "% unemployed",			
            "% with 4year college degree",
            "% manufacturing",
            "% service industry",
            "% structures more than 30 years old",
            "% households moved <10 years ago",
            "% multiunit structures",
            "% owner occupied housing",
            "% vacant housing",
            "% > 60 years old",			
            "% < 18 years old",
            "% white",
            "% Asian",
            "% Hispanic",			
            "% black",			
            "% foreign born",
                    ],	
        'Distribution_INC1': True,                   #density chart: INC changes as the map extent changes 
        'Zscore_Means_across_Clusters': True,
        'Zscore_Means_of_Each_Cluster': True,
        'Number_of_Barcharts_for_Subject_Clusters': 1,
        'Number_of_BoxPlots_for_Subject_Clusters': 0,
    }

    Clustering_viz(param)

    ended_datetime = datetime.now()
    elapsed = ended_datetime - started_datetime
    total_seconds = int(elapsed.total_seconds())
    hours, remainder = divmod(total_seconds,60*60)
    minutes, seconds = divmod(remainder,60)	
    print('VulnerablePOP ended at %s    Elapsed %02d:%02d:%02d' % (ended_datetime.strftime('%Y-%m-%d %H:%M:%S'), hours, minutes, seconds))
    
