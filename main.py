import requests
from bs4 import BeautifulSoup
from requests.api import get
import confidential
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time 

def sendMessage (chat_id, text, parse_mode, no_link_preview):
    link='https://api.telegram.org/bot' + confidential.api_key + '/sendMessage'
    params = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode,
                'disable_web_page_preview': no_link_preview,
                #this is hardcoded
                'disable_notification': False 
            }
    response = requests.post(link, json=params, timeout=2)
    print(response.status_code)
    return response

def getUpdates ():
    #take out ?offset=-1 to receive all messages
    link = 'https://api.telegram.org/bot' + confidential.api_key + '/getUpdates?offset=-1'
    response = requests.get(link, timeout=2)
    print(response.status_code)
    return response

def check_message (mes, id):

    print(mes)
    if (mes.find('/start')!=-1):
        sendMessage(id, 'use /register to register to updates', 'Markdown', True)

    elif (mes.find('/register')!=-1):
        with open('mailing_list.txt', 'r+', encoding = 'utf-8') as file:
            file.write(str(id) + '\n')
        sendMessage(id, '**bot goes brrrr** you can go relax!', 'Markdown', True)

def check_website_change ():

    trigger = 0
    f = open("reference_page.html", "r" , encoding = 'utf-8')
    g = open("screenshot.png", "wb")
    
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=chrome-data")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=720,1080")
    chrome_options.add_argument("--hide-scrollbars")

    driver = webdriver.Chrome('./chromedriver',options=chrome_options)

    print ('Checking webiste')
    site_link = 'https://www.ilpiemontetivaccina.it/preadesione/#/'
    driver.get(site_link)

    element = driver.find_element_by_id("vday")
    html = element.get_attribute('innerHTML')

    time.sleep(1)
    if (f.read() != html):
        trigger = 1
        element.screenshot_as_png #to take the page to the rigth place

        #taking screenshot of "vday" section
        print('Taking screenshot')
        driver.execute_script("document.getElementById('outdated').innerHTML = '';")
        time.sleep(4)
        element_png = element.screenshot_as_png
        g.write(element_png)
        driver.quit()

    f.close()
    g.close()

    return trigger

    #html = soup.find('body').getText()

    # if (html!=text):

    #     #do things
    #     print('Something changed!')
    #     text = 'Something changed on the PineBook page you were watching \n[link here](' + product_link + ')'
    #     response = sendMessage (confidential.id_privatechat, text, 'Markdown', True)
    #     f.close()
    #     return response

    # else:
    #     print('All the same :(')
    #     f.close()
    #     return 0


f = open("last_message_id.txt", "r+" , encoding = 'utf-8')

counter = 0

while True:
    time.sleep(0.5)
    counter = counter + 1
    counter = counter % 100
    response = getUpdates()
    a = json.loads(response.text)
    print(json.dumps(a['result'], indent=4, sort_keys=True))

    text = a['result'][0]['message']['text']
    username = a['result'][0]['message']['chat']['username']
    message_id = a['result'][0]['message']['message_id']
    user_id = a['result'][0]['message']['chat']['id']
    
    # ______                                                  
    # | ___ \                                                 
    # | |_/ /   _ _ __   __ _ _ __  _   ___      ____ _ _   _ 
    # |    / | | | '_ \ / _` | '_ \| | | \ \ /\ / / _` | | | |
    # | |\ \ |_| | | | | (_| | | | | |_| |\ V  V / (_| | |_| |
    # \_| \_\__,_|_| |_|\__,_|_| |_|\__, | \_/\_/ \__,_|\__, |
    #                                __/ |               __/ |
    #                               |___/               |___/ 

    if (counter==1):
        check_website_change()

    #   ___                                  
    #  / _ \                                 
    # / /_\ \_ __  _____      _____ _ __ ___ 
    # |  _  | '_ \/ __\ \ /\ / / _ \ '__/ __|
    # | | | | | | \__ \\ V  V /  __/ |  \__ \
    # \_| |_/_| |_|___/ \_/\_/ \___|_|  |___/
                                             
    f.seek (0)
    history=f.read()
    
    #checking if last message has already been seen
    if (str(message_id) != history):
        print('New Message')
        check = 1 
    else:
        print('Same Message')
        check = 0

    #answer if it's a new message
    if (check):
        print('Answering!')
        f.seek (0)
        f.write(str(message_id))
        check_message(text, user_id)
        sendMessage(confidential.id_privatechat, text, 'Markdown', True)

