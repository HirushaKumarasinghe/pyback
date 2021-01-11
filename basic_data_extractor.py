import text_retriever
import re

pattern_email = re.compile(r'[a-zA-Z0-9-\.]+@[a-zA-Z-\.]*\.(com|edu|lk|net)')

p_test = re.compile(r'''(^\+
...    (\s|-|\.)? # separator
...    (\d{3}) # first 3 digits
...    (\s|-|\.) # separator
...    (\d{4}) # last 4 digits
... )''', re.VERBOSE | re.IGNORECASE)

pattern_linkedin = re.compile(r'http(s)?:\/\/([\w]+\.)?linkedin\.com\/in\/[A-z0-9_-]+\/?')
pattern_facebook = re.compile(r'(?:https?:\/\/)?(?:www\.)?facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*?(\/)?([\w\-\.]*)')
pattern_twitter = re.compile(r'(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*?(\/)?([\w\-\.]*)')
pattern_stackoverflow = re.compile(r'(?:https?:)?\/\/(?:www\.)?stackoverflow\.com\/users\/(?P<id>[0-9]+)\/(?P<username>[A-z0-9-_.]+)\/?')
pattern_youtube_channel = re.compile(r'(?:https?:)?\/\/(?:[A-z]+\.)?youtube.com\/channel\/(?P<id>[A-z0-9-\_]+)\/?')
pattern_youtube_user = re.compile(r'(?:https?:)?\/\/(?:[A-z]+\.)?youtube.com\/user\/(?P<username>[A-z0-9]+)\/?')
pattern_pinterest = re.compile(r'(?:https?:\/\/)?(?:id\.)?pinterest\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*?(\/)?([\w\-\.]*)')
pattern_github = re.compile(r'(?:https?:)?\/\/(?:www\.)?github\.com\/(?P<login>[A-z0-9_-]+)\/?')


pattern_mobile = re.compile(r'')
pattern_date = re.compile(r'')

def extract_basic_email():
    emails = []
    cv_text = text_retriever.retrieve_text_from_image()
    matches = pattern_email.finditer(cv_text)

    for match in matches:
        emails.append(match.group(0))
    print(emails[0])

def extract_basic_web():
    webs = []
    cv_text = text_retriever.retrieve_text()
    matches = p_test.finditer(cv_text)

    for match in matches:
        webs.append(match.group(0))
    print(webs[0])

extract_basic_email()
# extract_basic_web()