# Suppress all warnings
import warnings
warnings.filterwarnings("ignore")
import json, math, copy, sys, re
from geosnap import Community
import pandas as pd
import shapely.wkt
import shapely.geometry
from datetime import datetime, timezone
from datetime import timedelta
from dateutil import tz
from pathlib import Path
import urllib.parse
import webbrowser
import os
import pprint
from sklearn.preprocessing import minmax_scale
import numpy as np
from scipy import stats
import geopandas as gpd
import csv
from IPython.core.display import display, HTML
from pingouin import pairwise_tukey
import ipywidgets as widgets
from IPython.display import display, HTML
#This is for CyberGISX. Uncomment two command lines below when you run in CyberGIX Environment
from jupyter_server  import serverapp
warnings.filterwarnings("ignore")

#Create directory for Visualization. This is for CyberGISX. Uncomment two command lines below when you run in CyberGIX Environment    
servers = list(serverapp.list_running_servers())
servers1 = 'https://cybergisx.cigi.illinois.edu'+servers[0]["base_url"]+ 'view'
servers2 = 'https://cybergisx.cigi.illinois.edu'+servers[0]["base_url"]+ 'edit'      

cwd = os.getcwd()
prefix_cwd = "/home/jovyan/work"
cwd = cwd.replace(prefix_cwd, "")

# This is for Jupyter notebbok installed in your PC
#local_dir1 = cwd + '/'
#local_dir2 = cwd + '/'  

#This is for CyberGISX. Uncomment two command lines below when you run in CyberGIX Environment
local_dir1 = servers1 + cwd + '/'
local_dir2 = servers2 + cwd + '/' 

class ABindex:
    def __init__(self, n):
        self.n = n
        self.arr = np.array([-1] * (n*n)).reshape((n,n))
        self.m = 0
        for self.a in range(self.n-1):
            for self.b in range(self.a+1,self.n):
                #print(a, b, m)
                self.arr[self.a, self.b] = self.m;
                self.m += 1
        self.table = np.array([-1] * (self.m*2)).reshape((self.m,2))
        #print(self.arr)
        for self.a in range(self.n-1):
            for self.b in range(self.a+1,self.n):
                self.table[self.arr[self.a, self.b], 0] = self.a
                self.table[self.arr[self.a, self.b], 1] = self.b
        #print(self.table)
        
    def count(self):
        return self.m
    
    def ab2id(self, a, b):
        if (not isinstance(a, int)): a = int(a)
        if (not isinstance(b, int)): b = int(b) 
        return self.arr[a, b]
    
    def id2ab(self, n):
        return self.table[n]


# write param.log file from param into the new result folder.
def write_LOG(param):
    
    #Create a new folder where GEO_CONFIG.js GEO_JSON.js VARIABLES.js will be saved
    oDir = 'VNE_' + param['filename_suffix']
    path = Path(oDir + '/data')
    path.mkdir(parents=True, exist_ok=True)
    
    contents = pprint.pformat(param, compact=True, sort_dicts=False)        # depth=1,
    #write new outfiles: GEO_CONFIG.js GEO_JSON.js VARIABLES.js
    ofile = open(oDir+"/data/param.log", "w")
    create_at = datetime.now()
    #print(create_at)
    #print(create_at.strftime('%y-%m-%d %H:%M:%S'))  
    ofile.write('%s %s\n\n' % (create_at.strftime('%Y-%m-%d %H:%M:%S'), oDir))
    ofile.write('  '+contents.replace('\n', '\n  '))
    ofile.close()


# Reads the HTML file (Vulnerable_Neighborhood_Explorer.html) from the template folder, replaces necessary variables in the file, and save the changes in the new HTML file (index.html)
def write_INDEX_html(param):
    
    #Create a new folder where GEO_CONFIG.js GEO_JSON.js VARIABLES.js will be saved
    oDir = 'VNE_' + param['filename_suffix']
    path = Path(oDir + '/data')
    path.mkdir(parents=True, exist_ok=True)

    contents = []
    #open Vulnerable_Neighborhood_Explorer.html (the excutable file for the visualization)
    ifile = open("template/Vulnerable_Neighborhood_Explorer.html", "r", encoding="utf-8")
    contents = ifile.read()
    
    #Replace variables based on the user's selection in each of four files below.
    contents = contents.replace("Vulnerable Neighborhood Explorer", param['title'])
    contents = contents.replace("data/CONFIG.js", "data/CONFIG_"+param['filename_suffix']+".js")
    contents = contents.replace("data/GEO_JSON.js", "data/GEO_JSON_"+param['filename_suffix']+".js")
    contents = contents.replace("data/VARIABLES.js", "data/VARIABLES_"+param['filename_suffix']+".js")
    
    #write new outfiles: GEO_CONFIG.js GEO_JSON.js VARIABLES.js
    ofile = open(oDir+"/index.html", "w", encoding="utf-8")
    ofile.write(contents)
    ofile.close()


# write GEO_CONFIG_xxx.js from template
def write_GEO_CONFIG_js(param):
    
    # read ACM_GEO_CONFIG.js
    ifile = open("template/CONFIG.js", "r")
    contents = ifile.read()
    
    SubjectName = "";
    QualitativeMap_Field = "";
    Maps_of_Subject = True;
    Maps_of_neighborhood = True;               
    Distribution_of_Subject = True;                  
    Distribution_of_Subject_different_period = True; 
    Distribution_of_Subject_different_cluster = True;
    Temporal_change_in_neighborhoods = True;
    Parallel_Categories_Diagram_in_neighborhoods = True;
    Chord_Diagram_in_neighborhoods = True;
    Zscore_Means_across_Clusters = True;
    Zscore_Means_of_Each_Cluster = True;
    Number_of_Column_Charts_for_Subject_Clusters = 0;
    Number_of_BoxPlots_for_Subject_Clusters = 0;
    
    if ('subject' in param): SubjectName =  param['subject']
    if ('years' in param): QualitativeMap_Field =  param['years']
    if ('Maps_of_Subject' in param): Maps_of_Subject =  param['Maps_of_Subject']
    if ('Maps_of_neighborhood' in param): Maps_of_neighborhood =  param['Maps_of_neighborhood']
    if ('Distribution_of_Subject' in param): Distribution_of_Subject =  param['Distribution_of_Subject']
    if ('Distribution_of_Subject_different_period' in param): Distribution_of_Subject_different_period =  param['Distribution_of_Subject_different_period']
    if ('Distribution_of_Subject_different_cluster' in param): Distribution_of_Subject_different_cluster =  param['Distribution_of_Subject_different_cluster']
    if ('Temporal_change_in_neighborhoods' in param): Temporal_change_in_neighborhoods =  param['Temporal_change_in_neighborhoods']
    if ('Parallel_Categories_Diagram_in_neighborhoods' in param): Parallel_Categories_Diagram_in_neighborhoods =  param['Parallel_Categories_Diagram_in_neighborhoods']
    if ('Chord_Diagram_in_neighborhoods' in param): Chord_Diagram_in_neighborhoods =  param['Chord_Diagram_in_neighborhoods']
    if ('Zscore_Means_across_Clusters' in param): Zscore_Means_across_Clusters =  param['Zscore_Means_across_Clusters']
    if ('Zscore_Means_of_Each_Cluster' in param): Zscore_Means_of_Each_Cluster =  param['Zscore_Means_of_Each_Cluster']
    if ('Number_of_Column_Charts_for_Subject_Clusters' in param): Number_of_Column_Charts_for_Subject_Clusters =  param['Number_of_Column_Charts_for_Subject_Clusters']
    if ('Number_of_BoxPlots_for_Subject_Clusters' in param): Number_of_BoxPlots_for_Subject_Clusters =  param['Number_of_BoxPlots_for_Subject_Clusters']
    
    # perpare parameters
    #NumOfMaps = len(param['years']) + 1
    #NumOfMaps = len(param['years']) + 1 if Maps_of_Subject else len(param['years'])
    #InitialLayers = ["INC"]
    InitialLayers = ["INC"] if Maps_of_Subject else []
    if (len(param['years']) <= 1): InitialLayers = []
    if (len(InitialLayers) == 0):
        if ('disasterInputCSV' in param):
            df_disease = pd.read_csv(param['disasterInputCSV'], dtype={'geoid':str})
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
    if (NumOfMaps ==1):
        Map_width = "800px"
        Map_height = "800px"
    # replace newly computed "NumOfMaps", "InitialLayers", "Map_width", "Map_height" in CONFIG.js. See the example replacement below
    '''
        'years': [1980, 1990, 2000, 2010]            ->    'var InitialLayers = ["INC", "1980", "1990", "2000", "2010"];'
    '''
    NumOfMaps = "var NumOfMaps = " + str(NumOfMaps) + ";"
    SubjectName = 'var SubjectName = "' + SubjectName + '";'
    QualitativeMap_Field = 'var QualitativeMap_Field = ' + str(QualitativeMap_Field) + ';'
    InitialLayers = "var InitialLayers = " + json.dumps(InitialLayers) + ";"
    Maps_of_Subject = "var Maps_of_Subject = " + json.dumps(Maps_of_Subject)+ ";"
    Maps_of_neighborhood = "var Maps_of_neighborhood = " + json.dumps(Maps_of_neighborhood)+ ";"
    Distribution_of_Subject = "var Distribution_of_Subject = " + json.dumps(Distribution_of_Subject)+ ";"
    Distribution_of_Subject_different_period = "var Distribution_of_Subject_different_period = " + json.dumps(Distribution_of_Subject_different_period)+ ";"
    Distribution_of_Subject_different_cluster = "var Distribution_of_Subject_different_cluster = " + json.dumps(Distribution_of_Subject_different_cluster)+ ";"
    Temporal_change_in_neighborhoods = "var Temporal_change_in_neighborhoods = " + json.dumps(Temporal_change_in_neighborhoods)+ ";"
    Parallel_Categories_Diagram_in_neighborhoods = "var Parallel_Categories_Diagram_in_neighborhoods = " + json.dumps(Parallel_Categories_Diagram_in_neighborhoods)+ ";"
    Chord_Diagram_in_neighborhoods = "var Chord_Diagram_in_neighborhoods = " + json.dumps(Chord_Diagram_in_neighborhoods)+ ";"
    Zscore_Means_across_Clusters = "var Zscore_Means_across_Clusters = " + json.dumps(Zscore_Means_across_Clusters)+ ";"
    Zscore_Means_of_Each_Cluster = "var Zscore_Means_of_Each_Cluster = " + json.dumps(Zscore_Means_of_Each_Cluster)+ ";"
    Number_of_Column_Charts_for_Subject_Clusters = "var Barchart_of_Subject_Clusters = " + str(Number_of_Column_Charts_for_Subject_Clusters) + ";"
    Number_of_BoxPlots_for_Subject_Clusters = "var BoxPlot_of_Subject_Clusters = " + str(Number_of_BoxPlots_for_Subject_Clusters) + ";"
    Map_width = 'var Map_width  = "' + Map_width + '";'
    Map_height = 'var Map_height = "' + Map_height + '";'
    
    
    contents = contents.replace('var SubjectName = "";', SubjectName)
    contents = contents.replace('var QualitativeMap_Field = "";', QualitativeMap_Field)    
    contents = contents.replace("var InitialLayers = [];", InitialLayers)
    contents = contents.replace("var Maps_of_Subject = true;", Maps_of_Subject)
    contents = contents.replace("var Maps_of_neighborhood = true;", Maps_of_neighborhood)
    contents = contents.replace("var Distribution_of_Subject = false;", Distribution_of_Subject)
    contents = contents.replace("var Distribution_of_Subject_different_period = true;", Distribution_of_Subject_different_period)
    contents = contents.replace("var Distribution_of_Subject_different_cluster = true;", Distribution_of_Subject_different_cluster)
    contents = contents.replace("var Temporal_change_in_neighborhoods = true;", Temporal_change_in_neighborhoods)
    contents = contents.replace("var Parallel_Categories_Diagram_in_neighborhoods = true;", Parallel_Categories_Diagram_in_neighborhoods)
    contents = contents.replace("var Chord_Diagram_in_neighborhoods = true;", Chord_Diagram_in_neighborhoods)
    contents = contents.replace("var Zscore_Means_across_Clusters = true;", Zscore_Means_across_Clusters)
    contents = contents.replace("var Zscore_Means_of_Each_Cluster = true;", Zscore_Means_of_Each_Cluster)
    contents = contents.replace("var Barchart_of_Subject_Clusters = 0;", Number_of_Column_Charts_for_Subject_Clusters)
    contents = contents.replace("var BoxPlot_of_Subject_Clusters = 0;", Number_of_BoxPlots_for_Subject_Clusters)
    contents = contents.replace('var Map_width  = "400px";', Map_width)
    contents = contents.replace('var Map_height = "400px";', Map_height)
    
    # Create a new folder where GEO_CONFIG.js GEO_JSON.js VARIABLES.js will be saved
    oDir = 'VNE_' + param['filename_suffix']
 
    #Write output including the replacement above
    filename_GEO_CONFIG = oDir + "/data/CONFIG_"+param['filename_suffix']+".js"
    ofile = open(filename_GEO_CONFIG, 'w')
    ofile.write(contents)
    ofile.close()


# write GEO_JSON_xxx.js from shapefile
def write_GEO_JSON_js(community, param):
    
    # Create a new folder where GEO_CONFIG.js GEO_JSON.js VARIABLES.js will be saved
    oDir = 'VNE_' + param['filename_suffix']

    # open GEO_JSON.js write heading for geojson format
    filename_GEO_JSON = oDir + "/data/GEO_JSON_"+param['filename_suffix']+".js"    
    ofile = open(filename_GEO_JSON, 'w')
    ofile.write('var GEO_JSON =\n')
    ofile.write('{"type":"FeatureCollection", "features": [\n')
    
    
    geoid = community.gdf.columns[0]
    #if (geoid != ""): geoid = "geoid"
    
    # read shape file to df_shape
    df_shape = gpd.read_file(param['shapefile'])
    df_shape = df_shape.astype(str)     
    #print("shapefile:  " + df_shape.GEOID10)        
    df_shape = df_shape.set_index("GEOID10")
    #print(df_shape)
    
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
        
        feature["geometry"] = shapely.geometry.mapping(geometry)
        feature["properties"] = {geoid: tractid}
        wCount += 1
        ofile.write(json.dumps(feature)+',\n')
    #print("GEO_JSON.js write count:", wCount)
        
    # complete the geojosn format by adding parenthesis at the end.	
    ofile.write(']}\n')
    ofile.close()


# write GEO_VARIABLES_xxx.js
def write_GEO_VARIABLES_js(community, param):
    
    #print(param)
    geoid       = community.gdf.columns[0]
    method      = param['method']
    nClusters   = param['nClusters']
    years       = param['years']
    variables   = param['variables']
    labels      = param['labels']
    
    # parse the formula of rate1 in param to get surfix, dividend_surfix and divisor_surfix
    rate1_surfix = ""
    rate1_dividend_surfix = ""
    rate1_divisor_surfix = ""  
    if ('rate1' in param):
        rate1_surfix = "_" + param['rate1'].split('=')[0].strip()
        rate1_dividend_surfix = param['rate1'].split('=')[1].split('/')[0].strip()
        rate1_divisor_surfix = param['rate1'].split('=')[1].split('/')[1].strip()
        
    # parse the formula of rate2 in param to get surfix, dividend_surfix and divisor_surfix
    rate2_surfix = ""
    rate2_dividend_surfix = ""
    rate2_divisor_surfix = ""  
    if ('rate2' in param):
        rate2_surfix = "_" + param['rate2'].split('=')[0].strip()
        rate2_dividend_surfix = param['rate2'].split('=')[1].split('/')[0].strip()
        rate2_divisor_surfix = param['rate2'].split('=')[1].split('/')[1].strip()
    
    # parse the subjectNormalization in param to get surfix, variables, multiplier and ivisor
    sb_surfix = ""                               # sb: subject Normalization
    sb_variables = ""
    sb_multiplier = 0.0
    sb_divisor = {}                              # key: denominator,  value: divisor
    df_divisor = None
    df_normalization = None
    #if ('subjectNormalization' in param and 'subjectNormalizationCSV' in param):
    if ('normalizationCSV' in param):
        
        # You don't have to put 'subjectNormalization' in the parm anymore.
        # Set default value to 'subjectNormalization' in the param
        # param['subjectNormalization'] = '(/10k pop) = all * 10000.0 / Population'  # denominator, per number of pop.
        
        # read subject normalization csv file
        #df_normalization = pd.read_csv(param['subjectNormalizationCSV'])
        df_normalization = pd.read_csv(param['normalizationCSV'])
        #print(df_normalization)
        
        denominator = df_normalization.columns[0]
        divisor = df_normalization.columns[1]
        
        #sb0 = param['subjectNormalization'].split('=')[0].strip()
        #sb1 = param['subjectNormalization'].split('=')[1].strip()
        #sb10 = sb1.split('*')[0].strip()
        #sb11 = sb1.split('*')[1].strip()
        #sb110 = sb11.split('/')[0].strip()
        #sb111 = sb11.split('/')[1].strip()
        #sb_surfix = " " + sb0
        #sb_variables = sb10
        #sb_multiplier = float(sb110)              # default: 10000.0
        #sb_divisor = sb111
        
        sb_variables = "all"
        sb_multiplier = 10000.0                  # default: 10000.0
        if ('normalizationUnit' in param): sb_multiplier = float(param['normalizationUnit'])
        sb_surfix = " (/" + "{:,}".format(int(sb_multiplier)) + " pop)"
        if (sb_multiplier == 1000): sb_surfix = " (/1K pop)"
        if (sb_multiplier == 10000): sb_surfix = " (/10K pop)"
        if (sb_multiplier == 100000): sb_surfix = " (/100K pop)"
        if (sb_multiplier == 1000000): sb_surfix = " (/1M pop)"
        
        sb_divisor = pd.Series(df_normalization[divisor].values,index=df_normalization[denominator]).to_dict()
        #print("{} = {} * {} / {}".format(sb_surfix, "all", sb_multiplier, "Population"))
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
        #print("df_divisor:", df_divisor)
    
    seqClusters = 5
    distType    = 'tran'
    
    if ('Sequence' in param and type(param['Sequence']) is dict):
        if ('seq_clusters' in param['Sequence']): seqClusters = param['Sequence']['seq_clusters']
        if ('dist_type' in param['Sequence']): distType = param['Sequence']['dist_type']
    
    # filtering by years
    community.gdf = community.gdf[community.gdf.year.isin(years)]
    #print(community.gdf)
    
    # clustering by method, nClusters with filtering by variables
    if (method == 'kmeans' or method == 'ward' or method == 'affinity_propagation' or method == 'spectral' or method == 'gaussian_mixture' or method == 'hdbscan'):
        clusters = community.cluster(columns=variables, method=method, n_clusters=nClusters)
    if (method == 'ward_spatial' or method == 'spenc' or method == 'skater' or method == 'azp' or method == 'max_p'):
        clusters = community.regionalize(columns=variables, method=method, n_clusters=nClusters) #spatial_cluster
    #print(clusters.gdf.columns)
    #print(clusters.gdf)
    #print(clusters.gdf[['year', 'geoid', 'kmeans']])
    nClusters = -1
    clusterDic = {}
    for i, row in clusters.gdf.iterrows():
        c = row[method]
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
    df_pivot = df_wide
    lastColumn = df_pivot.columns[df_pivot.shape[1]-1]					# get the last column name as like 'tran-5'
    df_pivot.rename(columns={lastColumn: 'Sequence'}, inplace=True)		# change the last column name to 'Sequence'
    #print(df_pivot)
    
    if (len(years) > 1):
        # convert df_pivot to list for INCS.linc
        yearList = []
        for year in years:
            aYearList = df_pivot[year].values.tolist()
            aYearList = list(map(float, aYearList)) 
            yearList.append(aYearList)
        #print(yearList)
        # calculate INC
        incs = linc(yearList)
        #print(incs)	
        # insert INC to first column of df_pivot
        df_pivot.insert(loc=0, column='INC', value=incs)
    
    if ('Sequence' not in param or not param['Sequence']): 
        df_pivot.drop(columns=['Sequence'], inplace=True)
    #print(df_pivot)
    
    # calculate zscore
    clusters_flattened = pd.DataFrame(df_pivot.to_records())                   # convert pivot to data frame
    geoids = clusters_flattened["geoid"].tolist()                              # get list of geoids from pivot
    valid_gdf = community.gdf[community.gdf.geoid.isin(geoids)]                # get all rows of valid geoids from community.gdf
    #print("clusters_flattened:", clusters_flattened)
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
    clusterChange = None
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
        #print("clusterChange:", clusterChange)    
    df_disease = None
    
    if ('disasterInputCSV' in param):
        df_disease = pd.read_csv(param['disasterInputCSV'], dtype={'geoid':str})
        df_disease['geoid'] = df_disease['geoid']
        #print("df_disease:   " + df_disease.geoid)        
        df_disease = df_disease.set_index(geoid)
    
    
    # write df_pivot to GEO_VARIABLES.js
    filename_GEO_VARIABLES = "VNE_" + param['filename_suffix'] + "/data/VARIABLES_"+param['filename_suffix']+".js"
    geoVariablesList = []
    ofile = open(filename_GEO_VARIABLES, 'w')
    ofile.write('var GEO_VARIABLES =\n')
    ofile.write('[\n')
    # generation heading and write it.
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
        #print(dividends1, dividends2)
        
    geoVariablesList.append(heading)
    ofile.write('  '+json.dumps(heading)+',\n')
    #print("df_disease:", df_disease.columns)
    wCount = 0
    for i, row in df_pivot.reset_index().iterrows():
        aLine = row.tolist()
        #print("aLine:", aLine)
        if (df_disease is not None):
            try:
                aDisease = df_disease.loc[aLine[0]].tolist()
            except KeyError:
                #aDisease = [-9999] * df_disease.shape[1]
                aDisease = [0] * df_disease.shape[1]                 # 2020-07-05 page3
            for j, v in enumerate(aDisease):
                column = df_disease.columns[j]
                aLine.append(v)
                if (sb_surfix != "" and column in sb_divisor):
                    populations = df_divisor.loc[aLine[0]][sb_divisor[column]]
                    r = 0.0 if (populations == 0 or populations == -9999) else v * sb_multiplier / populations
                    aLine.append(round(r,2))
                if (dividends1[j] >= 0):
                    d = dividends1[j]
                    r = 0.0 if (v == 0) else aDisease[d] * 100.0 / v
                    #if (r > 100): print("{}  {:<25}  {}%".format(aLine[0], df_disease.columns[d], round(r,2)))
                    aLine.append(round(r,2))
                if (dividends2[j] >= 0):
                    d = dividends2[j]
                    r = 0.0 if (v == 0) else aDisease[d] * 100.0 / v
                    #if (r > 100): print("{}  {:<25}  {}%".format(aLine[0], df_disease.columns[d], round(r,2)))
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
                  
    years = [str(year) for year in df_pivot.columns.tolist()]        # years must be column names as like ["2018", ..]
    #print("years:", type(years), years)
    df_geoVariables = pd.DataFrame(geoVariablesList[1:], columns=geoVariablesList[0])
    #print(df_geoVariables)
    
    # convert values of df_geoVariables[years] using clusterChange dictionary
    '''
    if (zScore_wAHb is not None):
        for year in years:
            changedClusters = []
            for l, row in df_geoVariables.iterrows():
                changedClusters.append(clusterChange[row[year]])
            df_geoVariables[year] = changedClusters
        #print(df_geoVariables)
    '''
    filename_GEO_VARIABLES_CSV = "VNE_" + param['filename_suffix'] + "/data/CSV_VARIABLES_"+param['filename_suffix']+".csv"
    #df_geoVariables.to_csv(filename_GEO_VARIABLES_CSV, index=False)
    #print(df_geoVariables)
    
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
    if (zScore_wAHb is not None):
        changedClusters = []
        for l, row in df_geoZscores.iterrows():
            changedClusters.append("C"+str(clusterChange[int(row['Cluster'][1:])]))
        df_geoZscores['Cluster'] = changedClusters
        #print(df_geoZscores)
        df_geoZscores = df_geoZscores.sort_values(df_geoZscores.columns[0])
    #print(df_geoZscores)
    
    filename_GEO_ZSCORES_CSV = "VNE_" + param['filename_suffix'] + "/data/CSV_ZSCORES_"+param['filename_suffix']+".csv"
    #df_geoZscores.to_csv(filename_GEO_ZSCORES_CSV, index=False)
    
    if (df_disease is not None):
        df_disease = df_disease.reset_index()
        countbycluster = {}
        #print("df_pivot:", df_pivot)
        #print("df_pivot.columns:", df_pivot.columns)
        for year in df_pivot.columns:
            #print("year:", year, type(year))
            if (isinstance(year, str)): continue
            
            populationsbycluster = {}            # key: colums,  value: [0] * nClusters
            if (sb_surfix != ""): 
                df_divisor = community.gdf[community.gdf['year'] == year]
                df_divisor = df_divisor[sb_columns]
                df_divisor = df_divisor.set_index('geoid')
                #print(df_divisor)
                
                for i, row in df_disease.iterrows():
                    if (row['geoid'] in df_pivot.index):
                        c = df_pivot.loc[row['geoid']][year]
                        #print(c, df_pivot.loc[row['geoid']])
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
                if (row['geoid'] in df_pivot.index):
                    c = df_pivot.loc[row['geoid']][year]
                    for k in range(1, row.size):
                        countbycluster[year][c][k] += row.iloc[k]
            #print(countbycluster[year])
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
            if (zScore_wAHb is not None):
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
            #df_geoCluster.to_csv(filename_GEO_ZSCORES_CSV, index=False)
            #print(df_geoCluster)
        ofile.write('}\n')
        
        # from pingouin import pairwise_tukey
        # perform multiple pairwise comparison (Tukey HSD)
        # for unbalanced (unequal sample size) data, pairwise_tukey uses Tukey-Kramer test
        #m_comp = pairwise_tukey(data=Tukey_HSD_Test_Input, dv=selected, between='2018')
        #m_comp = pairwise_tukey(data=Tukey_HSD_Test_Input, dv=selected, between='2018').round(6)
        #print(m_comp)
        #print(df_pivot)
        #print(df_disease)
        #print(df_geoVariables)
        n = len(set(df_geoVariables[years[0]].to_list()))
        ab = ABindex(n)
        #print("m =", ab.count())
        #print(len(set(df_geoVariables[years[0]].to_list())))
        
        ofile.write('\n')
        ofile.write('var GEO_TUKEY =\n')
        ofile.write('{\n')
        ofile.write('    "data format": [\n')
        for k in range(ab.count()):
            a = ab.id2ab(k)[0]
            b = ab.id2ab(k)[1]
            ofile.write('        ["{}", "{}", "p-tukey", "P"],\n'.format("A"+str(a), "B"+str(b)))
        ofile.write('    ],\n')
        
        for j, column in enumerate(df_geoVariables.columns):
            if (column == geoid): continue
            if (column == years[0]): continue
            #if (j > 3): continue
            #print(j, column)
            ofile.write('    "{}": [\n'.format(column.strip()))
            m_comp = pairwise_tukey(data=df_geoVariables, dv=column, between=years[0])
            #print(type(m_comp))
            #print(m_comp)
            for k, row in m_comp.iterrows():
                aLine = row.tolist()
                #print(k, type(row), row)
                #print(type(row.A))               # <class 'numpy.float64'>
                a = int(row.A)
                b = int(row.B)
                if (k != ab.ab2id(a, b)):
                    print(k, ab.ab2id(a, b), a, b, "{:0.6f}".format(row['p-tukey']))
                sign = "   "
                if (row['p-tukey'] < 0.05): sign = "*  "
                if (row['p-tukey'] < 0.01): sign = "** "
                if (row['p-tukey'] < 0.001): sign = "***"
                ofile.write('        [{}, {}, {:0.6f}, "{}"],\n'.format(a, b, row['p-tukey'], sign))
            ofile.write('    ],\n')
        
        ofile.write('}\n')
        
        
        
        
        
        
        if (zScore_wAHb is not None):
            aLine = "var CHANGE_CLUSTER = "
            #aLine += json.dumps(clusterChange).replace('"','') + ";"
            aLine += json.dumps(clusterChange)
            #print(aLine)
            ofile.write('\n'+aLine+'\n')
        
    ofile.close()
    #sys.exit(4)

def Vulnerability_log(param):
    #Create a new folder where GEO_CONFIG.js GEO_JSON.js VARIABLES.js will be saved
    oDir = 'VNE_' + param['filename_suffix']
    path = Path(oDir + '/data')
    path.mkdir(parents=True, exist_ok=True)
    
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
        cols = contents[0].split(' ', maxsplit=3)
        #create_at = contents[0] if (len(cols) <= 2) else cols[0] + ' ' + cols[1] + ' &nbsp; ' + cols[2]        
        create_at = contents[0]
        out_dir = ""
        if (len(cols) >= 3): 
            create_at = cols[0] + ' ' + cols[1]
            out_dir = cols[2]
            
        #create_at = datetime.fromisoformat(create_at).replace(tzinfo=timezone.utc).astimezone(tz=tz.tzlocal())
        #print(create_at)        
        create_at = datetime.fromisoformat(create_at).replace(tzinfo=timezone.utc)
        #print(create_at)
        param = contents[1]
        #print(subname+'/'+'index.html')
        #print(create_at)
        #print(param)
        #logs.append({'indexfile': os.path.join(subname, 'index.html'), 'create_at': create_at, 'param': param})
        #logs.append({'indexfile': subname+'/'+'index.html', 'create_at': create_at, 'param': param})
        #logs.append({'indexfile': local_dir1+subname+'/'+'index.html', 'create_at': create_at.isoformat(), 'out_dir': out_dir, 'param': param})
        logs.insert(0, {'indexfile': local_dir1+subname+'/'+'index.html', 'create_at': create_at.isoformat(), 'out_dir': out_dir, 'param': param})
    logs = sorted(logs, key=lambda k: k['create_at'], reverse=True) 
    #print(logs)
    
    #Write output to log.html
    filename_LOG = "log.html"
    ofile = open(filename_LOG, 'w')
    ofile.write('<!DOCTYPE html>\n')
    ofile.write('<html>\n')
    ofile.write('<head>\n')
    ofile.write('  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n')
    ofile.write('  <title>Vulnerablity Explorer Logging</title>\n')
    ofile.write('</head>\n')
    ofile.write('<body>\n')
    ofile.write('  <header>\n')
    ofile.write('    <h1>Logging</h1><p style="color:#6495ED;"><i>*Use the button to copy the URL and paste it into your browser to view the visualizations you created. If the button does not work, you can manually copy the URL from the text box.</i></p>\n')
    ofile.write('  </header>\n')
    
    for idx, val in enumerate(logs):
        params = val['param'].split('\n')
        html = '\n'
        html += '<div style="height:500px; margin:10px; float:left; border: 1px solid #99CCFF; border-radius: 5px;overflow-y: auto;">\n'
        html += '  <table>\n'
        html += '    <tr>\n'
        html += '      <td>\n'
        html += '      <span style="color:#CD5C5C;"><strong>' + str(idx+1) + '. ' + val['out_dir'] + '</strong></span>'
        html += '        <span style="display: inline-block; width:400px; text-align:left; margin-left: 100px;">' + '<span class="utcToLocal">'+ val['create_at'] + '</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        html += '        <input type="text" value=' + val['indexfile']+ ' id="myInput' + str(idx+1) + '">'
        html += '        <button onclick="myFunction' + str(idx+1) + '()">Copy</button></span>\n'  
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

        html += '<script>'
        html += 'function myFunction' + str(idx+1) + '() {'
        html += '  var copyText = document.getElementById("myInput' + str(idx+1) + '");' #Get the text field
        html += '  copyText.select();'                                 #Select the text field
        html += '  copyText.setSelectionRange(0, 99999);'              #For mobile devices
        html += '  navigator.clipboard.writeText(copyText.value);'     #Copy the text inside the text field
        html += '  alert("The URL has been copied to the clipboard. Paste it to the browser to see your visualizations: " + copyText.value);'       #Alert the copied text
        html += '};'
        html += 'document.querySelectorAll(".utcToLocal").forEach('
        html += '  function (i) {'
        html += '    const options = {hour12: false, hour:"2-digit", minute:"2-digit", timeZoneName: "short", year: "numeric", month: "numeric", day: "numeric"};'
        html += '    i.innerHTML = new Date(i.innerText).toLocaleString("en-US",options);'
        html += '  }'
        html += ');'
        html += '</script>\n'        
        ofile.write(html)
    
    ofile.write('</body>\n')
    ofile.write('</html>')
    ofile.close()
    
    local_dir = os.path.dirname(os.path.realpath(__file__))
    #local_dir = os.getcwd()
    fname =urllib.parse.quote(filename_LOG)
    url = 'file:' + os.path.join(local_dir, fname)
    #url = os.path.join(template_dir, fname)    
    webbrowser.open(url)

def Vulnerability_viz(param):
    # check years parameters
    if (len(param['years']) != 1):
        print("param['years'] must be one element")
        print("param['years'] =", param['years'])
        print("\n", param, "\n")
        print("program terminated abnormally.")
        sys.exit(10)
    
    write_LOG(param)
    community = None
    
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
    
    community.gdf = community.gdf.replace([np.inf, -np.inf], np.nan)
    
    # check if geometry is not null for Spatial Clustering
    if ('geometry' in community.gdf):
        community.gdf = community.gdf[pd.notnull(community.gdf['geometry'])]
        #print(community.gdf)
    
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
    
    if (community):
        write_INDEX_html(param)
        write_GEO_CONFIG_js(param)
        write_GEO_VARIABLES_js(community, param)
        write_GEO_JSON_js(community, param)
        
    
    #local_dir = os.path.dirname(os.path.realpath(__file__))
    #local_dir = os.getcwd()
    #print(local_dir)
    fname =urllib.parse.quote('index.html')
    template_dir = os.path.join(local_dir1, 'VNE_' + param['filename_suffix'])
    #url = 'file:' + os.path.join(template_dir, fname)
    url = os.path.join(template_dir, fname)
    Vulnerability_log(param)
    webbrowser.open(url)
    print('To see your visualization, click the URL below (or locate the files):')
    print(url)
    print('To access all visualizations that you have created, click the URL below (or locate the files):')
    print(local_dir1 + 'log.html')    
    print('Advanced options are available in ')  
    print(local_dir2 + 'VNE_' + param['filename_suffix']+'/data/CONFIG_' + param['filename_suffix']+'.js')


def VNE(attribute):

    # Exclude the first two columns for variable selection
    data = attribute
    available_variables = data.columns[2:].tolist()
    
    # Text input for title
    title_input = widgets.Text(
        value="Vulnerable Neighborhood to COVID-19, Chicago",
        description='Title:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Text input for subject
    subject_input = widgets.Text(
        value="COVID-19",
        description='Subject:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Text input for filename suffix
    filename_suffix_input = widgets.Text(
        value="Chicago_kmeans_C5",
        description='Filename Suffix:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Text input for input CSV path
    input_csv_input = widgets.Text(
        value="input_Chicago/ACS_2018_5year__zipcode_Cook_byZipcode_normalized.csv",
        description='Input CSV:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Function to update variables dynamically based on Input CSV
    def update_variables(change):
        global available_variables
        try:
            df = pd.read_csv(change['new'])
            available_variables = df.columns[2:].tolist()
            variables_listbox.options = available_variables
        except Exception as e:
            with output:
                output.clear_output()
                print(f"Error updating variables: {e}")
                
    # Observe changes in Input CSV
    input_csv_input.observe(update_variables, names='value')
    
    
    # Text input for shapefile path
    shapefile_input = widgets.Text(
        value="input_Chicago/zipcode_Cook_County.shp",
        description='Shapefile:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Text input for disaster input CSV path
    disaster_csv_input = widgets.Text(
        value="input_Chicago/COVID_IL_20200711.csv",
        description='Disaster CSV:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Text input for rate1
    rate1_input = widgets.Text(
        value="Confirmed (%) = _count/_tested",
        description='Rate Formula:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Text input for normalization CSV
    normalization_csv_input = widgets.Text(
        value="input_Chicago/Normalization_Table_Chicago.csv",
        description='Normalization CSV:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Text input for normalization unit
    normalization_unit_input = widgets.Text(
        value="10000",
        description='Normalization Unit:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Text input for years
    years_input = widgets.Text(
        value="2018",
        description='Years:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Dropdown for method selection
    method_dropdown = widgets.Dropdown(
        options=['kmeans', 'affinity_propagation', 'gaussian_mixture', 'spectral', 'ward'],
        value='kmeans',
        description='Method:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Dropdown for number of clusters
    nClusters_dropdown = widgets.Dropdown(
        options=list(range(31)),  # 0 to 30
        value=5,
        description='Number of Clusters:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )
    
    # Listbox for variables with shift key support
    variables_listbox = widgets.SelectMultiple(
        options=available_variables,
        value=[available_variables[0]],  # Default selection
        description='Variables:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px', height='340px')
    )
    
    # Label for checkboxes
    checkbox_label = widgets.Label(
        value="Select plots to visualize:"
    )
    
    # Checkboxes for boolean parameters
    Distribution_of_Subject_checkbox = widgets.Checkbox(
        value=True,
        description='Distribution of Subject',
        layout=widgets.Layout(width='400px'),
        style={'description_width': '160px'},
    )
    Zscore_Means_across_Clusters_checkbox = widgets.Checkbox(
        value=True,
        description='Zscore Means across Clusters',
        layout=widgets.Layout(width='400px'),
        style={'description_width': '160px'},
    )
    Zscore_Means_of_Each_Cluster_checkbox = widgets.Checkbox(
        value=True,
        description='Zscore Means of Each Cluster',
        layout=widgets.Layout(width='400px'),
        style={'description_width': '160px'},
    )
    
    # Dropdown for number of bar charts
    barcharts_dropdown = widgets.Dropdown(
        options=list(range(31)),  # 0 to 30
        value=3,
        description='Column Charts:',
        layout=widgets.Layout(width='400px'),
        style={'description_width': '160px'},
    )
    
    # Dropdown for number of box plots
    boxplots_dropdown = widgets.Dropdown(
        options=list(range(31)),  # 0 to 30
        value=0,
        description='Box Plots:',
        layout=widgets.Layout(width='400px'),
        style={'description_width': '160px'},
    )
    
    # Button to run the program
    run_button = widgets.Button(
        description="Submit",
        button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
        tooltip="Click to run the visualization",
        icon='play',  # (FontAwesome names without the `fa-` prefix)
        layout=widgets.Layout(width='300px', height='50px')
    )
    
    # Output widget to capture the result
    output = widgets.Output()
    
    def on_button_click(b):
        with output:
            output.clear_output()
            params = get_inputs()
            Vulnerability_viz(params)
    
    run_button.on_click(on_button_click)
    
    # Add an empty line
    empty_line = widgets.HTML(value="<br>")
    
    # Help content
    help_content = widgets.HTML(
        value="""
        <h4>Help Section</h4>
        <p>Use this interface to configure the parameters for Vulnerability Visualization:</p>
        <ul>
            <li><b>Title:</b> Enter a descriptive title for the visualization. Texts will be placed at the top of the result visualization.</li>
            <li><b>Subject:</b> Specify the subject matter (e.g., COVID-19). Texts will be placed at the top of the maps, column bar charts, and box plots.</li> 
            <li><b>Filename Suffix:</b> Enter the name of the output folder where your result visualization is saved. It shouldn't contain spaces.</li>
            <li><b>Input CSV:</b> Provide the path to your input CSV file. The file should include socioeconomic, demographic, and health status data. Ensure that the first column is labeled geoid and the second column is labeled year. All subsequent columns will be available for selection in the Variables input box below.</li>
            <li><b>Shapefile:</b> Enter the path to the shapefile. A shapefile is used to visualize polygons on the map. The first column header must start with ‘geoid,’ and the code should match the 'geoid' column of another input CSV file that you enter for 'inputCSV' and 'disasterInputCSV’.</li>
            <li><b>disasterInputCSV:</b> Enter the path to your input CSV file containing data representing the number of disaster-affected people. In the case of COVID-19, the file can contain the number of confirmed cases, COVID-19 testing cases, and deaths. Ensure that the first column is labeled geoid. </li>
            
            <li><b>Years:</b> List the years for the analysis. This value should match the second column of the input CSV. It will be displayed at the top of the neighborhood map.</li>
            <li><b>normalizationCSV:</b> Enter the path to your input CSV file. The first column of the CSV should contain column headers in ‘disasterInputCSV’, and the second column should contain column headers in ‘inputCSV’. For example, if you enter ‘total_count’ in the first column and ‘Population’ in the second column of the same row, it will compute ‘total_count’/’Population’ multiplied by the value entered in the next parameter, ‘normalizationUnit’.</li>
            <li><b>Normalization Unit:</b> Set the normalization value (e.g., 10000). If you enter the value 10000 here, your cases will be represented per 10000.</li>
            <li><b>Rate Formula:</b> This feature is primarily designed for analyzing disease-related data. It calculates percentages by utilizing two variables from the 'disasterInputCSV' file. For instance, if the 'disasterInputCSV' contains columns such as 'total_count' (representing the number of confirmed cases of a disease) and 'total_test' (representing the number of individuals tested for the disease), you can specify a formula like 'Confirmed (%) = _count / _test'. This formula will compute the percentage of confirmed cases (e.g., the number of confirmed cases divided by the number of tests conducted, multiplied by 100) and display the result as a new column named 'total_Confirmed (%)' in the visualization. To ensure this computation functions correctly, the column names in the input CSV file assigned to 'disasterInputCSV' must include underscore (_). When you define it like above case, the program identifies variables ending with '_count' and divides them by variables ending with '_test' for the calculation.</li>
            
            <li><b>Method:</b> Choose a clustering method from the dropdown.</li>
            <li><b>Number of Clusters:</b> Enter the number of clusters/neighborhoods you want to create.</li>
            <li><b>Variables:</b> Select multiple variables by holding down the Ctrl key. They are inputs for your selected clustering method above.</li>
            <li><b>Distribution of Subject:</b> Distribution chart. A in the figure above. Check to visualize.</li>
            <li><b>Z-score Means across Clusters:</b> Heatmap chart. K in the figure above. Check to visualize.</li>
            <li><b>Z-score Means of Each Cluster:</b> Bar chart. L in the figure above. Check to visualize.</li>
            <li><b>Column Charts:</b> Enter the number of column bar charts to be visualized.</li>
            <li><b>Box Plots:</b> Enter the number of box plots to be visualized.</li>
        </ul>
        <p>Click <b>Submit</b> to run the visualization with the configured parameters.</p>
        """
    )
    
    # Display the widgets and the button
    display(widgets.VBox([
        help_content,  # Help section at the top
        empty_line, #######################    
        empty_line, #######################    
        title_input,
        subject_input,
        filename_suffix_input,
        empty_line, #######################       
        input_csv_input,
        shapefile_input,
        disaster_csv_input,
        empty_line, ####################### 
        years_input,
        normalization_csv_input,
        normalization_unit_input,
        rate1_input,
        empty_line, ####################### 
        method_dropdown,
        nClusters_dropdown,
        empty_line, #######################    
        variables_listbox,
        empty_line, #######################
        checkbox_label,
        Distribution_of_Subject_checkbox,
        Zscore_Means_across_Clusters_checkbox,
        Zscore_Means_of_Each_Cluster_checkbox,
        barcharts_dropdown,
        boxplots_dropdown,
        empty_line, #######################
        run_button,
        output
    ], layout=widgets.Layout(width='100%', border='solid 1px #10A5F5', padding='50px')))
    
    # Function to gather inputs when needed
    def get_inputs():
        return {
            'title': title_input.value,
            'subject': subject_input.value,
            'filename_suffix': filename_suffix_input.value,
            'inputCSV': input_csv_input.value,
            'shapefile': shapefile_input.value,
            'disasterInputCSV': disaster_csv_input.value,
            'rate1': rate1_input.value,
            'normalizationCSV': normalization_csv_input.value,
            'normalizationUnit': int(normalization_unit_input.value),
            'years': [int(y.strip()) for y in years_input.value.split(',')],
            'method': method_dropdown.value,
            'nClusters': nClusters_dropdown.value,
            'variables': list(variables_listbox.value),
            'Distribution_of_Subject': Distribution_of_Subject_checkbox.value,
            'Zscore_Means_across_Clusters': Zscore_Means_across_Clusters_checkbox.value,
            'Zscore_Means_of_Each_Cluster': Zscore_Means_of_Each_Cluster_checkbox.value,
            'Number_of_Column_Charts_for_Subject_Clusters': barcharts_dropdown.value,
            'Number_of_BoxPlots_for_Subject_Clusters': boxplots_dropdown.value
        }    

    
if __name__ == '__main__':
    started_datetime = datetime.now()
    print('VulnerableNeighborhoodExplorer start at %s' % (started_datetime.strftime('%Y-%m-%d %H:%M:%S')))
    
    #sample = "downloads/LTDB_Std_All_Sample.zip"
    #full = "downloads/LTDB_Std_All_fullcount.zip"
    #store_ltdb(sample=sample, fullcount=full)
    #store_census()

    param_NYC = {
        'title': "Vulnerable Neighborhood to COVID-19, NYC",
        'subject': "COVID-19",
        'filename_suffix': "New_York_kmeans_C9",
        'inputCSV': "input_NYC\ACS_2018_5year__zipcode_NYC_byZipcode_normalized.csv",
        'shapefile': "input_NYC\zipcode_NYC.shp",
        'disasterInputCSV': "input_NYC\COVID_NYC_20200711_revised.csv",
        'rate1': 'Confirmed rate = _count/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1. 
        'rate2': 'Case fatality rate = _deaths/_count',			# Formula to compute rate2 in subjectCSV such as death rate2.        
        #'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # demoninator, per number of pop. 
        'normalizationCSV': "input_NYC\Decision_Normalization_NYC.csv",        # divisor instead of population from CSV file
        'normalizationUnit': 10000,               # default: 10000
        'years': [2018],        
        'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                          # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
        'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
        #'label': "short_name",
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
        'Distribution_of_Subject': True,                        # density chart: INC changes as the map extent changes 
        'Distribution_of_Subject_different_period': False,       # density chart: INC changes by different years 
        'Distribution_of_Subject_different_cluster': False,      # density chart: INC changes by different clusters 
        'Zscore_Means_across_Clusters': True,                   # heatmap: Z Score Means across Clusters
        'Zscore_Means_of_Each_Cluster': False,                  # barchart: Z Score Means of Each Cluster
        'Number_of_Column_Charts_for_Subject_Clusters': 1,
        'Number_of_BoxPlots_for_Subject_Clusters': 1,
    }

    param_Phoenix = {
        'title': "Vulnerable Neighborhood to COVID-19, Phoenix",
        'subject': "COVID-19",
        'filename_suffix': "Phoenix_kmeans_C5",
        'inputCSV': "input_Phoenix\ACS_2018_5year__zipcode_AZ_Maricopa_byZipcode_normalized.csv",
        'shapefile': "input_Phoenix\AZ_maricopa.shp",	
        'disasterInputCSV': "input_Phoenix\COVID_20200715_Arizona.csv",
        'rate1': 'Confirmed (%) = _count/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1. 
        #'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # denominator, per number of pop. 		
        'normalizationCSV': "Decision_Normalization.csv",            # divisor instead of population from CSV file	  
        'normalizationUnit': 10000,               # default: 10000
        'years': [2018],        
        'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                             # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
        'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
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
        'Distribution_of_Subject': True,                   #density chart: INC changes as the map extent changes 
        'Zscore_Means_across_Clusters': True,
        'Zscore_Means_of_Each_Cluster': True,
        'Number_of_Column_Charts_for_Subject_Clusters': 1,
        'Number_of_BoxPlots_for_Subject_Clusters': 1,
    }

    param_Miami = {
         'title': "Vulnerable Neighborhood to COVID-19, Miami",
         'subject': "COVID-19",
         'filename_suffix': "Miami_kmeans_C5", 
         'inputCSV': "input_Miami\ACS_2018_5year__zipcode_Miami_byZipcode_normalized.csv",   
         'shapefile': "input_Miami\Miami4.shp",
         'disasterInputCSV': "input_Miami\COVID_Florida_20200717.csv", 
         'rate1': 'Confirmed (%) = _count/_tested',# Formula to compute rate1 in subjectCSV such as confirmed rate1. 	
         #'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # denominator, per number of pop. 		
         'normalizationCSV': "Decision_Normalization.csv",            # divisor instead of population from CSV file			
         'normalizationUnit': 10000,               # default: 10000
         'years': [2018],        
         'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                              # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
         'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
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
         'Distribution_of_Subject': True,                   #density chart: INC changes as the map extent changes 
         'Zscore_Means_across_Clusters': True,
         'Zscore_Means_of_Each_Cluster': True,
         'Number_of_Column_Charts_for_Subject_Clusters': 1,
         'Number_of_BoxPlots_for_Subject_Clusters': 1,
    }

    param_extended_Chicago = {
        'title': "Vulnerable Neighborhood to COVID-19, Chicago",
        'subject': "COVID-19",
        'filename_suffix': "Chicago_extended_kmeans_C5",
        'inputCSV': "input_extended_Chicago\ACS_2018_5year__zipcode_extended_Chicago_byZipcode_normalized.csv",
        'shapefile': "input_extended_Chicago\Chicago_extended.shp",
        'disasterInputCSV': "input_Chicago\COVID_IL_20200711.csv",
        'rate1': 'Confirmed (%) = _count/_tested',        # Formula to compute rate1 in subjectCSV such as confirmed rate1. 
        #'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # denominator, per number of pop.         
        'normalizationCSV': "input_Chicago\Decision_Normalization_Chicago.csv",            # divisor instead of population from CSV file    
        'normalizationUnit': 10000,               # default: 10000
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
        'Distribution_of_Subject': True,                   #density chart: INC changes as the map extent changes 
        'Zscore_Means_across_Clusters': True,
        'Zscore_Means_of_Each_Cluster': True,
        'Number_of_Column_Charts_for_Subject_Clusters': 3,
        'Number_of_BoxPlots_for_Subject_Clusters': 3,
    }

    param_Illinois = {
        'title': "Vulnerable Neighborhood to COVID-19, Illinois",
        'subject': "COVID-19",
        'filename_suffix': "Illinois_kmeans_C5",
        'inputCSV': "input_Illinois\ACS_2018_5year__zipcode_IL_byZipcode_normalized.csv",
        'shapefile': "input_Illinois\zipcode_IL.shp",
        'disasterInputCSV': "input_Chicago\COVID_IL_20200711.csv",
        'rate1': 'Confirmed (%) = _count/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1. 
        #'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # denominator, per number of pop. 		
        'normalizationCSV': "Decision_Normalization.csv",            # divisor instead of population from CSV file	
        'normalizationUnit': 10000,               # default: 10000
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
        'Distribution_of_Subject': True,                   #density chart: INC changes as the map extent changes 
        'Zscore_Means_across_Clusters': True,
        'Zscore_Means_of_Each_Cluster': True,
        'Number_of_Column_Charts_for_Subject_Clusters':3,
        'Number_of_BoxPlots_for_Subject_Clusters': 3,	
    }

    param_US = {
        'title': "Vulnerable Neighborhood to COVID-19, US",
        'subject': "COVID-19",
        'filename_suffix': "US_kmeans_C5", 
        'inputCSV': "input_US\ACS_2018_5year__County_US_byCounty_normalized.csv",   
        'shapefile': "input_US\counties_mainland_US.shp", 		
        'disasterInputCSV': "input_US\COVID_us_counties.csv", 
        'rate2': 'Case fatality rate = _deaths/_count',			# Formula to compute rate2 in subjectCSV such as death rate2.       
        #'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # denominator, per number of pop. 		
        'normalizationCSV': "input_US\Decision_Normalization_US.csv",            # divisor instead of population from CSV file	
        'normalizationUnit': 10000,               # default: 10000
        'years': [2018],        
        'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                             # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
        'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
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
        'Distribution_of_Subject': True,                   #density chart: INC changes as the map extent changes 
        'Zscore_Means_across_Clusters': True,
        'Zscore_Means_of_Each_Cluster': True,
        'Number_of_Column_Charts_for_Subject_Clusters': 3,
        'Number_of_BoxPlots_for_Subject_Clusters': 3,
    }
    
    param_Chicago_v2 = {
        'title': "CDC SVI, COVID19 test and vaccinated rates, Chicago",
        'subject': "COVID-19",
        'filename_suffix': "Chicago_kmeans_C5_v2",
        #'inputCSV': "input_Chicago\ChicagoMSA_SVI_byZipcode_v2.csv",
        'inputCSV': "input_extended_Chicago\ACS_2018_5year__zipcode_extended_Chicago_byZipcode_normalized.csv",
        'shapefile': "input_Chicago\Zipcode_Chicago_MSA2.shp",
        'disasterInputCSV': "input_Chicago\COVID19_Vaccine_rate_sites_data_ChicagoMSA.csv",        
        #'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # denominator, per number of pop.
        'normalizationCSV': "input_Chicago\Decision_Normalization_Chicago.csv",            # divisor instead of population 
        'normalizationUnit': 10000,               # default: 10000
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
        'Distribution_of_Subject': True,                   #density chart: INC changes as the map extent changes 
        'Zscore_Means_across_Clusters': True,
        'Zscore_Means_of_Each_Cluster': True,
        'Number_of_Column_Charts_for_Subject_Clusters': 1,
        'Number_of_BoxPlots_for_Subject_Clusters': 1,    
    }
    
    param_Chicago = {
        'title': "Vulnerable Neighborhood to COVID-19, Chicago",
        'subject': "COVID-19",
        'filename_suffix': "Chicago_kmeans_C5",
        'inputCSV': "input_Chicago/ACS_2018_5year__zipcode_Cook_byZipcode_normalized.csv",
        'shapefile': "input_Chicago/zipcode_Cook_County.shp",
        'disasterInputCSV': "input_Chicago/COVID_IL_20200711.csv",
        'rate1': 'Confirmed (%) = _count/_tested',      # Formula to compute rate1 in subjectCSV such as confirmed rate1.        
        #'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # denominator, per number of pop.
        #'subjectNormalizationCSV': "input_Chicago/Decision_Normalization_Chicago.csv", # divisor instead of population from CSV file
        'normalizationCSV': "input_Chicago/Normalization_Table_Chicago.csv", # divisor instead of population from CSV file
        'normalizationUnit': 100000,               # default: 10000
        'years': [2018],     # must be one element
        #'cluster' : '2018', # default is 1st year
        'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                             # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
        'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
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
        'Distribution_of_Subject': True,                   #density chart: INC changes as the map extent changes 
        'Zscore_Means_across_Clusters': True,
        'Zscore_Means_of_Each_Cluster': True,
        'Number_of_Column_Charts_for_Subject_Clusters': 2,
        'Number_of_BoxPlots_for_Subject_Clusters': 2,
    }   
    
    # param_NYC, param_Chicago, param_Phoenix, param_Miami, param_extended_Chicago, param_Illinois, param_US, param_Chicago_v2
    Vulnerability_viz(param_Chicago)
    ended_datetime = datetime.now()
    elapsed = ended_datetime - started_datetime
    total_seconds = int(elapsed.total_seconds())
    hours, remainder = divmod(total_seconds,60*60)
    minutes, seconds = divmod(remainder,60)	
    print('VulnerableNeighborhoodExplorer ended at %s    Elapsed %02d:%02d:%02d' % (ended_datetime.strftime('%Y-%m-%d %H:%M:%S'), hours, minutes, seconds))