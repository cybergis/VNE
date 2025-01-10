
# Vulnerable Neighborhood Explorer (VNE)

<h3 align="center" style="margin-top:-10px">Vulnerable Neighborhood Explorer (VNE) is an open-source visual analytics tool for exploring social vulnerability across different neighborhoods</h3> 

VNE is a cyberGIS-based visual analytics tool that allows users to (1) delineate neighborhoods based on their selection of variables describing socioeconomic and demographic profiles and (2) explore which neighborhoods are susceptible to the impacts of disasters based on specific socioeconomic and demographic characteristics. [Firefox](https://www.mozilla.org/en-US/firefox/new/) or [Google Chrome](https://www.google.com/chrome/download) is the recommended web browser for reaping the best performance of VNE.

## Table of Contents
- [Getting Started](#Getting-Started)
- [Input parameter description](#parameter)
- [Example Result Visualization](#Example)
- [A Case Study](#Case)
- [Interactive Features of the Visual Interface (Tutorial Videos are included)](#Interactive)
- [Data](#Data)
- [Related Resources](#Resources)
- [Contributors](#Contributors)
- [References](#References)
- [License](#License)

<h2 id="Getting-Started"> Getting Started</h2>
**You can run VNE in your Jupyter Notebook/Lab installed on your PC as well as in CybearGISX. We recommend that you use CyberGISX because all the required packages have been integrated in CyberGISX.**<br/><br/>

**To use it in CyberGISX, follow steps below:**
1. If you do not have a CyerGISX account, create a CyberGISX account with your institution's email address or Google email address at  [https://cybergisxhub.cigi.illinois.edu](https://cybergisxhub.cigi.illinois.edu)
2. Once you log in CyberGISX, go to [https://cybergisxhub.cigi.illinois.edu/notebook/vulnerable-neighborhood-explorer](https://cybergisxhub.cigi.illinois.edu/notebook/vulnerable-neighborhood-explorer), and click the button "Open with CyberGISX".  Wait for 3 to 5 seconds. All related source codes will be automatically copied, and the main notebook will be opened. Then, click the “play button” at the top to run.

**A video tutorial on using VNE in CyberGISX**

*Note: The video is currently muted by default. Please unmute the video before playing to hear the audio.*
<video src="https://github.com/user-attachments/assets/9b7b673c-9118-4a99-b228-89209fbc8b1e" controls autoplay></video>


<h2 id="parameter"> Input Parameter Description</h2>
                                                       
<table border="1" cellpadding="5" cellspacing="0">
  <thead>
    <tr>
      <th><b>Parameter</b></th>
      <th><b>Description</b></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>‘title’</b></td>
      <td>Enter a descriptive title for the visualization. Texts will be placed at the top of the result visualization.</td>
    </tr>
    <tr>
      <td><b>‘subject’</b></td>
      <td>Specify the subject matter (e.g., COVID-19). Texts will be placed at the top of the maps, column bar charts, and box plots.</td>
    </tr>
    <tr>
      <td><b>‘inputCSV’</b></td>
      <td>Provide the path to your input CSV file. The file should include socioeconomic, demographic, and health status data. Ensure that the first column is labeled <code>geoid</code> and the second column is labeled <code>year</code>. All subsequent columns will be available for selection in the Variables input box below.</td>
    </tr>
    <tr>
      <td><b>‘shapefile’</b></td>
      <td>Enter the path to the shapefile. A shapefile is used to visualize polygons on the map. The first column header must start with <code>geoid</code>, and the code should match the <code>geoid</code> column of another input CSV file that you enter for <code>inputCSV</code> and <code>disasterInputCSV</code>.</td>
    </tr>
    <tr>
      <td><b>‘disasterInputCSV’</b></td>
      <td>Enter the path to your input CSV file containing data representing the number of disaster-affected people. In the case of COVID-19, the file can contain the number of confirmed cases, COVID-19 testing cases, and deaths. Ensure that the first column is labeled <code>geoid</code>.</td>
    </tr>
    <tr>
      <td><b>‘rate1’</b></td>
      <td>Primarily used for disease data. Computes the percentage using two variables in <code>disasterInputCSV</code>. For example, if the CSV file contains columns like <code>total_count</code> (number of confirmed cases) and <code>total_test</code> (number of individuals tested), you can define <code>Confirmed (%) = total_count / total_test * 100</code>. This will compute and display <code>total_Confirmed (%)</code> in the result visualization. The column names in the input CSV file assigned to <code>disasterInputCSV</code> must include underscore (_). When you define it like above case, the program identifies variables ending with <code>_count</code> and divides them by variables ending with <code>_test</code> for the calculation. Similarly, <code>rate2</code> can be used as <code>Death (%) = total_deaths / total_cases * 100</code> to compute and visualize the fatality rate. </td>
    </tr>
    <tr>
      <td><b>‘normalizationCSV’</b></td>
      <td>Enter the path to your input CSV file. The first column should contain column headers from <code>disasterInputCSV</code>, and the second column should contain column headers from <code>inputCSV</code>. For example, entering <code>total_count</code> in the first column and <code>Population</code> in the second column will compute <code>total_count / Population * normalizationUnit</code>.</td>
    </tr>
    <tr>
      <td><b>‘normalizationUnit’</b></td>
      <td>Set the normalization value (e.g., 10,000). For instance, if you set this to 10,000 and use <code>total_count / Population</code> from <code>normalizationCSV</code>, it will compute <code>total_count / Population * 10,000</code>. The result will be visualized as <code>total_count (/10K pop)</code> on the first map, column bar charts, and box plots.</td>
    </tr>
    <tr>
      <td><b>‘years’</b></td>
      <td>List the years for the analysis. This value should match the second column of the input CSV. It will be displayed at the top of the neighborhood map.</td>
    </tr>
    <tr>
      <td><b>‘method’</b></td>
      <td>Clustering algorithms used to identify neighborhood types. Enter one of the following methods: <code>kmeans</code>, <code>ward</code>, <code>affinity_propagation</code>, <code>spectral</code>, <code>gaussian_mixture</code>. For detailed information about each method, refer to the <i>Neighborhood Clustering Methods</i> section in the <i>Analyze Module</i> of the Geospatial Neighborhood Analysis Package (GEOSNAP).</td>
    </tr>
    <tr>
      <td><b>‘nClusters’</b></td>
      <td>Specify the number of clusters.</td>
    </tr>
    <tr>
      <td><b>‘variables’</b></td>
      <td>Select variables to be computed from <code>inputCSV</code>. Below is the full description of eighteen variables used in the example:</td>
    </tr>
    <tr>
      <td colspan="2">
        <ul>
          <li><b>Median monthly housing costs:</b> Median monthly housing costs.</li>
          <li><b>% below poverty:</b> Percentage of the population in poverty.</li>
          <li><b>% unemployed:</b> Percentage of the unemployed population.</li>
          <li><b>% with 4-year college degree:</b> Percentage of the population with at least a four-year college degree.</li>
          <li><b>% manufacturing:</b> Percentage of manufacturing employees (by industries).</li>
          <li><b>% service industry:</b> Percentage of service employees (by industries).</li>
          <li><b>% structures more than 30 years old:</b> Percentage of structures built more than 30 years ago.</li>
          <li><b>% households moved <10 years ago:</b> Percentage of household heads who moved into the unit less than 10 years ago.</li>
          <li><b>% multiunit structures:</b> Percentage of housing units in multi-unit structures.</li>
          <li><b>% owner-occupied housing:</b> Percentage of owner-occupied housing units.</li>
          <li><b>% vacant housing:</b> Percentage of vacant housing units.</li>
          <li><b>% > 60 years old:</b> Percentage of the population aged 60 years and over.</li>
          <li><b>% < 18 years old:</b> Percentage of the population aged 17 years and under.</li>
          <li><b>% white:</b> Percentage of persons of white race, not Hispanic origin.</li>
          <li><b>% Asian:</b> Percentage of persons of Asian race (and Pacific Islander).</li>
          <li><b>% Hispanic:</b> Percentage of persons of Hispanic origin.</li>
          <li><b>% black:</b> Percentage of persons of black race, not Hispanic origin.</li>
          <li><b>% foreign:</b> Percentage of the foreign-born population.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td><b>‘Distribution_of_Subject’</b></td>
      <td>A1 in Fig1. Enter <code>True</code> to display or <code>False</code> not to display.</td>
    </tr>
    <tr>
      <td><b>‘Zscore_Means_across_Clusters’</b></td>
      <td>A in Fig2. Enter <code>True</code> to display or <code>False</code> not to display.</td>
    </tr>
    <tr>
      <td><b>‘Zscore_Means_of_Each_Cluster’</b></td>
      <td>B in Fig2. Enter <code>True</code> to display or <code>False</code> not to display.</td>
    </tr>
    <tr>
      <td><b>‘Number_of_Column_Charts_for_Subject_Clusters’</b></td>
      <td>The number of column bar charts displayed in Fig1.</td>
    </tr>
    <tr>
      <td><b>‘Number_of_BoxPlots_for_Subject_Clusters’</b></td>
      <td>The number of box plots displayed in Fig1.</td>
    </tr>
  </tbody>
</table>


<h2 id="Example">Example Result Visualization</h2>

**Example visaulizations are available in the folders below:**<br/>
*	VNE_Chicago<br/>
*	VNE_Chicago2<br/>
*	VNE_Chicago_kmeans_C5 <br/>
*	VNE_Chicago_kmeans_C5 <br/>
*	New_York_kmeans_C5<br/>
*	Phoenix_kmeans_C5<br/>
*	Miami_kmeans_C5<br/>
*	US_kmeans_C5<br/>
*	Chicago_extended_kmeans_C5<br/>
*	Illinois_kmeans_C5 <br/>


<h2 id="Case">A Case Study</h2>

Exploring Neighborhood-level Social Vulnerability to COVID-19 in Chicago. 

Two images (Fig 1 and 2) below show the result visualization of VNE, which allow users to explore socioeconomic and demographic disparity in COVID-19 outbreaks as well as vulnerable neighborhoods and their socioeconomic and demographic characteristics. Two input data were used: 
<ul>
<li>COVID-19 confirmed and test cases at the zip code level in Chicago. They were downloaded from the website of the Illinois Department of Public Health. The data used reflects the duration of the COVID-19 outbreak until July 11th, 2020, when the data was downloaded.</li> 

<li> American Community Survey (ACS) 5-year estimates from 2014 to 2018. From ACS, 18 variables representing different socioeconomic and demographic statuses were collected.</li>
</ul>


Below is a detailed description of each chart and map that can be visualized using the Vulnerable Neighborhood Explorer (VNE).

- In __Fig1B__, users can select disaster-related data via a dropdown menu, choosing between total infection rates or rates categorized by race/ethnicity (e.g., White, Hispanic) at Zip Codes outlined in white. __Fig1A__ displays the density distribution of the selected data, providing geographic context

- __Fig1C__ presents neighborhood delineations obtained through k-means clustering of the eighteen American Community Survey variables at the census Zip Code level (as labeled on the x-axis in __Fig 2A__). Each neighborhood typically comprises multiple Zip Codes.

- __Fig1D__  shows the proportion of Zip Codes in each cluster, serving as a legend. Clusters include "White Rich Owner," "White Hispanic Aging Suburban," "Asian Elite Renter," "Hispanic Laborer," and "Black Poor." Users can name each cluster by analyzing the Z-score means of the variables using the heatmap and bar charts in  __Fig 2A and 2B__. This can be updated in Config.js by clicking the third link generated by VNE. For labeling instructions, see [*Han et al., 2023*].

- __Fig1 E-G__ display column charts of the total infection rate and the infection rates among White and Hispanic populations within each neighborhood, respectively.

- __Fig1 H-CJ__ complement these with box plots showing the distribution of these rates across the five clusters. 

- __Fig 2A and 2B__ illustrate the mean z-scores of each input variable, highlighting the distinguishing characteristics of the clusters in __Fig1C__.  Z-scores indicate how far each variable's value is from the mean. 

  - __Fig 2A__ compares the mean z-scores of the eighteen variables across the five neighborhoods.
  - __Fig 2B__ shows the sorted mean z-score for a selected neighborhood which can be chosen using the dropdown box at the top of this chart. In this case, five horizontal bar charts representing the mean z-score of each of the eighteen variables can be created on the interface of the interactive map.


<p><img src="images/Figure1.jpg" alt="Visualization of VNE - Part 1" height="800"/></p>
<p><strong>Figure 1:</strong> The initial part of the Vulnerable Neighborhood Explorer (VNE) visualization.</p>
<br></br>
<p><img src="images/Figure2.jpg" alt="Visualization of VNE - Part 2" height="600"/></p>
<p><strong>Figure 2:</strong> The subsequent part of the Vulnerable Neighborhood Explorer (VNE) visualization.</p>


<br>
<h2 id="Interactive">Interactive Features of the Visual Interface</h2>


VNE is a geovisual analytics tool that utilizes a Coordinated Multiple Views (CMV) approach, allowing users to interact with several interconnected visual representations simultaneously. This enhances the analysis of complex data relationships and facilitates the extraction of meaningful insights. 
Here is a video showcasing the visual features of the Vulnerable Neighborhood Explorer (VNE).

*Note: The video is currently muted by default. Please unmute the video before playing to hear the audio.*


https://github.com/user-attachments/assets/a96070ea-a168-4a01-9813-f951c788b8b0


<br>
To jump to specific functionalities, click the links below:
<br><br>

<ul>
  <li>
    <a href="https://github.com/user-attachments/assets/a96070ea-a168-4a01-9813-f951c788b8b0#t=0" target="_blank">
      Overview & Cross-Filtering for Maps
    </a>
  </li>
  <li>
    <a href="https://github.com/user-attachments/assets/a96070ea-a168-4a01-9813-f951c788b8b0#t=104" target="_blank">
      Local Visualization for Distribution & Proportion Charts
    </a>
  </li>
  <li>
    <a href="https://github.com/user-attachments/assets/a96070ea-a168-4a01-9813-f951c788b8b0#t=181" target="_blank">
      Disaster Impact Across Neighborhoods: Column Chart & Box Plots
    </a>
  </li>
  <li>
    <a href="https://github.com/user-attachments/assets/a96070ea-a168-4a01-9813-f951c788b8b0#t=262" target="_blank">
      Tukey's Honest Significant Difference (HSD) Test
    </a>
  </li>
  <li>
    <a href="https://github.com/user-attachments/assets/a96070ea-a168-4a01-9813-f951c788b8b0#t=345" target="_blank">
      Exploring Neighborhood Characteristics Using Z-Score Means
    </a>
  </li>
  <li>
    <a href="https://github.com/user-attachments/assets/a96070ea-a168-4a01-9813-f951c788b8b0#t=422" target="_blank">
      Change Subjects
    </a>
  </li>
  <li>
    <a href="https://github.com/user-attachments/assets/a96070ea-a168-4a01-9813-f951c788b8b0#t=464" target="_blank">
      Advanced Options & Fixed Axes for Direct Comparisons
    </a>
  </li>
  <li>
    <a href="https://github.com/user-attachments/assets/a96070ea-a168-4a01-9813-f951c788b8b0#t=605" target="_blank">
      Where Results Are Saved & Sharing Your Visualizations
    </a>
  </li>
</ul>


<br>

A key feature of CMV is cross-filtering, where actions in one view—such as selecting a region in a chart—automatically update related views. For instance, consider three visualizations: a map showing COVID-19 infection rates by Zip Code (__Fig 3A__), a map displaying different neighborhood types (__Fig 3B__), and a proportion chart of Zip Code areas per neighborhood (__Fig 3C__). When a user hovers over a neighborhood category in the proportion chart, both maps update to reflect the selected area. Hovering over "C0 White Rich Owner" highlights the data in this neighborhood on both maps, showing a generally low infection rate (__Fig 3D, E and F__). Conversely, hovering over "C4 Black Poor" highlights that neighborhood, indicating a higher infection rate (__Fig 3G, H and I__). This interactive cross-filtering enables users to compare infection rates across neighborhoods, focus on specific areas to identify localized trends, and understand how different neighborhoods relate to infection rates. In summary, VNE's CMV and cross-filtering capabilities allow for dynamic exploration and analysis of disaster-related data, such as COVID-19 infection rates, across different neighborhoods.

<p><img src="images/Fig3.jpg" alt="Visualization of VNE - Part 1" height="800"/></p>
<p><strong>Figure 3:</strong> Partial visualization of the VNE output. Panels (D) and (E) show the map view when the C0: White Rich Owner neighborhood is selected in the proportion chart (F). Panels (G) and (H) show the map view when the C4: Black Poor neighborhood is selected in the proportion chart (I). </p>
 

Another key feature of VNE is brushing, where highlighting a specific data point in one visualization, simultaneously highlighting the corresponding regions across all linked maps. On the right in __Fig 4__, the box plot depicts the distribution of COVID-19 infection rates across five neighborhoods, with each dot representing the infection rate of a specific Zip Code area. Users can lasso-select these dots (Zip Codes) on the chart, triggering the corresponding Zip Code areas to be highlighted on the two maps. In this example, the box plot focuses on the Hispanic laborer neighborhood, revealing a higher distribution of infection rates compared to other neighborhoods. By selecting areas above the 75th percentile within this neighborhood, the highlighted Zip Code areas represent the top 25% of infection rates in the Hispanic laborer neighborhood.


<p><img src="images/Fig4.jpg" alt="Visualization of VNE - Part 1" height="300"/></p>
<p><strong>Figure 4:</strong> The result visualization is created by setting only the box plots to 1 and leaving the other chart options unselected.</p>


VNE integrates synchronized map views with cross-filtering capabilities to enhance data exploration. When a user pans or zooms one map, all linked maps automatically adjust to display the same geographic area. This synchronization enables simultaneous analysis of COVID-19 infection rates and neighborhood types within focused regions. Additionally, zooming into a sub-region on the maps triggers the distribution chart to dynamically display the infection rate distribution within the current map boundaries. Furthermore, the chart illustrated in __Fig 5D__ updates in real-time to show the proportion of polygons within each neighborhood. __Fig 5__ presents maps of a region that has been zoomed in from __Fig1 A-D__. Please note that the distribution charts (__Fig 5A__) and the proportion chart (__Fig 5D__ ) appear differently in these figures, reflecting the views before and after zooming. Specifically, C2: Asian Elite Rent is not displayed in __Fig 5D__ because the zoomed-in map in __Fig 5C__ no longer includes this neighborhood once zoomed from the view shown in __Fig 1C__.


<p><img src="images/Fig5.jpg" alt="Visualization of VNE - Part 1" height="300"/></p>
<p><strong>Figure 5:</strong> Partial visualization of the VNE output. (A) illustrates the distribution of the variable selected in (B), where (B) represents the COVID-19 infection rate. (C) and (D) depict neighborhood types. These images are screen captures taken from the visualization featured in the accompanying video.</p>

 

<h2 id="Data">Data</h2>

* [American Community Survey (ACS) 5-year estimates from 2014 to 2018](https://www.census.gov/data/developers/data-sets/acs-5year.2018.html#list-tab-Z8NDSX202E05P3SE5O)
* [COVID-19 Zip Level Tests and Cases](https://dph.illinois.gov/covid19/data/data-portal/zip-level-tests-and-cases.html)

  

<h2 id="Resources">Related Resources</h2>

* [CyberGISX](https://cybergisxhub.cigi.illinois.edu/) 
* [Leaflet](https://leafletjs.com) 
* [PlotlyJS](https://plot.ly/javascript/) 
* [D3](https://d3js.org/) 
* [GEOSNAP](https://github.com/spatialucr/geosnap) 


<h2 id="Contributors">Contributors</h2>


Su Yeon Han<sup>1</sup>, Joon-Seok Kim<sup>2</sup>, Jooyoung Yoo<sup>3</sup>, Jeon-Young Kang<sup>4</sup>, Alexander Michels<sup>5</sup>, Fangzheng Lyu<sup>5</sup>, Furqan Baig<sup>5</sup>, Jinwoo Park<sup>5</sup>, Shaowen Wang<sup>5</sup>

<sup>1</sup> Geography and Environmental Studies, Texas State University, San Marcos, TX, USA  
<sup>2</sup> Computer Science, Emory University    
<sup>3</sup>Spatial Sciences Institute, University of Southern California   
<sup>4</sup> Department of Geography, Kyung Hee University, South Korea  
<sup>5</sup>CyberGIS Center for Advanced Digital and Spatial Studies, University of Illinois at Urbana-Champaign, Urbana, IL, USA


<h2 id="References">References</h2>


Han, S. Y., Kang, J. Y., Lyu, F., Baig, F., Park, J., Smilovsky, D., & Wang, S. (2023). A cyberGIS approach to exploring neighborhood‐level social vulnerability for disaster risk management. Transactions in GIS, 27(7), 1942-1958.


<h2 id="License">License</h2>

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/cybergis/VNE/blob/master/LICENSE) file for details.

-------------

If you have questions, please contact Dr. Su Yeon Han at su.han@txstate.edu at Geography and Environmental Studies, Texas State University

