#############################
### FUNCTIONS DEFINITIONS ###
#############################

# Imports

import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from constants import *
from utils import *


def create_and_store_df_for_spidercharts(sections_df, sectors_df, sub_folders_names, new_cols_dict, root):
        
    '''
    Function that creates and saves a dictionary of dataframes. Every df has a row with the sections scores for the company, 
    a row with the sections scores of the sector the company belongs to and a row with the sections scores of all companies. 
    
    params: sections_df (dataframe, containing all results per section, indexed on "Company_Name").
            sectors_df (dataframe, containing all results per section grouped by sector, indexed on "Company_Name").
            sub_folders_names (list of strings, contains the names of the sub folders).
    return: None. 
    '''
    
    # Empty dictionary. 
    df_for_spidercharts_dict = {}
   
    # For every company:
    for company in list(sections_df.index[:-1]): # Exclude "Averages"
        
        # Get its row from the sections_df 
        sr_1 = sections_df.loc[company]
        
        # Replace empty cells with None.
        sr_1.where((pd.notnull(sr_1)), None)
        
        # Turn sr_1 into a df_1 and exclude the "Trac_Index" and "Company_Sector" columns. 
        df_1 = sr_1.to_frame().transpose()
        df_1 = df_1[df_1.columns[0:10]]
        
        # Get the row from the sectors_df corresponding to the sector of the company we have extracted results in df_1.
        sr_2 = sectors_df.loc[sections_df.loc[company, "Company_Sector"]]
        
        # Get the row from the sections_df corresponding to the all companies average results per section.
        sr_3 = sections_df.loc["Averages"][0:10]

        # Join sector and all results into a df_2.
        df_2 = sr_2.to_frame().join(sr_3.to_frame()).transpose()

        # Join df_2 and df_1.
        df_3 = df_1.append(df_2)
        
        # Reset index and rename the previous index column to "groups".
        my_df = df_3.reset_index().rename(index = int, columns = {"index": "groups"})

        # Rename the columns using the Italian names of the sections shortened (see constant SECTIONS_SHORT_NAMES in 
        # constants.py). 
        # Rename row containing sector English name and "Averages" to Italian. 
        my_df.rename(new_cols_dict, axis = 'columns', inplace = True)
        my_df.at[1,"groups"] = "Medie Settore ({})".format(my_df.at[1,"groups"])
        my_df.at[2,"groups"] = "Medie Globali"

        # Add N/A to the new section name if the section result is None and replace None with 0.01 (we still need an int here
        # for the spiderchart to create a star-like effect connecting the dots of every section restult with a line).
        for i in my_df.columns[1:]:
            if my_df.at[0, i] == None:
                new_name = i + '\n' + "(N/A)"
                my_df.rename({i : new_name}, axis = 'columns', inplace = True)
                my_df.at[0, new_name] = 0.01 
                
        df_for_spidercharts_dict[company] = my_df
    
    # Save the df in the folder of the compay. 
    for key, value in df_for_spidercharts_dict.items():
        destination_path = sub_folders_names[1] + "/" + key 
        store_file(root, file = value, file_name = key + "_spiderchart_data", destination_path = destination_path)
        
    return (df_for_spidercharts_dict)


def make_and_save_spidercharts(df_for_spidercharts_dict, root, sub_folders_names):
    
    '''
    Function that creates and saves three spidercharts per company. 1) with the scores of the company plotted, 2) with the 
    scores of the company plotted against the averages of the sector 3) with the scores of the companies plotted against the 
    averages of all the sample. In case the company has section with None because it was deactivated, then the label of the 
    section includes an (N/A).

    In the body of this function we will define 4 auxiliary functions:
    calculate_radiants_for_spiderchart(), to calculate the angles in radiants for the 10 sections we want the polar chart to be 
                                          divided into. 
    plot_empty_spiderchart(), to create the empty spiderchart that we will use as argument for do_charts() to fill it with 
                              data.
    do_charts(), filling the empty spiderchart with the dataframe of the company we are plotting. 
        
    credits: https://python-graph-gallery.com/391-radar-chart-with-several-individuals/ 
    params: df_for_spidercharts_dict (dictionary of dfs, contains all dfs, one per company).
    return: None. 
    '''
         
    def calculate_radiants_for_spiderchart(my_df):
    
        '''
        I will need to create this function inside make_and_save_spidercharts() before being able to call it in 
        plot_empty_spiderchart(). 

        We need to find the αrad of each angle to create the spider chart. 
        We will apply the following proportion ==> αrad : α° = 2π : 360° ==> αrad = (α° * 2π)/360° 
        I have 10 points on the circle whose arcs subtend angles each distant from one other exactly 36°. 
        αrad of the first arc = (36° * 2π)/360° = (1 * 2π)/10° 
        36*2*pi/360 == 1/N*2*pi == 1/len(categories)*2*pi  # True

        params: my_df (dataframe, we will need to pass to this function the df from the df_for_spidercharts_dict).
        return: my_angles (list of floats, every float is the angle in radiant if we want to divide the plot in N number of 
        sections. 
        '''
 
        my_N =len(list(my_df)[1:])
        my_angles = [(n * 2 * pi) / my_N for n in range(my_N)] 
        my_angles += my_angles[:1] 

        return(my_angles)

    
    def plot_empty_spiderchart(my_df, my_ax, groups, label, color):
        
        '''
        I will need to create this function inside make_and_save_spidercharts function before being able to call it in 
        do_charts(). 

        params: my_df (dataframe, we will need to pass to this function the df from the df_for_spidercharts_dict).
                my_ax (matplotlib axis)
                groups (int, index of the row we will be slicing from my_df)
                label (string, name of the label to put in legend)
                color (string, color of the line)
        return: my_angles (list of floats, every float is the angle in radiant if we want to divide the plot in N number of 
        sections. 
        '''
        
        # Get angles
        my_angles = calculate_radiants_for_spiderchart(my_df)
        
        # Get list of labels to use for the sections short names in Italian, skip cloumn "groups". 
        my_categories = list(my_df)[1:]
        
        # Set the first axis to be on top and rotate clock-wise.
        my_ax.set_theta_offset(pi / 2)
        my_ax.set_theta_direction(-1)

        # Draw one line per variable + add labels.
        plt.xticks(my_angles[:-1], my_categories, fontsize = 11, color = "black", horizontalalignment = "center")

        # Draw ylabels.
        my_ax.set_rlabel_position(1)
        plt.yticks([0.25,0.50,0.75], ["25%","50%","75%"], color = "grey", size = 10)
        plt.ylim(0,1)
        values = my_df.loc[groups].drop('groups').values.flatten().tolist()
        values += values[:1]
        my_ax.plot(my_angles, values, linewidth = 1, linestyle = 'solid', label = "{}".format(label))
        my_ax.fill(my_angles, values, '{}'.format(color), alpha = 0.1)
        
        return(my_ax)
    
    
    def do_charts(my_df, company_label, sector_label, all_companies_label, root, company_only = True, 
                  to_sector_only = False, to_all = False):
        
        '''
        I will need to create this function inside make_and_save_spidercharts() before being able to call it in 
        make_and_save_spidercharts().

        params: my_df (dataframe, we will need to pass to this function the df from the df_for_spidercharts_dict).
                company_label (string, name of the company to add as label)
                sector_label (string, name of the sector to add as label)
                all_companies_label (string, label to indicate that the results come from an average of all companies)
                company_only (bool, set to True to start doing the chart for the company only, will be set to False after 
                              code inside the if statement has run).
                to_sector_only(bool, set to False, will change to True after company_only is will be set to False). 
                to_all (bool, set to False, will change to True after to_sector_only is will be set to False).
                
        return: my_angles (list of floats, every float is the angle in radiant if we want to divide the plot in N number of 
        sections.
        '''

        # Loop will always starts here by construction.
        if company_only == True:
            
            # Initialise new spiderchart. 
            my_company_fig = plt.figure()
            my_company_ax = my_company_fig.add_subplot(111,  polar = True)

            # do spiderchart with one indicator only, the company scores.
            plot_empty_spiderchart(my_df, my_ax  = my_company_ax, groups = 0, label = company_label, color = "b", )

            # Add legend and save file in file structre under the `company_profiles/company_name` folder.
            plt.legend(loc='upper right', bbox_to_anchor=(0.01, 0.01))
            destination_path = sub_folders_names[1] + "/" + company_label 
            store_file(root, 
                       file = my_company_fig, 
                       file_name = "{}_spiderchart".format(company_label), 
                       destination_path=destination_path)
            
            plt.close()

            # Change values of argument all_sector to True for next loop to activate.
            to_sector_only = True
            company_only = False

        if to_sector_only == True:
            
            # Initialise new spiderchart. 
            my_sector_fig = plt.figure()
            my_sector_ax = my_sector_fig.add_subplot(111,  polar=True)

            # do spiderchart with two indicators, the company scores and the averages of the sector.
            plot_empty_spiderchart(my_df, my_ax  = my_sector_ax, groups=0, label=company_label, color="b")
            plot_empty_spiderchart(my_df, my_ax  = my_sector_ax, groups=1, label=sector_label, color="r")

            # Add legend and save file in file structre under the `company_profiles/company_name` folder.
            plt.legend(loc = 'upper right', bbox_to_anchor = (0.01, 0.01))
            destination_path = sub_folders_names[1] + "/" + company_label
            store_file(root, 
                       file = my_sector_fig, 
                       file_name = "{}_{}_spiderchart".format(company_label, sector_label[15:-1]), 
                       destination_path = sub_folders_names[1] + "/" + company_label)
            
            plt.close()
            
            # Change values of argument all_sector to True for next loop to activate.
            to_sector_only = False
            to_all = True

        if to_all == True:
            
            # Initialise new spiderchart. 
            my_all_fig = plt.figure()
            my_all_ax = my_all_fig.add_subplot(111,  polar=True)

            # do spiderchart with two indicators, the company scores and the global averages.
            plot_empty_spiderchart(my_df, my_ax = my_all_ax, groups=0, label = company_label, color = "b")
            plot_empty_spiderchart(my_df, my_ax = my_all_ax, groups=2, label = all_companies_label, color = "r")

            # Add legend and save file in file structre under the `company_profiles/company_name` folder.
            plt.legend(loc = 'upper right', bbox_to_anchor = (0.01, 0.01))
            destination_path = sub_folders_names[1]+ "/" + company_label
            store_file(root, 
                       file = my_all_fig, 
                       file_name = "{}_{}_spiderchart".format(company_label, all_companies_label), 
                       destination_path = sub_folders_names[1] + "/" + company_label)
            
            # reset to_all back to False. 
            to_all = False 
            
            plt.close()
            
        return None
        
    # START `make_and_save_spidercharts()` definition
    
    for key, value in df_for_spidercharts_dict.items():
        
        # for ease of reading I create clearer variable names
        spiderchart_df = value

        # Get labels for the spiderchart from the spiderchart df (under the "groups" column)
        company_label = key # We are iterating over a dictionary whose key is the name of the company
        sector_label = spiderchart_df.at[1, "groups"]
        all_companies_label = spiderchart_df.at[2, "groups"]

        # Do charts 
        do_charts(my_df = spiderchart_df,
                  company_label = company_label, 
                  sector_label = sector_label, 
                  all_companies_label = all_companies_label,
                  root = root)
        
    return None

    # END `make_and_save_spidercharts()` definition
