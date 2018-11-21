# Transparency International Italia 
## Transparency in Corporate Reporting
### Background 

Transparency International (TI) is one of the pioneers in the fight for a more transparent corporate reporting. Being the leader of anti-corruption standards in the world, the Business Inegrity team of TI created what are now known in the compliance industry the [Business Principles for Countering Bribery (BPCB)](https://www.transparency.org/whatwedo/publication/business_principles_for_countering_bribery) and its [Commentary](https://www.transparency.org/files/content/publication/2015_BusinessPrinciplesCommentary_EN.pdf) which act as a go to resource for multinationals designing their anti-corruption programmes. 

Based on the best practices laid down in the BPCP, the Business Integrity team developed a questionnaire to assess the level of adherence of multinationals to the BPCB, giving birth to the [Transparency in Corporate Reporting (TRAC)](https://www.transparency.org/files/content/feature/2016_TRACEMM_Index.png), a study which has already been conducted several times in [2009](https://www.transparency.org/whatwedo/publication/transparency_in_reporting_on_anti_corruption_a_report_on_corporate_practice), [2011](https://www.transparency.org/whatwedo/publication/promoting_revenue_transparency_2011_report_on_oil_and_gas_companies), [2012](https://www.transparency.org/news/feature/shining-a-light-on-the-worlds-biggest-companies), [2013](https://www.transparency.org/news/feature/emerging_market_multinational_companies_ready_for_prime_time), [2014](https://www.transparency.org/news/feature/global_companies_global_transparency), [2015](https://www.transparency.org/whatwedo/publication/transparency_in_corporate_reporting_assessing_the_worlds_largest_telecommun), and [2016](https://www.transparency.org/news/feature/emerging_markets_pathetic_transparency). 

This year, the Italian antenna created the first iteration of its TRAC, assessing the transparency and strength of anti-corruption programmes of 50 Italian Multinationals, whose final report can be downloaded here. 

## Methodology 
### Data collection

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
