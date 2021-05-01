import requests
import csv
import pandas as pd
import pymongo
import json
import sys, getopt, pprint
from pymongo import MongoClient
from collections import Counter


print("mjao")
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
response = requests.get(url, allow_redirects=True)

with open('owid-covid-data.csv', 'w') as f:
   writer = csv.writer(f)
   for line in response.iter_lines():
       writer.writerow(line.decode('utf-8').split(','))

      
csvfile = open('owid-covid-data.csv', 'r')
reader = csv.DictReader( csvfile )
mongo_client=MongoClient() 
db=mongo_client.covid_table
db.segment.drop()
header= [ "iso_code", "continent", "location", "date", "total_cases", "new_cases", "new_cases_smoothed", "total_deaths", "new_deaths", "new_deaths_smoothed", "total_cases_per_million", "new_cases_per_million", "new_cases_smoothed_per_million", "total_deaths_per_million", "new_deaths_per_million", "new_deaths_smoothed_per_million", "reproduction_rate", "icu_patients", "icu_patients_per_million", "hosp_patients", "hosp_patients_per_million", "weekly_icu_admissions", "weekly_icu_admissions_per_million", "weekly_hosp_admissions", "weekly_hosp_admissions_per_million", "new_tests", "total_tests", "total_tests_per_thousand", "new_tests_per_thousand", "new_tests_smoothed", "new_tests_smoothed_per_thousand", "positive_rate", "tests_per_case", "tests_units", "total_vaccinations", "people_vaccinated", "people_fully_vaccinated", "new_vaccinations", "new_vaccinations_smoothed", "total_vaccinations_per_hundred", "people_vaccinated_per_hundred", "people_fully_vaccinated_per_hundred", "new_vaccinations_smoothed_per_million", "stringency_index", "population", "population_density", "median_age", "aged_65_older", "aged_70_older", "gdp_per_capita", "extreme_poverty", "cardiovasc_death_rate", "diabetes_prevalence", "female_smokers", "male_smokers", "handwashing_facilities", "hospital_beds_per_thousand", "life_expectancy", "human_development_index"]

for each in reader:
    row={}
    for field in header:
        row[field]=each[field]

    db.segment.insert(row)

answer = db.segment.distinct('location') 

print(len(answer))
