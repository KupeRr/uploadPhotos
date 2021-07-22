from typing import Tuple
from selenium.webdriver import Chrome
from selenium import webdriver
import json
import os
from time import sleep


##########################################################################################################

####################################
###          Constants           ###
####################################

file = ".config"
with open(file, 'rb') as f:
    config  = json.load(f)

PASSWORD            = config['PASSWORD']
MAIL_LOGIN          = config['MAIL_LOGIN']
NUM_BY_ONE_LOAD     = int(config['NUM_BY_ONE_LOAD'])
FOLDER_NAME         = config['FOLDER_NAME']

URL = 'https://bez-kompleksov.com/search'

##########################################################################################################

##############################################
###          Main work functions           ###
##############################################

def log_in(driver):
    driver.find_element_by_class_name('btn-landing').click()
    sleep(1)
    input_fields = driver.find_elements_by_class_name('input-text')

    input_fields[0].send_keys(MAIL_LOGIN)
    input_fields[1].send_keys(PASSWORD)

    driver.find_element_by_class_name('btn-landing--red').click()

    return driver

def connect():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    driver = Chrome(options=options)
    driver.set_window_size(1920, 1080)
    return driver

def go_to_url(url, driver):
    driver.get(url)
    return driver  

def get_photos(link):
    if os.path.isdir(f"{FOLDER_NAME}/{link.split('/')[-1]}"): return False

    driver_loader = connect()
    driver_loader = go_to_url(link, driver_loader)
    sleep(3)

    num = int(driver_loader.find_elements_by_class_name('user-about__item')[2].text.split()[0])
    if num >= 2:
        os.mkdir(f"{FOLDER_NAME}/{link.split('/')[-1]}")
        print('Find new girl!')

        i = 0
        photos_items = driver_loader.find_elements_by_class_name('photo-slide')
        for item in photos_items:
            if num > 5 and i == 5:
                break

            print(f'Load {i+1} photo...')
            item.click()
            sleep(2)
            src = driver_loader.find_elements_by_class_name('slick-current')

            girl_folder = link.split('/')[-1]
            with open(f"{FOLDER_NAME}/{girl_folder}/photo{i+1}.png", 'wb') as file:
                file.write(src[-1].find_element_by_tag_name('img').screenshot_as_png)
                sleep(1)
            i += 1

            driver_loader.find_element_by_class_name('modal-close').click()
        driver_loader.close()
        print(f'Get all photos in folder: {girl_folder}!')
        return True
    return False

def get_content(driver):
    if not os.path.isdir(FOLDER_NAME):
            os.mkdir(FOLDER_NAME)
    sleep(3)

    print('Start parsing...')
    i = 0
    while NUM_BY_ONE_LOAD != i:
        link = driver.find_element_by_class_name('search-profile').get_attribute('href')

        if not get_photos(link):
            print('Skipped the data that was already loaded...')
            i -= 1
        i+= 1
        driver.find_element_by_class_name('btn--approve').click()

##########################################################################################################

def main():
    driver = connect()
    driver = go_to_url(URL, driver)
    driver = log_in(driver)
    sleep(3)
    get_content(driver)

main()






