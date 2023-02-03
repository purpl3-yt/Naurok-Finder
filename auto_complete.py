from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep as wait
import random
def get_all(test_start_url: str, answers: dict, name: str, enable_random_delay: bool):

    driver = webdriver.Firefox()

    driver.get(test_start_url)

    inputElement = driver.find_element(value='sessionform-firstname')
    inputElement.send_keys(name)

    driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/form/button').click()#Button "Почати тест"

    wait(3)#Wait for page load

    questions_count = driver.find_element(By.XPATH,'/html/body/div[1]/div/nav/div/div/div[1]/div/div/span[2]').text

    for x in range(int(questions_count)):

        if enable_random_delay:
            wait(random.randint(5,20))
         
        elif not enable_random_delay:
            wait(5)
            

        question = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div').text#Вопрос
        print('Current question: '+question)
        id_question = str(driver.find_element(By.XPATH, '/html/body/div[1]/div/nav/div/div/div[1]/div/div/span[1]').text)#Айди вопроса
        print('ID of question: '+id_question)
        
        quiz_buttons = {}

        for button_index,button_letter in zip(range(1,4+1),['а','б','в','г']):    
            quiz_buttons[button_letter] = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div/div/div/div[2]/div[2]/div/div[{button_index}]/div/div')

        if len(answers[id_question][1]) <= 1:#if answers is bigger than 1
            quiz_buttons[answers[id_question][1][0]].click()

        elif len(answers[id_question][1]) > 1:
            for temp in answers[id_question][1]:
                quiz_buttons[temp].click()

            driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div[2]/div[3]/a').click()

    wait(5)


        
    if input('Close window [y,n]: ').lower() == 'y':
        driver.close()
