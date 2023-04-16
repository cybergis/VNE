// Define the number of maps and some configuration parameters that you want to visualize.

var SubjectName = "COVID-19"; //Display the name of quantitative map on the left
var QualitativeMap_Name = "Neighborhood"; //Display the name of qualitative map on the right
var QualitativeMap_Field = [2018]; //Assign the field of qualitative map on the right 
var InitialLayers = [" total_count (/10K pop)", "2018"];
var InitialCharts = [" total_count (/10K pop)", " total_tested (/10K pop)", " total_Confirmed (%)"];
var QualitativeMap_Labels = {"C0": "C0 White Rich Owner", "C1": "C1 White Hispanic Aging Suburban", "C2": "C2 Asian Elite Renter", "C3": "C3 Hispanic Laborer", "C4": "C4 Black Poor"};
//var QualitativeMap_Labels = {};


/* Map Extent and Zoom level will be automatically adjusted when you do not define map center and zoom level */
//var Initial_map_center = [34.0522, -117.9];  
//var Initial_map_zoom_level = 8;   

var Maps_of_Subject = true;									//choropleth map: Maps representing subject
var Maps_of_neighborhood = true;							//choropleth map: Maps representing clustering result  
var Distribution_of_Subject = true;							//density chart: INC changes as the map extent changes 
var Distribution_of_Subject_different_period = false;		//density chart: INC changes by different years
var Distribution_of_Subject_different_cluster = false;		//density chart: INC changes by different clusters
var Temporal_change_in_neighborhoods = false;				//stacked chart: Temporal Change in Neighborhoods over years
var Parallel_Categories_Diagram_in_neighborhoods = true;	//parallel categories diagram
var Chord_Diagram_in_neighborhoods = true;					//chord diagram
var Zscore_Means_across_Clusters = true;					//heatmap: Z Score Means across Clusters
var Zscore_Means_of_Each_Cluster = true;					//barchart: Z Score Means of Each Cluster
var Barchart_of_Subject_Clusters = 3;						//Number of subject barchart for cluster count
var BoxPlot_of_Subject_Clusters = 0;						//Number of subject box plot for cluster count
  

var Num_Of_Decimal_Places = 2;                             // default = 2

var Map_width  = "450px";                                  // min 350px
var Map_height = "500px";                                  // min 300px


/////////////////////////////////////////////////////////////////
// Options for only INC map                                    //
/////////////////////////////////////////////////////////////////

//option for class(the classification method): equal, quantile, ckmeans, std, arithmetic, geometric
//option for count(the number of classes): 1 to 8  (Only Red color scheme has up to 10)
//options for color scheme of INC map: Green, Blue, Orange, Red, Pink

var mapAclassification = {class: 'quantile', count: 8, color: 'Orange'};

/////////////////////////////////////////////////////////////////
// Options for change order of clusters for visualization      //
// uncomment below and enter cluster numbers in from:to format //
/////////////////////////////////////////////////////////////////
//var CHANGE_CLUSTER = { 0:0, 1:1, 2:2, 3:3, 4:4, 5:5 }