from rich.console import Console
from download import download
from bs4 import BeautifulSoup
from rich import print
import googlesearch
import requests
import os, sys
from auto_complete import *
try:os.remove('geckodriver.log')
except FileNotFoundError:pass

os.chdir(sys.path[0])

console = Console()#Rich console


if not os.path.isfile('./geckodriver'):
    download('https://raw.githubusercontent.com/purpl3-yt/trash-bin/main/files_for_my_programs/geckodriver','./geckodriver',replace=True)

print('''[red]
  _   _                       _       _____ _           _           
 | \ | | __ _ _   _ _ __ ___ | | __  |  ___(_)_ __   __| | ___ _ __ 
 |  \| |/ _` | | | | '__/ _ \| |/ /  | |_  | | '_ \ / _` |/ _ \ '__|
 | |\  | (_| | |_| | | | (_) |   <   |  _| | | | | | (_| |  __/ |   
 |_| \_|\__,_|\__,_|_|  \___/|_|\_\  |_|   |_|_| |_|\__,_|\___|_|   
[/red]''')

do_not_search = False

question = console.input('[yellow]Enter a random question from test or link: [/yellow]')

if question.lower().startswith('https'):
    do_not_search = True

if not do_not_search:
    print('Search test url...')
    
    for result in googlesearch.search(question+' inurl:naurok',lang='ua',num_results=30):
        if 'naurok' in result and '/test' in result:
            if input(f'Found test url: {result}\nSkip [y,n]: ').lower() == 'n':
                test_url = result
                break
            else:
                pass
        
if do_not_search:
    test_url = question

site = requests.get(test_url,
    headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',

    })

soup = BeautifulSoup(site.content, 'lxml')

for a in soup.find_all('a',class_='test-action-button', href=True):
    if str(a['href']).endswith('print'):
        print_url = 'https://naurok.com.ua'+a['href']

    elif str(a['href']).startswith('/test/start/'):
        test_start_url = 'https://naurok.com.ua'+a['href']

test = requests.get(print_url,
headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',

    },cookies={'PHPSESSID':'ENTER_YOUR_PHPSESSID_HERE!!!'})
    
soup = BeautifulSoup(test.content, 'lxml')

keys = []

for div in soup.find_all('div',class_='answer-key'):
    for div_children in div:
        if str(div_children):
            formated = str(div_children).replace('\n','')
            formated = formated.replace('<div>','')
            formated = formated.replace('</div>','')
            if formated!='':
                keys.append(formated)

questions_dict = {}

for div,question_num,key in zip(soup.find_all('div',class_='col-md-11 no-padding'),soup.find_all('div',class_='q-num'),keys):
    question_num = str(question_num.text).replace('\n','')
    question_num = question_num[:question_num.find('.')]#Question number

    questions_dict[question_num] = (
        str(div.find('p').text),#Question
        [x for x in str(key[str(key).find('.')+1:str(key).find('(')]).split(' ') if x!=''])#Answers

print(questions_dict)
print('Print url: '+print_url)

if input('Auto complete [y,n]: ').lower() == 'y':
    conv_boolean = {'y':True,'n':False}
    name = input('Enter name: ')
    enable_random_delay = input('Enable random delay [y,n]: ')
    get_all(test_start_url,questions_dict,name,conv_boolean[enable_random_delay.lower()])

else:
    quit()
