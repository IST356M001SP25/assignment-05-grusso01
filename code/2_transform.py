import pandas as pd
import streamlit as st
import pandaslib as pl

survey_data = pd.read_csv('cache/survey.csv')
states_data = pd.read_csv('cache/states.csv')

column_data = []
for year in survey_data['year'].unique():
    data = pd.read_csv(f'cache/col_{year}.csv')
    column_data.append(data)

col_data_combined = pd.concat(column_data, ignore_index=True)

survey_data['_country_clean'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)

merged_data_with_states = survey_data.merge(
    states_data, 
    left_on="If you're in the U.S., what state do you work in?", 
    right_on='State', 
    how='inner'
)

merged_data_with_states['_full_city'] = (
    merged_data_with_states['What city do you work in?'] + ', ' +
    merged_data_with_states['Abbreviation'] + ', ' +
    merged_data_with_states['_country_clean']
)

final_combined_data = merged_data_with_states.merge(
    col_data_combined, 
    left_on=['year', '_full_city'], 
    right_on=['year', 'City'], 
    how='inner'
)

final_combined_data["_annual_salary_cleaned"] = final_combined_data[
    "What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"
].apply(pl.clean_currency)

final_combined_data['_annual_salary_adjusted'] = final_combined_data.apply(
    lambda row: row["_annual_salary_cleaned"] * (100 / row['Cost of Living Index']),
    axis=1
)

final_combined_data.to_csv('cache/survey_dataset.csv', index=False)

salary_by_location_and_age = final_combined_data.pivot_table(
    index='_full_city', 
    columns='How old are you?', 
    values='_annual_salary_adjusted', 
    aggfunc='mean'
)
salary_by_location_and_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

salary_by_location_and_education = final_combined_data.pivot_table(
    index='_full_city', 
    columns='What is your highest level of education completed?', 
    values='_annual_salary_adjusted', 
    aggfunc='mean'
)
salary_by_location_and_education.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')

st.write(salary_by_location_and_education)