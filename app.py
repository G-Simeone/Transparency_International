######################################################################
### EXTRACTION - TRANSFORMATION - LOADING - VISUALISATION PIPELINE ###
######################################################################                

'''
Variable definition and logic is as follows (also applicable to utils.py, spidercharts.py, constants.py and company_profiles.py)

In the methodology of Transparency International (TI), the Trasparency in Corporate Reporting Index (TRAC Index) is the average of the results of the 10 sections a company has been assessed on. Each section has a different number of questions, and the section result is the weighted average of the questions scores obtained. Each question can be graded on a scale of either 0-1, 0-1-2, or 0-1-2-3, depending on the weight that TI attributes to that particular question in the section.

For every question, in the original Google Spreadsheet, there are 4 columns (Score, Source, URL, Comment) where Source is the document type where the information that underpins the attribution of the score was found, its URL and a Comment that explains why the company has got that Score (explaining how the information retrived satsfies or not TI methodology). 

The way the columns were built in the original Google Spreadsheet is this:

ColumnName_SectionNumber_QuestionNumber, example: Score_1_3 would be the Score of the 3rd question of Section 1. 

The objective of this pipeline is to:

1) Extract the raw data from the Google Spreadsheet and create a raw data and a scores only dataframes. 
2) Use the scores only dataframe to calculate the results of every section, and create a sections results dataframe. 
3) Use the sections results dataframe to group the companies by sector, recalculate the sections results by group, and 
   store these results in a sectors dataframe. 
4) Use the raw data from the Google Spreadsheet to create a .docx for every one of the companies, collating together all 
   information in the raw data in a document, creating a company profile. 
5) Create 3 spidercharts for every company, one plotting the sections results of the company only, one plotting the sections    
   results of the company with the averages results of sections in the sector of the company, and one plotting the company 
   sections results with the averages results of the sections of all companies in the sample. 
6) Create a folder strucutre where to store the dataframes as .csv and the company profiles as .docx and the visulations as  
   .png. 
'''

# Imports 

import pandas as pd
import numpy as np
from df2gspread import df2gspread as d2g
from docx import *
from utils import *
from spidercharts import *
from constants import *
from company_profiles import *
import matplotlib.pyplot as plt
import matplotlib as mpl
from math import pi

########################
### DATA EXTRACTION ####
########################

# Get the raw data from Google Spreadsheet and create a back up (copy_df) of the df and one we'll work with (raw_df).
copy_df, credentials = access_google_spreadsheet(
    scope = SCOPE, 
    json_keyfile_name = KEY, # This file has to be in the same folder
    spreadsheet = SPREADSHEET_ID, # You get this from the link of the GSheet
    worksheet = WORKSHEET) # Tab you want to import 
    
raw_df = copy_df
raw_df = raw_df.set_index("Company_Name")

############################ 
### DATA TRANSFORMATION ####  
############################

# Get the list of all scores columns + "Company_Name" and "Company_Sector" columns.  
scores_cols_ls = columns_to_keep(column = "Score", sections = SECTIONS_DICT) 
scores_cols_ls.extend(("Company_Name", "Company_Sector")) 

# Create the scores_only_df indexed on the "Company_Name" column.
scores_only_df = copy_df[scores_cols_ls].set_index("Company_Name")

# Create list of columns to create the sections_results_df, a new df with averages of every section.
sections_cols_ls = []
sections_cols_ls = list(SECTIONS_SHORT_NAMES.keys())
sections_cols_ls.extend(("TRAC_Index", "Bands"))

# Create section_df.
sections_results_df = create_sections_df(cols_ls = sections_cols_ls, index = scores_only_df.index)

# Pupulate the sections_results_df by calculating the average per company per section.
# Calculate the average of the sections averages, what Transparency International calls the "TRAC_Index".
# Note that the variables SECTIONS_LS, QUESTION_LS and MAX_RESULTS_LS are constant in constants.py. 
sections_results_df = populate_sections_df(company_list = scores_only_df.index, 
                                           num_of_sections = len(SECTIONS_LS),
                                           scores_df = scores_only_df, 
                                           sections_df = sections_results_df,
                                           questions_ls = QUESTIONS_LS, 
                                           max_results_ls = MAX_RESULTS_LS)

# Based on the "TRAC_Index" result, assign a band (unsatisfactory, satisfactory, good, excellent) see BANDS_DICT in constants.py
sections_results_df = assign_bands(sections_df = sections_results_df, bands_dict = BANDS_DICT)

# Add columns on sector by merging initial copy DataFrame with the section scores DataFrame on Company Name and reset index. 
sections_results_df = pd.merge(sections_results_df, 
                               copy_df[['Company_Name','Company_Sector']], 
                               on = 'Company_Name', 
                               how = 'left')

sections_results_df = sections_results_df.set_index("Company_Name")

# Create sectors_results_df to save the results of every sections grouped by the sectors the companies belong to. 
sectors_results_df = pd.DataFrame()

for section in list(range(1, 11)):  
    sectors_results_df = sectors_results_df.append(sections_results_df.groupby("Company_Sector")["Section_{}".format(section)]
                                                    .mean())

sectors_results_df_transposed = sectors_results_df.transpose()

####################
### DATA LOADING ###  
####################

# Let's create the folder structure on our machine where we will store the results of the analysis. 
# Note that the variable ROOT and SUB_FOLDERS_LS are constant in constants.py.
# We want to pass as list of companies only the names of the companies, remember we addes the "Average" row in
# the sections_results_df, exclude this with -1 in the slicing.
create_folders_structure(root = ROOT, sub_folders_names = SUB_FOLDERS_LS, companies_ls = sections_results_df.index[:-1])

# Replace all NaN with None for checking condition `is None` when creating the spidercharts. 
scores_only_df = scores_only_df.where(scores_only_df.notnull(), None)
sections_results_df = sections_results_df.where(sections_results_df.notnull(), None)
sectors_results_df_transposed = sectors_results_df_transposed.where(sectors_results_df_transposed.notnull(), None)

# Assign a name to every df and store them in a dictionary. 
all_dataframes_dict = {'scores_data_test' : scores_only_df,
                       'sections_results_data_test': sections_results_df,
                       'sectors_results_data_test' : sectors_results_df_transposed,
                       'raw_data_test': raw_df}

# Store the all dataframes as csv in the corresponding folders. sub_folder_ls[0] is "data", see constants.py
# Push DataFrames to Google Spreadsheet as new tabs

for key, value in all_dataframes_dict.items():
    store_file(root = ROOT, file = value, file_name = key, destination_path = SUB_FOLDERS_LS[0])
    if key is not 'raw_data_test':
        d2g.upload(value, SPREADSHEET_ID, key, credentials=credentials, row_names=True)
        
# Create customised company profiles and store them at the PATH: /deliverables/company_profile/{company_name}
create_save_company_profiles(df_raw_data = raw_df, 
                             df_sections = sections_results_df, 
                             intro_for_analysis_docx = INTRO_FOR_ANALYSIS_DOCX, 
                             sections_headings = SECTIONS_LONG_NAMES, 
                             sections_dict = SECTIONS_DICT, 
                             root = ROOT, 
                             sub_folders_names = SUB_FOLDERS_LS) 

############################
### DATA VIZUALISATIONS ####  
############################

# Create dataframes for the spidercharts and store them in a dictionary, store also every df in the folder
# of the company at the PATH: /deliverables/company_profile/{company_name}
spider_charts_dfs_dict = create_and_store_df_for_spidercharts(root = ROOT, 
                                                             sections_df = sections_results_df, 
                                                             sectors_df = sectors_results_df_transposed, 
                                                             sub_folders_names = SUB_FOLDERS_LS, 
                                                             new_cols_dict = SECTIONS_SHORT_NAMES)

# Make 3 spiderchart for every company and store them in the company folder.
make_and_save_spidercharts(df_for_spidercharts_dict = spider_charts_dfs_dict, 
                           root = ROOT, 
                           sub_folders_names = SUB_FOLDERS_LS)

