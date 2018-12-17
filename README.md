# Transparency International Italia 
## Transparency in Corporate Reporting (Italy) Index
### Background 

Transparency International (TI) is one of the pioneers in the fight for a more transparent corporate reporting. Being the leader of anti-corruption standards in the world, the Business Inegrity team of TI created what are now known in the compliance industry as the [Business Principles for Countering Bribery (BPCB)](https://www.transparency.org/whatwedo/publication/business_principles_for_countering_bribery) and its [Commentary](https://www.transparency.org/files/content/publication/2015_BusinessPrinciplesCommentary_EN.pdf) which act as a go to resource for multinationals designing their anti-corruption programmes. 

Based on the best practices laid down in the BPCP, the Business Integrity team developed a questionnaire to assess the level of adherence of multinationals to the BPCB, giving birth to the [Transparency in Corporate Reporting (TRAC) Index](https://www.transparency.org/files/content/feature/2016_TRACEMM_Index.png), a study which has already been conducted several times in [2009](https://www.transparency.org/whatwedo/publication/transparency_in_reporting_on_anti_corruption_a_report_on_corporate_practice), [2011](https://www.transparency.org/whatwedo/publication/promoting_revenue_transparency_2011_report_on_oil_and_gas_companies), [2012](https://www.transparency.org/news/feature/shining-a-light-on-the-worlds-biggest-companies), [2013](https://www.transparency.org/news/feature/emerging_market_multinational_companies_ready_for_prime_time), [2014](https://www.transparency.org/news/feature/global_companies_global_transparency), [2015](https://www.transparency.org/whatwedo/publication/transparency_in_corporate_reporting_assessing_the_worlds_largest_telecommun), and [2016](https://www.transparency.org/news/feature/emerging_markets_pathetic_transparency). 

This year, the [Italian branch of TI](https://www.transparency.it/) carried out the second iteration of its TRAC, assessing the transparency and strength of anti-corruption programmes of 50 Italian Multinationals, whose final report can be downloaded here across 61 questions, divided in 10 sections:
1. Public Committment against Corruption (5 questions)
2. Anti-Corruption Programme (9 questions)
3. Code of Conduct (10 questions)
4. Whistleblowing (10 questions)
5. Lobbying (6 questions)
6. Conflict of Interests (6 questions)
7. Political Contribution (4 questions)
8. Organisational Transparency (5 questions)
9. Anti-corruption training (8 questions)
10. Sustainble Projects Transparency (4 questions)

## The Data 
### Data collection 

The data was collected in a Google Spreadsheet. Every row represented one company which was assessed across 61 questions, divided in the aforementioned 10 sections. In order to assess the questions, it was necessary to look for the information in several document types, such as:
* Annual Reports, 
* Sustainbility Reports, 
* 231 Model (exists only in Italy, coming from the administrative order 231), 
* Anti Corruption Programme Documents, 
* Code of Ethics, 

To speed up the search, we used the google search engine capabilities, which allows to search file types and key words in the same web domain: 
* `in: URL filetype:pdf keyword` would search for keywork in all PDF files in the URL domain. 
* `in: URL keyword`would search for keyword in the whole URL domain. 

So a typical seach would be `in: https://www.brembo.com/ filetype:pdf bribery` that would give me all the links to the pdfs in the website of the company `Brembo` containing the word `bribery`.

In the methodology of Transparency International Italia, the TRAC Index is the average of the results of the 10 sections. Each section has a different number of questions (see list above) and the section result is the weighted average of the questions scores obtained. 

### Database structure

We created a Google spreadsheet of 51x244. Each one of the 61 questions could be graded in one of the three following scales:
* 0-1,
* 0-1-2,
* 0-1-2-3. 

For every question, we created 5 columns 
* Score: integer type. 
* Source: string type indicating the type of document the information was found in (Annual Report etc.)
* URL: string type indicating the URL of the Source. 
* Comment: string type explaining why the company had obtained the given score. 
* Space: Empty column to allow for grouping and minimizing columns in Google Spreadsheet. 

The way the column names were given in the Google Spreadsheet is this:
`ColumnName_SectionNumber_QuestionNumber` example: `Score_1_3` would be the Score of the 3rd question of Section 1. 

### Data Extraction, Transformation and Loading (ETL) Pipeline. 

The objective of this pipeline is to:

1) Extract the raw data from the orignal Google Spreadsheet and create a raw data and a scores only Pandas dataframes. 
2) Use the scores only dataframe to calculate the results of every section, and create a sections results Pandas dataframe. 
3) Use the sections results dataframe to group the companies by sector, recalculate the sections results by group, and 
   store these results in a Pandas sectors dataframe. 
4) Use the strings in raw data from the Google Spreadsheet to create a `company_name.docx` for every one of the companies,   
   collating together all information stores in the columns Score, Source, URL and Comment to create a company profile. 
5) Create 3 spidercharts for every company, one plotting the sections results of the company only, one plotting the sections
   results of the company with the averages results of sections in the sector of the company, and one plotting the company 
   sections results with the averages results of the sections of all companies in the sample. 
6) Create a folder strucutre where to store the dataframes as `.csv` and the company profiles as `.docx` and the visulations as `.png.` 
   
### Deliverables 
The deliverables for this project are: 
1) A reproducible ETL pipeline 
2) 50 Company Profiles 
3) 50x3 Spidercharts 

Moreover, deliverable 2 and 3 should be saved in a folder structure decided by the client. 
```
.
├── company_profiles
│   ├── Abb Italia
│   ├── A.C. Milan S.p.A.
│   ├── Ali
│   ├── Armani
│   ├── Ast
│   ├── Barilla Holding
│   ├── Brembo
│   ├── Calzedonia
│   ├── Cassa Depositi e Prestiti
│   ├── Costa crociere
│   ├── Danieli & C.
│   ├── Edison
│   ├── Enel
│   ├── Eni
│   ├── Falk
│   ├── Fastweb
│   ├── Ferrari
│   ├── Ferrero
│   ├── Ferrovie dello Stato
│   ├── GE Italia Holding
│   ├── Generali
│   ├── Gruppo Cremonini
│   ├── Gruppo GSE
│   ├── Inter
│   ├── Intesa San Paolo
│   ├── Juventus 
│   ├── Leonardo
│   ├── Luxotica
│   ├── Magneti Marelli
│   ├── Mediaset
│   ├── MSC
│   ├── Napoli
│   ├── OTB
│   ├── Parmalat
│   ├── Pirelli
│   ├── Poste Italiane
│   ├── Prada
│   ├── RAI
│   ├── Rina
│   ├── Roma
│   ├── Saes
│   ├── Snam
│   ├── Terna
│   ├── Tim
│   ├── Tiscali
│   ├── UBI Banca
│   ├── Unicredit
│   ├── Veronesi Holdings SPA
│   ├── Vodafone
│   └── Wind Tre
└── data
    ├── raw_data_test.csv
    ├── scores_data_test.csv
    ├── sections_results_data_test.csv
    └── sectors_results_data_test.csv
```

When clicking on one of the companies folder, then we would find 4 files:

```
.
├── company_profiles
│   ├── Abb Italia
│   │   ├── Abb Italia_analisi.docx
│   │   ├── Abb Italia_Meccanica_spiderchart.png
│   │   ├── Abb Italia_Medie Globali_spiderchart.png
│   │   ├── Abb Italia_spiderchart_data.csv
│   │   └── Abb Italia_spiderchart.png
```

See below an example of three spidercharts that the pipeline would create.
<p align="middle">
  <img src="https://github.com/gsime1/Transparency_International_ETL_Pipeline/blob/master/deliverables/company_profiles/Brembo/Brembo_spiderchart.png" width="250" />
   <img src="https://github.com/gsime1/Transparency_International_ETL_Pipeline/blob/master/deliverables/company_profiles/Brembo/Brembo_Medie%20Globali_spiderchart.png" width="270" />
   <img src="https://github.com/gsime1/Transparency_International_ETL_Pipeline/blob/master/deliverables/company_profiles/Brembo/Brembo_Meccanica_spiderchart.png" width="300" />
</p>

It's important to notice that there was an edge-case to be handled in the creation of the spiderchart, when a company had been attributed an "N/A" to a certain section (say, lobbying) because they openly said to refrain from any such activities. In this case we had to artificially attribute to every  `None` in Python a 0.01 and deactivating the label by adding NA, "Lobbying (NA)". 

Here you can download an example of a company profile in `.docx`. Why not directly pdf? Because the client might want to tweak the language. 

### Software set-up 

The user of this pipeline will use Windows, so below the instructions on how to download Python and set up the environment needed to run `app.py`. 
<details open>
<summary> 1) Download Python, pip, virtualenv and virtualenvwrapper-win: </summary>
<br>
<ul>
   <li> Go to the <a href="https://www.python.org/downloads/windows/">Python releases for Windows</a>. </li>
   <li> CTRL+F "Python 3.6.5 - 2018-03-28".</li>
      <ul>
         <li> If you don't know if your Windows is a 32 or 64 bits:</li>
         <li> Open the Terminal Window by typing in the bottom-left bar "Terminal"; </li>
         <li> Type in the terminal the following command: <code>echo %PROCESSOR_ARCHITECTURE%</code> and you will know if it is 32 or 64.</li>
     </ul>
  <li> Click on the link "Windows x86-WHAT_BITS_YOU_HAVE executable installer"</li>
  <li> At the end of the download the installation window pops up: </li>
      <ul>
          <li> Tick the box "Add Python 3.6 to PATH"; (Adding Python to the PATH will allow you to call if from the Terminal.)</li>
          <li> OPTIONAL: to be sure you could check the we added Python to the computer's PATH by following <a href="https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/"> these instructions </a>.</li>
          <li> Click on "Customize installation"; </li>
          <li> Make sure the box "Install pip" is ticked;</li>
          <li> Click "Next";</li>
          <li> Tick "Add Python to environment variables".</li>
      </ul>
  <li> Install VirtualEnv:</li>
     <ul>
        <li> Open the Terminal window;</li>
        <li> Type <samp>pip install virtualenv<samp>.</li>
    </ul>
  <li> Install virtualenvwrapper-win:</li>
     <ul>
        <li> Always on the Terminal window type <code>pip install virtualenvwrapper-win</code></li>
     </ul>
PS: We decided not to use Miniconda as the <a href="https://anaconda.org/conda-forge/df2gspread"> Conda forge channel </a>, somehow downloads an old version of the <a href="https://github.com/maybelinot/df2gspread"> df2gspread </a>) library giving you errors at run time. 
</details>

2) Download Git for Windows. 
* Go to [`Git for Windows`](https://gitforwindows.org/) and Download it (keep clicking on "Next" without changing the options and boxes ticked for you). 

3) Download this repository on your PC. 
* From the Terminal window type `git clone https://github.com/gsime1/Transparency_International_ETL_Pipeline` 
* From the Windows search box search "Transparency_International_ETL_Pipeline", right-click and select "copy path". 
* From the Terminal window type `cd`, then right clck and paste the path to the "Transparency_International_ETL_Pipeline" folder on your computer. 
* the prompter sign `>` of the command line should now contain `Transparency_International_ETL_Pipeline` which means you are inside the folder from the terminal (`cd` actually means, change directory, whereby we mean go to this folder whose path I gave you). 

4) Create environment using virtualenv + `requirements.txt`
Before downloading all needed dependencies, we will need you to download [Visual Studio 2015 Community Edition (or any later version, when these are released)](https://visualstudio.microsoft.com/de/downloads/?rr=https%3A%2F%2Fpackaging.python.org%2F). 
* From the command line type `virtualenv trac2018` *(trac2018 is the name I chose, you can give your environment any name you wish)*
* Activate your environment by typing in the command line `.\trac2018\Scripts\activate` *(if you gave your virtual environment another name make sure you're changing the in between `.\whaevertyoucalledtheenvironment\Scripts\activate`.*
* Install all necessary packages typing `pip install -r requirements.txt`. This might take few minutes.
* Should you get any error related to the `pycrypto` library, follow [these wonderful instructions](https://github.com/sfbahr/PyCrypto-Wheels).  

5) Working with the Google API 
* Activate Google API by following step by step the instructions of [this link](https://socraticowl.com/post/integrate-google-sheets-and-jupyter-notebooks/), stop at the end of Part 1. 
* Make sure to save your client ID and Service Account Credentials files in the same folder of the project cloned from GitHub, `Transparency_International_ETL_PipelineTransparency_International_ETL_Pipeline`. 

6) Change the name of key.json in `constants.py`
* Now open the `constant.py` file, if you don't have any programme that reads `.py` extensions (like [`Sublime Text`](https://fileinfo.com/software/jon_skinner/sublime_text), you can also just use the good old [`Microsoft Notepad`](https://fileinfo.com/software/microsoft/notepad). 
* Change the content of the variable KEY, `KEY = "jupyter-meets-gsheet-f71096c7c7b8.json"` inserting in the double quotes the name you gave to your Service Account Credentials JSON file. 
* Save and close `contstants.py`. 

7) From the Terminal run `Python app.py`

## Reusability
Now it's 2019 and you want to do a new iteration of this study. 

### How to change/add data
### How to replicate the study with new data
