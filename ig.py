### Import Libraries
import os
from selenium import webdriver


### Write a class for a Instagram Bot

class Instabot:
    def __init__(self, username, password):
        self.username= username
        self.password = password

        ### Crete browser
        self.driver = webdriver.Firefox()
        
        self.login()

### Have Bot automatically login
    def login(self):
        self.driver.get('https://www.instagram.comn/accounts/login/')
        
        self.driver.find_element_by_name('username').send_keys(self.username)
        
        self.driver.find_element_by_name('password').send_keys(self.password)
