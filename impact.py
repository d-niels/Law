import pandas as pd
import numpy as np
import data
import os


def extract_score(path):
    text = ''
    with open(path, 'r') as f:
        text = f.read()
        
    return float(text.split('\n')[0])


def get_resumes(evaluator, job_type):
    names = []
    races = []
    genders = []
    scores = []

    dir_name = 'evaluations/' + evaluator

    ethnicities = data.ETHNICITIES
    for race in ethnicities:
        sexes = data.GENDERS
        for gender in sexes:
            outputs = os.listdir(f'{dir_name}/{job_type}/{race}/{gender}')
            for output in outputs:
                try:
                    score = extract_score(f'{dir_name}/{job_type}/{race}/{gender}/{output}')
                except:
                    continue
                names.append(output[:4])
                races.append(race)
                genders.append(gender)
                scores.append(score)

    df = pd.DataFrame(data={'Name': names, 'Race': races, 'Gender': genders, 'Score': scores})
        
    return df


def calc_impact(df):
    df['selection_rate'] = df['num_selections'] / df['num_applicants']
    df['impact_ratio'] = df['selection_rate'] / df['selection_rate'].max()
    df[['selection_rate', 'impact_ratio']] = df[['selection_rate', 'impact_ratio']].round(2)
    return df


def impact(evaluator, job_title):
    df = get_resumes(evaluator, job_title)
    df['Selected'] = (df['Score'] > 7).astype(int)

    df_genders = df.groupby(['Gender']).agg(num_applicants=('Name', 'count'), num_selections=('Selected', 'sum'))
    df_gender_impact = calc_impact(df_genders)

    df_races = df.groupby(['Race']).agg(num_applicants=('Name', 'count'), num_selections=('Selected', 'sum'))
    df_race_impact = calc_impact(df_races)

    intersectional_df = df\
        .groupby(['Gender', 'Race'])['Selected']\
        .agg(['count', 'sum'])\
        .rename(columns={'count': 'num_applicants', 'sum': 'num_selections'})

    df_intersectional_impact = calc_impact(intersectional_df)

    dir = f'impacts/{evaluator}/{job_title}'
    os.makedirs(dir, exist_ok=True)
    df_gender_impact.to_excel(f'{dir}/gender-impact.xlsx')
    df_race_impact.to_excel(f'{dir}/race-impact.xlsx')
    df_intersectional_impact.to_excel(f'{dir}/intersectional-impact.xlsx')

    print('\n\n\nGENDER IMPACT\n')
    print(df_gender_impact.to_string())
    print('\n\n\nRACE IMPACT\n')
    print(df_race_impact.to_string())
    print('\n\n\nINTERSECTIONAL IMPACT\n')
    print(df_intersectional_impact.to_string())
    print('\n\n')