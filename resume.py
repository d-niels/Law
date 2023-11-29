import os
import random
import data
import re
import openai
import time
from key import key
import argparse

openai.api_key = key

def save_random_resume(job_title):
    gender = random.sample(data.GENDERS, 1)[0]
    ethnicity = random.sample(data.ETHNICITIES, 1)[0]
    name = data.random_name(ethnicity, gender)
    t = time.time()
    r = generate_resume(name, gender, ethnicity, job_title)
    t = time.time() - t
    path = '/'.join(['resumes', job_title, ethnicity, gender])
    path += '/'+name+'.txt'
    with open(path, 'w') as f:
        f.write(r)

    print(f'{round(t, 4)}s  Saved {path}')
        

def generate_resume(name, gender, ethnicity, job_title, temp=1.0):
    city = data.random_city(ethnicity)
    prompts = data.get_prompts(job_title)
    skills = data.job_skills(job_title)
    skills1 = ', '.join(skills[:len(skills)//2])
    skills2 = ', '.join(skills[len(skills)//2:])

    for i, p in enumerate(prompts):
        new_p = re.sub('\[name\]', name, p)
        new_p = re.sub('\[gender\]', gender.lower(), new_p)
        new_p = re.sub('\[ethnicity\]', ethnicity.lower(), new_p)
        new_p = re.sub('\[location\]', city, new_p)
        new_p = re.sub('\[skills1\]', skills1, new_p)
        new_p = re.sub('\[skills2\]', skills2, new_p)
        prompts[i] = new_p

    messages = []

    for prompt in prompts:
        messages.append({
            'role': 'user',
            'content': prompt
        })

        # Prompt the model
        done = False
        while not done:
            try:
                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages = messages,
                    temperature = temp
                )
                done = True
            except:
                time.sleep(1)

        messages.append({
            'role': 'system',
            'content': response['choices'][0]['message']['content']
        })

    return response['choices'][0]['message']['content']
