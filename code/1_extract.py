import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
#TODO Write your extraction code here

states_url = 'https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv'
states_data = pd.read_csv(states_url)
states_data.to_csv('cache/states.csv', index=False)

survey_url = 'https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv'
survey_data = pd.read_csv(survey_url)
survey_data['year'] = survey_data['Timestamp'].apply(pl.extract_year_mdy)
survey_data.to_csv('cache/survey.csv', index=False)

unique_years = survey_data['year'].unique()

for year in unique_years:
    col_url = (f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")
    
    col_data = pd.read_html(col_url)[1] 
    col_data['year'] = year
    col_data.to_csv(f'cache/col_{year}.csv', index=False)