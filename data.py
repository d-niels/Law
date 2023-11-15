
import csv
import os
import random

GENDERS = ['Male', 'Female']
ETHNICITIES = ['White', 'Black', 'Latino', 'Chinese', 'Indian']
JOB_TITLES = ['Software-Engineer', 'Data-Scientist', 'Machine-Learning-Engineer']

gender_idx = {'Male': 0, 'Female': 1}

def job_skills(job_title):
    path = f'job_descriptions/{job_title}.txt'
    skills = []
    with open(path, 'r') as f:
        skills = f.read().split(',')
        
    random.shuffle(skills)

    return skills
    

def random_name(ethnicity, gender):
    path = f'names/{ethnicity}.csv'
    first_names = []
    last_names = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            first_names.append(row[gender_idx[gender]])
            last_names.append(row[-1])

        first_name = random.sample(first_names, 1)[0]
        last_name = random.sample(last_names, 1)[0]

        return first_name + ' ' + last_name

def random_city(ethnicity):
    path = f'cities/{ethnicity}.csv'
    cities = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            cities.append(row[0] + ', ' + row[1])

    city = random.sample(cities, 1)[0]
    return city

def get_prompts(job_title):
    path = f'prompts/{job_title}/'
    prompts = []
    for file in sorted(os.listdir(path)):
        with open(path+file, 'r') as f:
            prompts.append(f.read())

    return prompts
