# Imports 

import pandas as pd
import numpy as np
from df2gspread import df2gspread as d2g
from utils import *

# Get the data from Google Spreadsheet using the parameters

copy_df = access_google_spreadsheet(
    scope = "https://spreadsheets.google.com/feeds", 
    json_keyfile_name = "Jupyter_meets_GSheet-a279ad757691.json", # This file has to be in the same folder
    spreadsheet_key = "1ANV9TXjL75vUaxxuBCvMqYgc7fgg3uruUy_BdKKyr30", # You get this from the link of the GSheet
    worksheet = "Full_DB") # Tab you want to import 
    
# Get list of columns to keep.  
cols_ls = columns_to_keep("Score") # I want to get all scores 
cols_ls.extend(("Company_Name", "Company_Sector")) # And add the name of the company and the sector they belong to

# Create the scores DataFrame, index is name of company
scores_df = copy_df[cols_ls].set_index("Company_Name")

# List of columns I will need when creating the sections_scores df
col_ls = ["Section_1", "Section_2", "Section_3", "Section_4", "Section_5", "Section_6", "Section_7", "Section_8", "Section_9", "Section_10", "TRAC_Index", "Bands"]

# Create section_scores_df
sections_scores_df = create_sections_scores_df(col_ls, index = scores_df.index)
# sections_scores_df # It works! Hurray!

# Pupulate the sections_scores_df by calculating the average per company per section and the TRAC Index.
# 10 is the number of sections I know from the methodology. 
sections_scores_df = populate_sections_scores_df(scores_df.index, len(sections_ls), scores_df, sections_scores_df)
sections_scores_df = assign_bands(sections_scores_df)

# Add columns on sector by merging initial copy DataFrame with the section scores DataFrame on Company Name. 
sections_scores_df = pd.merge(sections_scores_df,copy_df[['Company_Name','Company_Sector']],on='Company_Name', how='left')
sections_scores_df = sections_scores_df.set_index("Company_Name")

# Create dataframe to store the results of sections over the sectors
grouped_scores_df = pd.DataFrame()

for section_i in list(range(1, 11)):  
    grouped_scores_df = grouped_scores_df.append(round(sections_scores_df.groupby("Company_Sector")["Section_{}".format(section_i)].mean(), 2))

grouped_scores_df_transposed = grouped_scores_df.transpose()

# Store the all dataframes as csv in case people want to use Microsoft (Eww). 
raw_df = copy_df
raw_df.to_csv("raw_data")

scores_df.to_csv("Scores_only_data")

sections_scores_df.to_csv("Sections_scores_aggregated_data")

grouped_scores_df_transposed.to_csv("Grouped_scores_aggregated_data")