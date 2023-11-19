import openai
import argparse
import os
import re
import time
from key import key

openai.api_key = key

parser = argparse.ArgumentParser(description="Script to evaluate resumes.")

# Add the 'job_title' argument
parser.add_argument('-j', '--job_title', type=str, help='Specify the job title')
# Parse the command line arguments
args = parser.parse_args()
# Access the value of the 'job_title' argument
job_title = args.job_title


class Evaluator:
    def __init__(self, prompt_file):
        with open(prompt_file, 'r') as f:
            self.action_prompt = f.read()
            self.action_prompt = self.action_prompt.replace('\n', ' ')

    def evaluate(self, job_description, resume):
        context_prompt = f'Job Description:\n{job_description}\n\nCandidate Resume:\n{resume}'
        done = False
        while not done:
            try:
                completion = openai.ChatCompletion.create(
                  model="gpt-3.5-turbo",
                  messages=[
                    {"role": "system", "content": context_prompt},
                    {"role": "user", "content": self.action_prompt}
                  ]
                )
                done = True
            except:
                time.sleep(1)
        response = completion.choices[0].message['content']
        # print(response)
        score, bullet_points = self.clean_response(response)
        return score, bullet_points

    @staticmethod
    def clean_response(response):
        bullet_points = []
        for line in response.split('\n'):
            if line and line[0] == '-':
                bullet_points.append(line.replace('- ', ''))
        match = re.search(r'(\d+)/10', response)
        if match:
            score = int(match[0][0])
        else:
            score = None
        if len(bullet_points) == 0:
            bullet_points = None
        return score, bullet_points


with open('job_descriptions/' + job_title + '.txt', 'r') as f:
    job_description = f.read()
    job_description = job_description.replace('\n', ' ')
ethnicities = ['Black', 'Indian', 'Chinese', 'Latino', 'White']
sexes = ['Male', 'Female']
evaluator = Evaluator('prompts/evaluator.txt')

for ethnicity in ethnicities:
    for sex in sexes:
        resume_folder_path = os.path.join('resumes', job_title, ethnicity, sex)
        evaluator_folder_path = os.path.join('evaluations', job_title, ethnicity, sex)
        for file in os.listdir(resume_folder_path):
            if file not in os.listdir(os.path.join('evaluations', job_title, ethnicity, sex)):
                start = time.time()
                with open(os.path.join(resume_folder_path, file), 'r') as f:
                    resume = f.read()
                score, bullet_points = evaluator.evaluate(job_description, resume)
                if score:
                    string_to_write = str(score)
                    if bullet_points:
                        for bullet_point in bullet_points:
                            string_to_write += '\n' + bullet_point
                else:
                    string_to_write = 'Invalid Prompt Format'
                with open(os.path.join(evaluator_folder_path, file), 'w') as f:
                    f.write(string_to_write)
                print(f'time: {int(time.time() - start)}s, evaluated: {os.path.join(evaluator_folder_path, file)}')
