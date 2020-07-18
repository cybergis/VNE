# Vulnerable Neighborhood Explorer (VNE)
This is currently under development as of 7/17/2020
#### GEOSNAP needs to be installed to run VNE.
geosnap development is hosted on [github](https://github.com/spatialucr/geosnap)
To get started with the development version,
clone this repository or download it manually then `cd` into the directory and run the
following commands:

```bash
conda env create -f environment.yml
conda activate geosnap 
python setup.py develop
```
This will download the appropriate dependencies and install geosnap in its own conda environment.
After the installation above is done run VNE in the geosnap environment. 

### How to run:
- python vulnerablePOP4.py
### All input parameters are available in param3 in vulnerablePOP4.py
### Input parameters for different cities
- ##### Chicago
		'title': "Vulnerable Neighborhood to COVID-19, Chicago",
		'subject': "COVID-19",
        'filename_suffix': "Chicago_kmeans_C5",
        'inputCSV': "ACS_2018_5year__zipcode_Cook_byZipcode_normalized.csv",
		'shapefile': "zipcode_Cook_County.shp",
		'diseaseInputCSV': "COVID_20200710_zipcode_Cook.csv",
        'rate1': 'Confirmed (%) = _count/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1. 
        #'rate1': 'Confirmed (%) = _cases/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1.		
		#'rate2': 'Death (%) = _deaths/_cases',			# Formula to compute rate2 in subjectCSV such as death rate2.        
		'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # demoninator, per number of pop. 
		'years': [2018],        
		'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                             # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
		'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
		'label': "variable",
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
		'Number_of_Barcharts_for_Subject_Clusters': 2,

- ##### New York City
		'title': "Vulnerable Neighborhood to COVID-19, NYC",
		'subject': "COVID-19",
        'filename_suffix': "NYC_kmeans_C5",
	    'inputCSV': "ACS_2018_5year__zipcode_NYC_byZipcode_normalized.csv",
		'shapefile': "zipcode_NYC.shp",
		'diseaseInputCSV': "COVID_NYC_20200711_revised.csv",
        'rate1': 'Confirmed (%) = _count/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1. 
		'rate2': 'Death (%) = _deaths/_count',			# Formula to compute rate2 in subjectCSV such as death rate2.        
		'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # demoninator, per number of pop. 
		'years': [2018],        
		'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                             # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
		'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
		'label': "variable",
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
		'Number_of_Barcharts_for_Subject_Clusters': 2,
- ##### Phoenix
		'title': "Vulnerable Neighborhood to COVID-19, Phoenix",
		'subject': "COVID-19",
        'filename_suffix': "Phoenix_kmeans_C5",
		'inputCSV': "ACS_2018_5year__zipcode_AZ_Maricopa_byZipcode_normalized.csv",
		'shapefile': "AZ_maricopa.shp",	
		'diseaseInputCSV': "COVID_20200715_Arizona.csv",
        #'rate1': 'Confirmed (%) = _count/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1. 
		#'rate2': 'Death (%) = _deaths/_cases',			# Formula to compute rate2 in subjectCSV such as death rate2.        
		'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # demoninator, per number of pop. 
		'years': [2018],        
		'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                             # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
		'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
		'label': "variable",
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
		'Number_of_Barcharts_for_Subject_Clusters': 2,
- ##### Extended Chicago 
		'title': "Vulnerable Neighborhood to COVID-19, Extended Chicago",
		'subject': "COVID-19",
        'filename_suffix': "Extended_Chicago_kmeans_C5",
		'inputCSV': "ACS_2018_5year__zipcode_extended_Chicago_byZipcode_normalized.csv",
		'shapefile': "Chicago_extended.shp",
		'diseaseInputCSV': "COVID_20200710_zipcode_extended_Chicago.csv",	
        'rate1': 'Confirmed (%) = _count/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1. 	
		#'rate2': 'Death (%) = _deaths/_cases',			# Formula to compute rate2 in subjectCSV such as death rate2.        
		'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # demoninator, per number of pop. 
		'years': [2018],        
		'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                             # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
		'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
		'label': "variable",
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
		'Number_of_Barcharts_for_Subject_Clusters': 2,
- ##### Illinois
		'title': "Vulnerable Neighborhood to COVID-19, Illinois",
		'subject': "COVID-19",
        'filename_suffix': "Illinois_kmeans_C5", 
		'inputCSV': "ACS_2018_5year__zipcode_IL_byZipcode_normalized.csv",
		'shapefile': "zipcode_IL.shp",
		'diseaseInputCSV': "COVID_IL_20200711.csv",
        'rate1': 'Confirmed (%) = _count/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1. 	
		#'rate2': 'Death (%) = _deaths/_cases',			# Formula to compute rate2 in subjectCSV such as death rate2.        
		'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # demoninator, per number of pop. 
		'years': [2018],        
		'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                             # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
		'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
		'label': "variable",
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
		'Number_of_Barcharts_for_Subject_Clusters': 2,
- #### Miami
		'title': "Vulnerable Neighborhood to COVID-19, Miami",
		'subject': "COVID-19",
        'filename_suffix': "Miami_kmeans_C5", 
		'inputCSV': "ACS_2018_5year__zipcode_Miami_byZipcode_normalized.csv",   
		'shapefile': "Miami4.shp", 		
		'diseaseInputCSV': "COVID_Florida_20200717.csv", 
        #'rate1': 'Confirmed (%) = _count/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1. 	
		#'rate2': 'Death (%) = _deaths/_cases',			# Formula to compute rate2 in subjectCSV such as death rate2.        
		'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # demoninator, per number of pop. 
		'years': [2018],        
		'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                             # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
		'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
		'label': "variable",
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
		'Number_of_Barcharts_for_Subject_Clusters': 2,

- #### US
		'title': "Vulnerable Neighborhood to COVID-19, US",
		'subject': "COVID-19",
        'filename_suffix': "US_kmeans_C5", 
		'inputCSV': "ACS_2018_5year__County_US_byCounty_normalized2.csv",   
		'shapefile': "counties_mainland_US.shp", 		
		'diseaseInputCSV': "COVID_us_counties.csv", 
        #'rate1': 'Confirmed (%) = _count/_tested',		# Formula to compute rate1 in subjectCSV such as confirmed rate1. 	
		'rate2': 'Death (%) = _deaths/_cases',			# Formula to compute rate2 in subjectCSV such as death rate2.        
		'subjectNormalization': '(/10k pop) = all * 10000.0 / Population',  # demoninator, per number of pop. 
		'years': [2018],        
		'method': "kmeans",  # Aspatial Clustering: affinity_propagation, gaussian_mixture, hdbscan, kmeans, spectral, ward
                             # Spatial Clustering: azp, max_p, skater, spenc, ward_spatial   
		'nClusters': 5,      # This option should be commented out for affinity_propagation and hdbscan
		'label': "variable",
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
		'Number_of_Barcharts_for_Subject_Clusters': 2,		

-------------
If you have questions, please contact Dr. Su Yeon Han at suhan2@illinois.edu at CyberGIS Center for Advanced Digital and Spatial Studies.
