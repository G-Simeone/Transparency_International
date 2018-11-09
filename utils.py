#############################
### FUNCTIONS DEFINITIONS ###
###    In order of call   ###
###       in app.py       ###
#############################

# Imports

import pandas as pd
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import pathlib
from param import *

def access_google_spreadsheet (scope = "URL", json_keyfile_name = "Name of your .json file", spreadsheet_key = "https://docs.google.com/spreadsheets/d/{WHAT IS HERE}/edit#gid=0", worksheet = "Name of the tab"):
    
    '''
    Function that accesses Google Spreadsheet tab. 
    
    credits: www.countingcalculi.com/explanations/google_sheets_and_jupyter_notebooks/
    params: scope (string type of an URL).
            json_key_file_name (name of the json file saved in the same folder as utils.py).
            speadsheet_key (key of the spreadsheet to identify it).
            worksheet (tab of the spreadsheet).
    return: orig_df (dataframe where the data has been loaded). 
    '''
    
    # Create credentials.
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_name, scope)
    
    # Create google_client. 
    google_client = gspread.authorize(credentials)
    
    # Use google_client to open the Google Spreadsheet using spreadsheet_key. 
    book = google_client.open_by_key(spreadsheet_key)

    # Choose tab to extract data from.
    worksheet = book.worksheet(worksheet) 

    # Convert table data into a dataframe
    table = worksheet.get_all_values()

    # Create orig_df. 
    orig_df = pd.DataFrame(table[1:], columns=table[0]).fillna(value=np.nan)

    return (orig_df)


def columns_to_keep (column, sections):
    
    '''
    Function that creates a list of strings representing the names of the columns we will want to slice raw_df. All columns in
    the raw_df are numbered following a nested logic (column_NumSection_NumQuestion, e.g. Score_1_2 is the column where all
    scores for question 2 of section 1 have been stacked). 
    
    ColumnName can be one of the following: Score [score assigned during the data collection], Source [document where the 
    information to give a certain score was found], URL [the url where the source can be found], Comment [the reason why a 
    certain score has been attributed]. 
    
    In app.py we will be extracting all "Score_NumSection_NumQuestion" columns. 
    
    params: column_str (string type, user chooses from Score, Source, Comment, URL).
    return: columns_to_keep_ls (list of strings, represeting the columns to slice raw_df).
    '''
    
    # Create empty list.
    columns_to_keep_ls = []
    
    # Extract from a dictionary type the section (key) and the list of question numbers (value). This dictionary is created in
    # param.py as a constant and this whole ETL pipeline changes based on that dictionary elements. 
    for key, value in sections.items():
        for question in range(len(value)):
            columns_to_keep_ls.append("{}_{}_{}".format(column, key, value[question]))
            
    return (columns_to_keep_ls)


def create_sections_df (index, cols_ls):
    
    '''
    Function that creates a df for the sections results.
    params: cols_ls (list of strings type, names of columns for the df).
            index (index object, passed from the index of another df we want to be indexed the same)
    return: pd.DataFrame (df, filled with NaN, indexed on index and with columns cols_ls).
    ''' 
    
    return (pd.DataFrame(data=np.NaN, index = index, columns = cols_ls))


def populate_sections_df(company_list, num_of_sections, scores_df, sections_df, questions_ls, max_results_ls):
    
    
    def calculate_section_result(scores_df, questions_ls, max_results_ls, company_name, section):
        
        '''
        Function that calculates the average score of a company over a given section.
        params: scores_df (dataframe, containing all scores columns, indexed on "Company_Name").
                company_name (string, name of the company to look for the index column in the df_score).
                section (int, number of the section for which we need to calculate the average).
                questions_ls (list, contains the numbers of the questions in a given section).
                max_results_ls (list of ints, every int corresponds to the maximum score obtainable in a given section).
        return: result_flt (float, average of all scores a company got at a given section).
        ''' 
        
        # Get the slice of the df_score that corresponds to the questions contained in a given section. 
        # Hard code the '1' as we will always want to start from the 1st question.
        # To get the number of the last question I calculate the length of the list of questions that corresponds to 
        # that section. Note that to get to the section we want we will subtrcat 1, as the lists where all questions numbers are 
        # stored are 0-indexed.
        
        ls = (scores_df.loc \
              [company_name] \
              ["Score_{}_1".format(section):"Score_{}_{}".format(section, len(questions_ls[section-1]))]
             ).values[:]

        # Calculate the average as a float.
        section_result_flt = (pd.to_numeric(ls).sum())/max_results_ls[section-1]

        return (section_result_flt)

    '''
    Function that creates a df for the sections results.
    params: company_list (list of strings, contains all the names of the companies).
            num_of_sections (int, represents the total number of sections in the analysis).
            scores_df (dataframe, containing all scores columns, indexed on "Company_Name").
            sections_df (dataframe, should be passed with NaN, indexed on "Company_Name").
            questions_ls
    return: sections_df (dataframe, populated with the sections averages. In the "Company_Name" columns there should also be 
                         a new row called "Averages", and after the last section "Section_10" there should be a new column 
                         called "TRAC_Index", it is indexed on "Company_Name").
    ''' 
    
    # For every one of the company in the sample.
    for company in company_list:
        
        # For every one of the section. Note that we add 1 because range stops 1 number before its second argument. 
        for section_num in range(1,num_of_sections + 1): 
            
             # Populate the sections_df with the results of the calculate_section_results function.
            sections_df.at[company,'Section_{}'.format(section_num)]\
            = round((calculate_section_result(scores_df, questions_ls,\
                                              max_results_ls, company_name = company, section = section_num)), 2)
            
            # Populate the average line with the average of every section
            sections_df.at["Averages", "Section_{}".format(section_num)] \
            = round(sections_df["Section_{}".format(section_num)].mean(), 2)
            
        #Calculate the average of every company and store it the "TRAC_Index" column
        sections_df.at[company, "TRAC_Index"] = round(sections_df.loc[company].mean(), 2)
        
    # Add the average of the "TRAC_Index"column.   
    sections_df.at["Averages", "TRAC_Index"] = round(sections_df["TRAC_Index"].mean(), 2)
    
    return (sections_df)


def assign_bands (sections_df, bands_dict):
    
    '''
    Function that assign bands to the results the companies obtained. 
            sections_df (dataframe, should be the return value of the populate_sections_df() function).
    return: sections_df (dataframe, populated with a new column "Bands" and the corresponding assigned band).
    '''
    
    # For every one of the company in the sample.
    for company in sections_df.index:
            
        # Handles 0.00 exeption, as it will not be true that 0.00 > 0. 
        if sections_df.at[company, "TRAC_Index"] == 0:
            sections_df.loc[company, "Bands"] = list(bands_dict.values())[0]
            
        # Loop backwards from the highest possible band.
        for index in reversed((range(0,5))): 

            # If score is between lower bound (included) and the upper bound (excluded) attribute corresponding band.
            if  (
                sections_df.at[company, "TRAC_Index"] < list(bands_dict.keys())[index] and
                sections_df.at[company, "TRAC_Index"] >= list(bands_dict.keys())[index-1]
                ):
                
                sections_df.loc[company, "Bands"] = list(bands_dict.values())[index-1]
                
    return (sections_df)


def create_folders_structure (root, sub_folders_names, companies_ls):
   
    '''
    Function that creates folders structures to store the outputs of app.py.
    
    params: root (string type, name of the root folder).
            sub_folders_names (string type, name of the sub folder).
            companies_ls (list of strings, containing all names of all companies to create one folder each).
    return: None 
    '''
    
    # Create the root folder using pathlib.
    root_path = pathlib.Path(root)
    root_path.mkdir(parents=True, exist_ok=True)

    # Create the sub folders.  
    for sub_folder in sub_folders_names:
        sub_folder_path = pathlib.Path(root + "/" + sub_folder)
        sub_folder_path.mkdir(parents=True, exist_ok=True)
        
    # Create a folder per company in the second sub folder. 
    for company in companies_ls: 
        sub_company_folder_path = pathlib.Path(root + "/" + sub_folders_names[1] + "/" + company)
        sub_company_folder_path.mkdir(parents=True, exist_ok=True)
        
    return None


def store_file (root, file, file_name, destination_path):
    
    '''
    Function that saves the file it is given in the correponding folder in the folder structure create in 
    create_folders_structure(). 
    params: file (could be either a pandas df or a matplotlib figure)
            file_name (string, name to write as name of the file)
            destination_path (string, used to locate the folder where to store the file)
    retunr: None 
    ''' 
    
    if isinstance(file, pd.DataFrame) == True:
        file.to_csv(root + "/" + destination_path + "/" + file_name + ".csv")
    if isinstance(file, plt.Figure) == True:
        file.savefig(root + "/" + destination_path + "/" + file_name + ".png", bbox_inches='tight', dpi = 300)
        
    return None