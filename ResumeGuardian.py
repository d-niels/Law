from pprint import pprint
import inquirer
from resume import save_random_resume
import evaluator
import impact
import os


def get_response(message, choices):
    questions = [
    inquirer.List(
            'answer',
            message=message,
            choices=choices,
        ),
    ]

    return inquirer.prompt(questions)['answer']

actions = ['Generate Resumes', 'Evaluate Resumes', 'Evaluate Scores', 'Exit']
job_titles = [x[:-4] for x in os.listdir('job_descriptions') if x[0] != '.']
evaluators = ['eval1', 'eval2', 'eval3']

exit_status = False

pprint('Welcome to ResumeGuardian')

while not exit_status:
    action = get_response('What would you like to do?', actions)

    if action == 'Generate Resumes':
        job_title = get_response('What job would you like to generate resumes for?', job_titles)
        while True:
            save_random_resume(job_title)

    elif action == 'Evaluate Resumes':
        evaluator_name = get_response('Which evaluator would you like to use?', evaluators)
        job_title = get_response('Which job would you like to evaluate?', job_titles)
        if evaluator_name == 'eval1':
            evaluator.eval1(job_title)
        elif evaluator_name == 'eval2':
            evaluator.eval2(job_title)
        elif evaluator_name == 'eval3':
            evaluator.eval3(job_title)

        print('Finished evaluating resumes\n')

    elif action == 'Evaluate Scores':
        evaluator_name = get_response('Which evaluator\'s scores would you like to evaluate?', evaluators)
        job_title = get_response('Which job would you like to evaluate?', job_titles)
        impact.impact(evaluator_name, job_title)

    else:
        exit_status = True