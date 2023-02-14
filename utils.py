from rich import print

def test_info(test_soup):
    test_name = test_soup.find('h1',class_='h1-block h1-single', title=True)
    test_author = test_soup.find('div',class_='control-label').a

    for info in test_soup.find_all('div',class_='control-label'):
        if str(info.text).startswith('Додано'):
            test_date = str(str(info.text).split(':')[1])[1:]
        
        elif str(info.text).startswith('Предмет'):
            test_lesson = str(str(info.text).split(':')[1])[1:]

    print('[green]Test name: '+test_name.text)
    print('[green]Test author: '+test_author.text)
    print('[green]Test date: '+test_date)
    print('[green]Test lesson: '+test_lesson)