### Import Libraries
import os
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from utility_methods.utility_methods import *
import urllib.request



### Write a class for a Instagram Bot

class InstaBot:
    def __init__(self, username=None, password=None):
        self.username= config['IG_AUTH']['USERNAME']
        self.password = config['IG_AUTH']['PASSWORD']

        ### Crete browser
        self.login_url = config['IG_URLS']['LOGIN']
        self.nav_user_url = config['IG_URLS']['NAV_USER']
        self.get_tag_url = config['IG_URLS']['SEARCH_TAGS']

        self.driver = webdriver.Chrome(config['ENVIRONMENT']['CHROMEDRIVER_PATH'])

        self.logged_in = False

    ### Self close browser
    def closeBrowser(self):
        self.driver.close()
### Have Bot automatically login
    @insta_method
    def login(self):
        self.driver.get(self.login_url)  ### Load the IG login Page
        
        time.sleep(5)
        login_button = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')

        ### Locate Username, PW and Login button elements
        username_input = self.driver.find_element_by_name('username')
        password_input = self.driver.find_element_by_name('password')
        
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_button.click()

        time.sleep(3) ### Wait for pop ups and select appropriate buttons
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/section/div/button').click()
        
        time.sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()


    ### Bot will search certain tags to follow
    @insta_method
    def like_photo(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(5)


        # gathering photos
        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                # print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2, 4))
                like_button = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span/svg')
                like_button().click()
                for second in reversed(range(0, random.randint(18, 28))):
                    print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    time.sleep(3)
            except Exception as e:
                time.sleep(3)
            unique_photos -= 1

    ### Follow Users
    @insta_method
    def follow_user(self, user):
        self.nav_user(user)

        follow_buttons = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')

        for btn in follow_buttons:
            btn.click()



if __name__ == '__main__':

    config_file_path = './config.ini' 
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)

    bot = InstaBot()
    bot.login()

    hashtags = ['amazing', 'beautiful', 'photography', 'nofilter',
                'fashion', 'ootd', 'women', 'shopping', 'trending', 'inspiration',
                'selflove']

    while True:
        try:
            # Choose a random tag from the list of tags
            tag = random.choice(hashtags)
            bot.like_photo(tag)
            bot.follow_user(tag)
        except Exception:
            bot.closeBrowser()
            time.sleep(60)
            bot = InstaBot()
            bot.login()





