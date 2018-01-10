This is an project in Udacity's data science nanodegree class. I cleaned the OpenStreetMap data for Shanghai. 

# 1 Introduction
I chose Shanghai as my studying case, simply because right now I live here. The map data of Shanghai was obtained from Mapzen, https://mapzen.com/data/metro-extracts/metro/shanghai_china/. It’s named “shanghai_china.osm”, with a size of more than 850M(of course it's not shown in this repositories). However, all operations on the full data take less than 2 minutes and < 200M memory in my laptop, so 
I use the sample file for my explorations and the code can be found in "sampleing.py". 

# 2 Cleaning
## 2.1 Drop Data Not in Shanghai
The original data includes many other information from other cities which are not needed for my case. I use regular expression to drop all data not related to Shanghai. You can find the code in "updated.py", and the updated data are stored in the file "updated.osm".

## 2.2 Check Tag Name 
I counted all tag names and attributes to check for any problematic tag and attribute name, especially for those with few counts. The output was stored in “check_items.md”. Everything seems to be right.

## 2.3 Check v Value
I examined attribute v of all tags. After exploration, attribute 'k' and its corresponding attribute v values were stored in “k_v_values_updated.md”. Some problems came out at this step.

Codes are displayed in the file "clean.py". There are two main steps for cleaning data. The "clean_element" funtion normalize "addr:postcode" and "addr:street" to select right postcode and make street name more readable. The "shape_element" function returns a list of dictionaries based on the element of XML format. Then we can see a JSON-like format for further analysis.



# 3 Export to CSV
After getting the JSON-like file "updated.txt", I can extract every field I need to export to csv file for further analyzing. Codes shown in "writCSV.py" make examples to extract all user and amenity information. 
