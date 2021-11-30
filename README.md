# Restaurant recommender data transformer
This collection of scripts is for transforming data collected by ZHAW for building a restaurant recommender.

# Usage
Download this repository and install the required packages with pip.
```
pip install -r requirements.txt
```
Make sure you are using python 3.7+

The script expects a dataset split into three sets. 
- User features
- Restaurant features
- Ratings

Per default the scripts looks for those files in the input directory. They have to be in a CSV format following the raw data structure defined in the data report.
To start the transforming you can execute the following command.
```
python transform.py
```
