# generate.py (explore-mailer)
# Generate a digest for sending
import argparse
import json
import os
from functools import reduce


def read_feedback_file(feedback_file):
    with open(feedback_file) as f:
        data = json.load(f)

        if len(data) < 1:
            return []

        valid_keys = reduce(lambda s1, e2: s1.intersection(set(e2['responses'].keys())),
                            data,
                            set(data[0]['responses'].keys()))

        for entry in data:
            recipient = entry['recipient']
            for k in ('first', 'last', 'email'):
                if k not in recipient:
                    raise KeyError(f'Missing key {k}')

            responses = entry['responses']
            for rk in responses:
                if rk not in valid_keys:
                    del responses[rk]

        return data, valid_keys


def read_template_file(template_file):
    with open(template_file) as f:
        return f.read().splitlines()


def read_params_file(params_file):
    with open(params_file) as f:
        return json.load(f)


def group(data, keys):
    def rec_str(rec):
        return rec['first'], rec['last'], rec['email']

    all_recipients = set(rec_str(d['recipient']) for d in data)

    groups = {recipient: {response: [] for response in keys} for recipient in all_recipients}
    for entry in data:
        recipient = rec_str(entry['recipient'])
        responses = entry['responses']
        for response in keys:
            groups[recipient][response].append(responses[response])

    return groups


def generate(feedback_file, template_file, output_file='digest.json', params_file=None):
    for f in [feedback_file, template_file] + [params_file] if params_file else []:
        if not os.path.isfile(f):
            raise FileNotFoundError(f)

    feedback_data, valid_keys = read_feedback_file(feedback_file)
    template_data = read_template_file(template_file)
    params_data = read_params_file(params_file) if params_file else {}

    template_subject = template_data[0]
    template_body = '\n'.join(template_data[1:])

    groups = group(feedback_data, valid_keys)

    digest = []
    for (first, last, email), feedback in groups.items():
        params = params_data.copy()
        params.update({'first': first, 'last': last, 'email': email})

        feedback_str = '\n\n'.join([
            '\n'.join([question] + [
                f'- {answer}'
                for answer in answers
            ]) for question, answers in feedback.items()
        ])

        item = {
            'params': params,
            'subject': template_subject.format(**params),
            'body': template_body.format(**params, feedback=feedback_str)
        }

        digest.append(item)

    with open(output_file, 'w') as f:
        json.dump(digest, f, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a digest for sending')
    parser.add_argument('-o', '--output', type=str, default='digest.json', help='Output JSON file (default=digest.json)')
    parser.add_argument('-p', '--params', type=str, help='Parameters JSON file')
    parser.add_argument('feedback_file', type=str, help='Feedback JSON file')
    parser.add_argument('template_file', type=str, help='Template TXT file')
    args = parser.parse_args()
    generate(args.feedback_file, args.template_file, output_file=args.output, params_file=args.params)
