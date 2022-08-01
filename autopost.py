import time 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pickle
import autoit
import json

# service = Service(r"C:\Users\Dm101\Desktop\Reddit Automation\venv\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")


def tiktok(category, rank = ''):
    service = Service(r"C:\Users\Dm101\Desktop\Reddit Automation\venv\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
    driver = webdriver.Chrome(service = service, desired_capabilities= {"resolution": "2048x1536"})
    
    caption = category + ' ' + str(rank) + '! '

    tags = [
        '#fyp',
        '#foryou',
        '#foryoupage',
        '#duet',
        '#viral',
        '#trending',
        '#tf2',
        '#funny',
        '#reddit',
        '#' + category,
        '#read',
        '#explorepage', 
        '#follow',
        '#like'
    ]

    driver.get('https://www.tiktok.com')

    #load all the cookies onto the current driver 
    with open('tiktok_cookies.pkl', 'rb') as f: 
        cookies = pickle.load(f)
        for cookie in cookies: 
            driver.add_cookie(cookie)

    #reload to load the cookies and login (OH MY GOD THIS WORKS)
    driver.get('https://www.tiktok.com/upload/?lang=en')
 
    time.sleep(5)

    #switch to frame where the upload button is at 
    driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe"))

    #click the upload buttton
    file_upload = driver.find_element(By.CLASS_NAME, 'css-14w2a8u')
    file_upload.click()

    time.sleep(3)

    path = r"C:\Users\Dm101\Desktop\Reddit Automation\{}\{}.mp4".format(category, category)

    #type the path on the file upload tab that pops up 
    autoit.win_active("Open") 
    autoit.control_send("Open","Edit1", path, flag = 1) 
    autoit.control_send("Open","Edit1", "{ENTER}")

    #input caption and tags
    box = driver.find_element(By.XPATH, "//div[@role = 'combobox']")
    box.send_keys(caption)

    time.sleep(0.3)

    for tag in tags: 
        box.send_keys(tag)
        time.sleep(1.5)
        #click the hashtag button
        driver.find_element(By.XPATH, "//div[@class = 'jsx-1095170125 hash-tag']").click()
        time.sleep(0.5)

    #scroll and click the post button
    post = driver.find_element(By.XPATH, "//button[@class = 'css-n99h88']")
    driver.execute_script("window.scrollTo(0, {})".format(post.location['y']))
    time.sleep(0.5)
    post.click()
    time.sleep(5)
    driver.quit()    

def youtube(category, rank = ''): 

    service = Service(r"C:\Users\Dm101\Desktop\Reddit Automation\venv\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")

    driver = webdriver.Chrome(service = service, desired_capabilities= {"resolution": "2048x1536"})

    driver.get('https://www.youtube.com/')

    with open('youtube_cookies.json') as d: 
        cookies = json.load(d)
        for cookie in cookies:
            driver.add_cookie(cookie)

    time.sleep(2)

    #load the uploading file 
    driver.get('https://studio.youtube.com/channel/UCoEA1PJkTc9IqlsQI9c6_sw/videos/upload?d=ud&filter=%5B%5D&sort=%7B%22columnType%22%3A%22date%22%2C%22sortOrder%22%3A%22DESCENDING%22%7D')

    time.sleep(3)

    #click the "choose file" button
    driver.switch_to.default_content
    buttons = driver.find_elements(By.XPATH, "//div[@class = 'label style-scope ytcp-button']")
    for button in buttons:
        if "SELECT FILES" in button.text: 
            button.click()

    time.sleep(2)

    path = r"C:\Users\Dm101\Desktop\Reddit Automation\{}\{}.mp4".format(category, category)

    #type the path on the file upload tab that pops up 
    autoit.win_active("Open") 

    #the "Flag" argument sends the literal keys for the characters inside the path string 
    #without the argument the control_send method 
    autoit.control_send("Open","Edit1", path, flag = 1) 
    autoit.control_send("Open","Edit1", "{ENTER}")
    
    time.sleep(5)

    #fill in the title and description
    textboxes = driver.find_elements(By.XPATH, "//div[@id = 'textbox']")
    
    titlebox = textboxes[0]
    description = textboxes[1]
    
    #titlebox
    titlebox.send_keys(Keys.BACKSPACE)
    titlebox.send_keys(category + ' ' + str(rank))
    titlebox.send_keys(' ')
    titlebox.send_keys('(r/{})'.format(category))

    #description
    description.send_keys('(r/{}) Reddit Insomniac'.format(category))
    description.send_keys(Keys.ENTER)
    description.send_keys(Keys.ENTER)
    description.send_keys('Thank you for choosing Reddit Insomniac!')
    description.send_keys(Keys.ENTER)
    description.send_keys(Keys.ENTER)

    tags = ['#reddit', '#redditstories', '#' + category, '#shorts']
    
    for tag in tags: 
        description.send_keys(tag + ' ')

    #click next
    buttons = driver.find_elements(By.XPATH, "//div[@class = 'label style-scope ytcp-button']")
    for button in buttons:
        if "NEXT" in button.text: 
            button.click()

    time.sleep(1)

    #click 'not for kids'
    buttons = driver.find_elements(By.ID, 'radioLabel')
    for button in buttons:
        if "No, it's not made for kids" in button.text:
            button.click()

    #click next
    buttons = driver.find_elements(By.XPATH, "//div[@class = 'label style-scope ytcp-button']")
    for button in buttons:
        if "NEXT" in button.text: 
            button.click()

    time.sleep(2)

    #click next
    buttons = driver.find_elements(By.XPATH, "//div[@class = 'label style-scope ytcp-button']")
    for button in buttons:
        if "NEXT" in button.text: 
            button.click()

    #click next
    buttons = driver.find_elements(By.XPATH, "//div[@class = 'label style-scope ytcp-button']")
    for button in buttons:
        if "NEXT" in button.text: 
            button.click()

    #click 'make public' button
    button = driver.find_elements(By.ID, 'offRadio')[3]
    button.click() 

    #click post button
    buttons = driver.find_elements(By.XPATH, "//div[@class = 'label style-scope ytcp-button']")
    for button in buttons: 
        if 'PUBLISH' in button.text: 
            button.click() 

    time.sleep(10)
    driver.quit() 

if __name__ == "__main__":
    # tiktok('UnEthicalLifeProTips', rank = 3)
    youtube('UnEthicalLifeProTips', rank = 3) 
