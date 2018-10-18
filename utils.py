# IMPORTS

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

## GLOBAL VARIABALES (hard coded, they will never change) ###

# Add all names as key and a list of the questions they contain as list 
sections_dict = {
                 "1" : [1, 2, 3, 4, 5], 
                 "2" : [1, 2, 3, 4, 5, 6, 7, 8, 9],
                 "3" : [1, 2, 3, 4, 5, 6, 7, 8, 9],
                 "4" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                 "5" : [1, 2, 3, 4, 5, 6],
                 "6" : [1, 2, 3, 4, 5, 6],
                 "7" : [1, 2, 3, 4],
                 "8" : [1, 2, 3, 4, 5],
                 "9" : [1, 2, 3, 4, 5, 6, 7, 8],
                 "10": [1, 2, 3, 4]
                }

# List of all question numbers
questions_ls = list(sections_dict.values())

# List of all sections 
sections_ls = list(sections_dict.keys())

# List of sections max_score possible
max_scores_ls = [10, 17, 18, 20, 12, 12, 10, 10, 16, 8]

# Create dictionary to associate bands to score ranges. 
bands_dict = {0 : "Non Soddisfacente", 0.25 : "Poco Soddisfacente", 0.50 : "Soddisfacente", 0.75 : "Eccellente", 1.0 : "WhatevsThisWilNeverBeUsed"}


### FUNCTIONS DEFINITIONS ####

# Function that accesses the Google Spreadsheet. 
# Credits: www.countingcalculi.com/explanations/google_sheets_and_jupyter_notebooks/

def access_google_spreadsheet (scope = "URL", json_keyfile_name = "Name of your .json file", spreadsheet_key = "https://docs.google.com/spreadsheets/d/{WHAT IS HERE}/edit#gid=0", worksheet = "Name of the tab"):
    
    # Store credentials in variable we will then pass to the authorize function.
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_name, scope)
    
    # Store authorized Google client in a variable 
    google_client = gspread.authorize(credentials)
    
    # Allow the google client to open the spreadsheet using the spreadsheet_key, store the spreadsheet in book. 
    book = google_client.open_by_key(spreadsheet_key)

    # Which tab do we want to open?
    worksheet = book.worksheet(worksheet) 

    # Convert table data into a dataframe
    table = worksheet.get_all_values()

    # Create original DataFrame and store it in the folder. 
    orig_df = pd.DataFrame(table[1:], columns=table[0]).fillna(value=np.nan) #fill missing values with NaN

    return (orig_df)

# Function to create the list of columns to keep from the copy DataFrame. Takes a string as an argument and iteratively creates the names of the columns to keep extracting the number of the section and the the questions from the sections_dict object. Returns list of strings of the format ColumnName_SectionNumber_QuestionNumber. 

def columns_to_keep (column_str = "name"):
    columns_to_keep_ls = []
    for key_i, value_ls in sections_dict.items():
        for question_i in range(len(value_ls)):
            columns_to_keep_ls.append("{}_{}_{}".format(column_str, key_i, value_ls[question_i]))
    return (columns_to_keep_ls)


# Function that creates a df for the sections_scores. Takes the list of columns to be generated and the index. 
def create_sections_scores_df (col_ls = [], index = []):
    
    return (pd.DataFrame(data=np.NaN, index = index, columns = col_ls))


# Function that takes the name of a company and the section over which to calculate the score (as a float) - I need this for the following function. 
def calculate_section_scores(df_scores, company_name="name", section=0):
    ls = (df_scores.loc["{}".format(company_name)]
        
        # Hard code the '1' as I will always want to start from the 1st question.
        # Get length of list in questions_list corresponding to last question in that section.
        ["Score_{}_1".format(section):"Score_{}_{}".format(section, len(questions_ls[section-1]))]).values[:]
    
    # Finally calculate the score as a float.
    score_flt = (pd.to_numeric(ls).sum())/max_scores_ls[section-1]
    
    return (score_flt)

# Function that 
def populate_sections_scores_df(company_list, num_of_sections, df_scores, df_sections):
    
    # For every one of the company in the sample
    for company in company_list:
        
        # For every one of the section they have been evaluated on 
        for section_num in range(1,num_of_sections + 1): # To match human-like counting.
            
             # Populate the sections_scores_df with the results of the calculate_section_scores function
            df_sections.at[company,'Section_{}'.format(section_num)] =round((calculate_section_scores(df_scores,company_name=company, section=section_num)), 2)
            
            # Populate the average line with the average of every section
            df_sections.at["Averages", "Section_{}".format(section_num)] =round(df_sections["Section_{}".format(section_num)].mean(), 2)
            
        #Calculate the average of every company and store it the TRAC_Index column
        df_sections.at[company, "TRAC_Index"] = round(df_sections.loc[company].mean(), 2)

    return (df_sections)

def assign_bands (df_sections):
    # Loop over every company 
    for company in df_sections.index:
            
        # Handles 0.00 exeption, as it will not be true that 0.00 > 0 in the following loop. 
        if df_sections.at[company, "TRAC_Index"] == 0:
            df_sections.loc[company, "Bands"] = list(bands_dict.values())[0]
            
        # Loop backwards from the highest possible band 
        for index in reversed((range(0,5))): 

            # If score is between lower bound (included) and the upper bound (excluded) attribute corresponding band 
            if  (
                df_sections.at[company, "TRAC_Index"] < list(bands_dict.keys())[index] and
                df_sections.at[company, "TRAC_Index"] >= list(bands_dict.keys())[index-1]
                ):
                
                df_sections.loc[company, "Bands"] = list(bands_dict.values())[index-1]
                
    return (df_sections)
