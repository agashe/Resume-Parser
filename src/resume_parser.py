from argparse import ArgumentParser
from PyPDF2 import PdfReader
from enum import Enum
import re
import json

# Define arguments to get the resume path
parser = ArgumentParser(
    prog='Resume-Parser',
    description='A tool to extract info from resume'
)

parser.add_argument("-f", "--file", dest="filename",
    help="The path to the resume", metavar="FILE"
)

parser.add_argument("-o", "--output", dest="output",
    help="The path to the output json file", metavar="FILE"
)

args = parser.parse_args()

# If no filepath was provided terminate !
if not args.filename:
    print("No resume path was provided , use -h for more info !")
    exit()

# Reading PDF file
resume_lines = []

try:
    reader = PdfReader(args.filename)

    for page in reader.pages:
        resume_lines += page.extract_text().split("\n")

except:
    print("Invalid PDF resume , use -h for more info !")
    exit()

# Process resume
InfoType = Enum('InfoType', ['Personal', 'Skills', 'Education', 'Experience'])
scope = InfoType.Personal
details = {
    'personal': {
        'name': '',
        'email': '',
        'phone': '',
        'mobile': '',
        'address': '',
    },
    'skills': [],
    'experience': '',
    'education': '',
}

name_pattern = re.compile('^[A-Z]{1}[a-z-.]+\s+[A-Z]{1}[a-z-.]+$')
email_pattern = re.compile('[a-zA-Z0-9 ._-]+@[a-zA-Z0-9 ._-]+\.[a-zA-Z0-9 _-]+')
phone_pattern = re.compile('(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}')
mobile_pattern = re.compile('(\+\d{1,3}[- ]?)?\d{8}')
address_pattern = re.compile('[a-zA-Z\- ]+\,[a-zA-Z\- ]+')

skills_pattern = re.compile('([a-zA-Z0-9.-_#&*+]+,?)+')

for line in resume_lines:
    line = line.strip()

    if line == '':
        continue

    if 'skills' in line.lower() and scope != InfoType.Skills:
        scope = InfoType.Skills
        continue
    elif (any(word in line.lower() for word in ['experience', 'employment', 'working', 'history']) 
            and scope != InfoType.Experience):
        scope = InfoType.Experience
        continue
    elif 'education' in line.lower() and scope != InfoType.Education:
        scope = InfoType.Education
        continue

    if scope == InfoType.Personal:
        if details['personal']['name'] == '':
            match_name = name_pattern.search(line) 
            if match_name:
                details['personal']['name'] = match_name.group(0).strip()

        if details['personal']['email'] == '':
            match_email = email_pattern.search(line) 
            if match_email:
                details['personal']['email'] = match_email.group(0).strip()

        if details['personal']['phone'] == '':
            match_phone = phone_pattern.search(line)
            if match_phone:
                details['personal']['phone'] = match_phone.group(0).strip()

        if details['personal']['mobile'] == '':
            match_mobile = mobile_pattern.search(line)
            if match_mobile:
                details['personal']['mobile'] = match_mobile.group(0).strip()
        
        if details['personal']['address'] == '':
            match_address = address_pattern.search(line) 
            if match_address:
                details['personal']['address'] = match_address.group(0).strip()

    if scope == InfoType.Skills:
        if ':' in line :
            line = line.split(':')[1]

        line = line.replace(' ', '')
        match_skills = skills_pattern.search(line) 
        if match_skills:
            details['skills'] += (match_skills
                .group(0)
                .strip()
                .split(','))
    
    if scope == InfoType.Experience and details['experience'] == '':
        details['experience'] = ' '.join(line.split())
        scope = ''

    if scope == InfoType.Education and details['education'] == '':
        details['education'] = ' '.join(line.split())
        scope = ''

# Dump the JSON output to a file or print
# if the 'output' flag wasn't passed
if args.output:
    with open(args.output, 'w') as out:
        json.dump(details, out)
    
    print("The resume was parsed successfully !")
else:
    print(json.dumps(details))