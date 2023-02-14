from rich.console import Console
from bs4 import BeautifulSoup
from auto_complete import *
from rich import print
from utils import *
import googlesearch
import requests
import os, sys

os.chdir(sys.path[0])

if not os.path.isfile('config.py'):
    with open('config.py','w') as cfg:
        cfg.write("PHPSESSID = 'ENTER YOUR PHP SESSION ID HERE!'")
    print('[purple]Check root dir and fill PHPSESSID var in config.py')
    quit()

from config import *

console = Console()#Rich console

print('''[red]
  _   _                       _       _____ _           _           
 | \ | | __ _ _   _ _ __ ___ | | __  |  ___(_)_ __   __| | ___ _ __ 
 |  \| |/ _` | | | | '__/ _ \| |/ /  | |_  | | '_ \ / _` |/ _ \ '__|
 | |\  | (_| | |_| | | | (_) |   <   |  _| | | | | | (_| |  __/ |   
 |_| \_|\__,_|\__,_|_|  \___/|_|\_\  |_|   |_|_| |_|\__,_|\___|_|   
[/red]''')

do_not_search = False

question = console.input('[yellow]Enter a random question from test or link: ')

if question.lower().startswith('http'):
    do_not_search = True

find = False
if not do_not_search:
    with console.status("[bold cyan]🔎 Search test url...") as status:
        while not find:
            for result in googlesearch.search(question,lang='ua',num_results=30):
                if 'naurok' in result and '/test' in result:
                    status.stop()
                    test_info(BeautifulSoup(requests.get(result,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',}).content, 'lxml'))
                    if console.input(f'[green]Found test url: [/green][blue]{result}[/blue]\n[yellow]Skip (y,n): [/yellow]').lower() == 'n':
                        test_url = result
                        find=True
                        break
                    else:
                        status.start()
                        pass
                        
        
if do_not_search:
    test_url = question

site = requests.get(test_url,
    headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',

    })

test_soup = BeautifulSoup(site.content, 'lxml')

for a in test_soup.find_all('a',class_='test-action-button', href=True):
    if str(a['href']).endswith('print'):
        print_url = 'https://naurok.com.ua'+a['href']

    elif str(a['href']).startswith('/test/start/'):
        test_start_url = 'https://naurok.com.ua'+a['href']

test = requests.get(print_url,
headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',
    },cookies={'PHPSESSID':PHPSESSID})
    
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

print('[purple]Answers: ')
print(questions_dict)
print('[green]Print url: [/green][blue]'+print_url)
test_info(test_soup)

if console.input('[yellow]Auto complete (y,n): ').lower() == 'y':
    conv_boolean = {'y':True,'n':False}
    name = console.input('[yellow]Enter name: ')
    enable_random_delay = console.input('[yellow]Enable random delay (y,n): ')
    count_of_errors = console.input('[yellow]Count of errors (0 for disable): ')

    get_all(test_start_url,
    questions_dict,
    name,
    conv_boolean[enable_random_delay.lower()], 
    count_of_errors)

else:
    quit()
