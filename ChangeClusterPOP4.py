#!/usr/bin/env python
# coding: utf-8

import os, json, math, copy, sys, getopt
#from geosnap.data import store_ltdb
#from geosnap.io import store_ltdb
#from geosnap.data import Community
#from geosnap import Community, datasets
#from geosnap.data import store_census
#from geosnap.io import store_census
#from geosnap.data import data_store
import pandas as pd
#import shapely.wkt
#import shapely.geometry
from datetime import datetime
from datetime import timedelta
from pathlib import Path
#from INCS import linc
import urllib.parse
#import webbrowser
import pprint
#from sklearn.preprocessing import minmax_scale
#import numpy as np
#from scipy import stats
#import geopandas as gpd
import csv


def main(inputFileName):
    path, fname = os.path.split(inputFileName)
    print(path, fname)
    
    geoVariablesList = None
    geoZscores = None
    geoCluster = None
    clusterChange = None
    with open(inputFileName) as inputFile:
        inputString = inputFile.read()
        inputParts = inputString.split("var ")
        for i, inputPart in enumerate(inputParts):
            if (inputPart.startswith("GEO_VARIABLES =")):
                jString = inputPart.replace("GEO_VARIABLES =", "")
                #jString = jString.replace("\n", "")
                #print(jString)
                #print(jString[jString.find('{') : jString.rfind('}')+1])
                geoVariablesList = json.loads(jString)
                #print(geoVariablesList)
            
            if (inputPart.startswith("GEO_ZSCORES =")):
                jString = inputPart.replace("GEO_ZSCORES =", "")
                #jString = jString.replace("\n", "")
                #print(jString)
                #print(jString[jString.find('{') : jString.rfind('}')+1])
                geoZscoresList = json.loads(jString)
                #print(geoZscoresList)
            
            if (inputPart.startswith("GEO_CLUSTER =")):
                jString = inputPart.replace("GEO_CLUSTER =", "")
                #jString = jString.replace("\n", "")
                #print(jString)
                #print(jString[jString.find('{') : jString.rfind('}')+1])
                geoClusterLists = json.loads(jString)
                #print(geoClusterLists)
        
            if (inputPart.startswith("CHANGE_CLUSTER = ")):
                jString = inputPart.replace("CHANGE_CLUSTER = ", "")
                #print(jString)
                #print(jString[jString.find('{') : jString.rfind('}')+1])
                #clusterChange = json.loads(jString[jString.find('{') : jString.rfind('}')+1])
                clusterChange = json.loads(jString)
                #print(type(clusterChange), clusterChange)
                clusterChange = {int(key): value for key, value in clusterChange.items()}
                print(clusterChange)
    
    # rewrite CSV_VARIABLES
    df_geoVariables = pd.DataFrame(geoVariablesList[1:], columns=geoVariablesList[0])
    #print(df_geoVariables)
    # get years from df_geoVariables.columns
    years = []
    for column in df_geoVariables.columns:
        if (column.isnumeric()): years.append(column)      # year is must be numeric in the geoVariablesList.columns
    #print("years:", years)
    # convert values of df_geoVariables[years] using clusterChange dictionary
    for year in years:
        changedClusters = []
        for l, row in df_geoVariables.iterrows():
            changedClusters.append(clusterChange[row[year]])
        df_geoVariables[year] = changedClusters
    #print(df_geoVariables)
    #filename_GEO_VARIABLES_CSV = "VNE_" + param['filename_suffix'] + "/data/CSV_VARIABLES_"+param['filename_suffix']+".csv"
    filename_GEO_VARIABLES_CSV = path + "/" + fname.replace("GEO_VARIABLES", "CSV2_VARIABLES").replace(".js", ".csv")
    #print(filename_GEO_VARIABLES_CSV)
    df_geoVariables.to_csv(filename_GEO_VARIABLES_CSV, index=False)
    
    # rewrite CSV_ZSCORES
    df_geoZscores = pd.DataFrame(geoZscoresList['data'], columns=geoZscoresList['xAxis'])
    df_geoZscores.insert(0, "Cluster", geoZscoresList['yAxis'], True)
    #print(df_geoZscores)
    changedClusters = []
    for l, row in df_geoZscores.iterrows():
        changedClusters.append("C"+str(clusterChange[int(row['Cluster'][1:])]))
    df_geoZscores['Cluster'] = changedClusters
    #print(df_geoZscores)
    df_geoZscores = df_geoZscores.sort_values(df_geoZscores.columns[0])
    #print(df_geoZscores)
    filename_GEO_ZSCORES_CSV = path + "/" + fname.replace("GEO_VARIABLES", "CSV2_ZSCORES").replace(".js", ".csv")
    #print(filename_GEO_ZSCORES_CSV)
    df_geoZscores.to_csv(filename_GEO_ZSCORES_CSV, index=False)
    
    # rewrite CSV_CLUSTER
    for year, geoClusterList in geoClusterLists.items():
        #print(year, geoClusterList)
        heading = ["C"+str(c) for c in range(len(geoClusterList[0])-1)]
        heading.insert(0, int(year))
        #print(heading)
        df_geoCluster = pd.DataFrame(geoClusterList, columns=heading)
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
        filename_GEO_CLUSTER_CSV = path + "/" + fname.replace("GEO_VARIABLES", "CSV2_CLUSTER").replace(".js", "_"+str(year)+".csv")
        #print(filename_GEO_CLUSTER_CSV)
        df_geoCluster.to_csv(filename_GEO_CLUSTER_CSV, index=False)
    
    return

def getParameter(argv):
    inputFile = ""
    
    try:
        opts, args = getopt.getopt(argv, "hi:", ["inputFile="])
    except getopt.GetoptError:
        print("ChangeClusterPOP.py -i <inputFile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("ChangeClusterPOP.py -i <inputFile>")
            sys.exit()
        elif opt in ("-i", "--inputFile"):
            inputFile = arg
    
    print("inputFile file is {}".format(inputFile))
    return {"inputFile": inputFile}


if __name__ == '__main__':
# python ChangeClusterPOP4.py -i "VNE_0_Chicago_C5/data/GEO_VARIABLES_0_Chicago_C5.js"
# python ChangeClusterPOP4.py -i "VNE_0_New_York_C5/data/GEO_CONFIG_0_New_York_C5.js"
# python ChangeClusterPOP4.py -i "VNE_0_Phoenix_C5/data/GEO_VARIABLES_Phoenix_kmeans_C5.js"
# python ChangeClusterPOP4.py -i "VNE_0_Miami_C5/data/GEO_VARIABLES_Miami_kmeans_C5.js"
    started_datetime = datetime.now()
    print('ChangeClusterPOP start at %s' % (started_datetime.strftime('%Y-%m-%d %H:%M:%S')))
    
    parameter = getParameter(sys.argv[1:])
    inputFile = parameter["inputFile"]
    
    main(inputFile)
    
    ended_datetime = datetime.now()
    elapsed = ended_datetime - started_datetime
    total_seconds = int(elapsed.total_seconds())
    hours, remainder = divmod(total_seconds,60*60)
    minutes, seconds = divmod(remainder,60)	
    print('ChangeClusterPOP ended at %s    Elapsed %02d:%02d:%02d' % (ended_datetime.strftime('%Y-%m-%d %H:%M:%S'), hours, minutes, seconds))
    
