import csv
import json

lines = []
survey = []

with open('survey.csv', 'r') as f:
    reader = csv.reader(f)

    for line in reader:
        line[0] = line[0].strip()
        line[1] = line[1].strip()
        line[2] = line[2].strip()
        survey.append(line)

with open('feedback.csv', 'r') as f:
    reader = csv.reader(f)

    for line in reader:
        lines.append(line)


feedback = []
lines = lines[1:]
questions = ['What is something you learned from watching this presentation?',
             'What is something that the presenter did well?',
             'What is something that the presenter could improve upon?',
             'What is your overall rating of this presentation?']
FEEDBACK_STARTS_AT = 6

for line in lines:
    present_first = line[4].strip()
    present_last = line[5].strip()
    email = ''

    found = False
    for student in survey:
        if student[2] == present_last and (student[0] == present_first or student[1] == present_first):
            found = True
            if student[6] == 'Section E (2pm)':
                email = student[3]
            break

    if not found:
        # print(f'Unable to find: {present_first} {present_last} so skipping student')
        continue
    if email == '':
        continue

    responses = {}
    for i in range(len(questions)):
        responses[questions[i]] = line[FEEDBACK_STARTS_AT + i]
    this_line_feedback = {
        'recipient': {
            'first': present_first,
            'last': present_last,
            'email': email,
        },
        'responses': responses,
    }
    feedback.append(this_line_feedback)

json_object = json.dumps(feedback, indent = 4)  
print(json_object)
# print(len(feedback))
