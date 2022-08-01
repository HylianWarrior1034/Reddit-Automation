import requests 
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
from pydub import AudioSegment
import gtts
import pandas as pd 
from PIL import Image
import os 
import shutil
import time 
import speedup 
import numpy as np 
import random 
from movie import movie
from autopost import *

username = "HylianWarrior1034"          # Enter your username for reddit
password = "Dsm10142!"                   # Enter your password for reddit

service = Service(r"C:\Users\Dm101\Desktop\Reddit Automation\venv\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'AutoBot/0.0.1'}

#DISABLE ALL CHROME NOTIFICATIONS AND SET THE WINDOW RESOLUTION 
options = webdriver.ChromeOptions() 
options.add_argument("--disable-infobars")
# options.add_argument("start-maximized")
options.add_argument("--disable-extensions")


# Pass the argument 1 to allow and 2 to block
options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

options.add_experimental_option('excludeSwitches', ['enable-logging'])

#launch chrome webdriver with the defined options 
driver = webdriver.Chrome(service = service, options=options, desired_capabilities= {"resolution": "2048x1536"})
driver.set_window_size(660, 830)

screen_width = driver.get_window_size()['width']
screen_height = driver.get_window_size()['height']

sc_width = 809
scale = sc_width/screen_width

title_text = [] 
body_text = []
comment_text = [] 

#get the links of the subreddits posts 
def get_links(subreddit, category, timeframe, rank = 1):
    # category: controversial, best, hot, new, random, rising, top
    # timeframe: hour, day, week, month, year, all
    res = requests.get("https://www.reddit.com/r/{}/{}.json?limit=100&t={}".format(subreddit, category, timeframe), headers = headers)

    link = []
    score = [] 

    for post in res.json()['data']['children']: 
        link.append(post['data']['permalink'])
        score.append(post['data']['score'])

    df = pd.DataFrame({
        'link': link,
        'score': score
    })

    df.sort_values(by = 'score')

    return df.loc[rank]

def getScreenshots(df, category, number_of_comments = 2):
    try:
        driver.get("https://www.reddit.com/")
    except InvalidSessionIdException: 
        time.sleep(2)
        getScreenshots(df, category)

    profile = driver.find_element(By.ID, 'USER_DROPDOWN_ID')
    profile.click() 

    time.sleep(1)

    #check if there is an existing directory for the category 
    dir = os.path.join("{}".format(category))

    if not os.path.exists(dir): 
        os.mkdir(dir)

    #check if there is an existing directory for the image of the category
    dir = os.path.join("{}/images".format(category))

    if os.path.exists(dir): 
        shutil.rmtree(dir)

    os.mkdir(dir)

    #log in to reddit and turn it into dark mode (and whatnot)
    #exception is for the rare moments where the reddit homepage does not load properly and we have to reload 
    try:
        elements=driver.find_elements(By.XPATH, "//button[@class='_3fbofimxVp_hpVM6I1TGMS GCltVwsXPu5lE-gs4Nucu']")
    except NoSuchElementException: 
        driver.close()
        getScreenshots(df, category)

    for element in elements:
        if element.text == 'Settings': 
            element.click()
            break

    time.sleep(0.5)

    try: 
        dark_mode = driver.find_element(By.XPATH, "//button[@class='nBh6t8H3UNZpI1Ce9s6yQ']")
        dark_mode.click() 
    except NoSuchElementException:
        driver.close() 
        getScreenshots(df, category)

    profile.click() 
    logIn() 

    time.sleep(5)

    link = df['link'] 
    #go to the post website link
    driver.get('https://www.reddit.com{}tack%20?depth=1'.format(link))

    time.sleep(3) 

    #if reddit gives some dumbass pop-up, close it 
    try:
        close = driver.find_element(By.XPATH, "//button[@aria-label ='Close']")
        close.click() 
    except NoSuchElementException: 
        pass

    #if the post has a expand button, click it 
    try: 
        expand = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Expand content']")
        expand.click() 
        body = driver.find_element(By.CLASS_NAME, "_1qeIAgB0cPwnLhDF9XSiJM")
        body.click() 

    except NoSuchElementException:
        pass

    #screenshot and crop the title of the post
    titleScreenshot(category) 

    time.sleep(3) #wait for a bit

    #find the post content and screenshot
    #if there is no post content, pass
    try: 
        driver.find_element(By.XPATH, "//div[@class='_2w7fkGYeZk22ZtKCTcGj_T']")
        bodyScreenshot(category) 
    except: 
        pass
        
    commentScreenshot(category, number_of_comments)

    #text to speech
    speechFiles(category)

    #quit driver
    driver.quit() 

def titleScreenshot(category):
    #get a screenshot of the base website link (no edits no element searching)
    #the '1' is in the front so the title image comes to the top of the directory 
    driver.save_screenshot('{}/images/1title.png'.format(category))
    base_image = Image.open('{}/images/1title.png'.format(category))

    #find the bounding box of the title section 
    title = driver.find_element(By.CLASS_NAME, 'uI_hDmU5GSiudtABRz_37')
    title_end = driver.find_element(By.CSS_SELECTOR, "a[data-click-id='body']")

    title_text.append(title_end.text)
    
    x1 = title.location['x']*scale
    x2 = x1 + title.size['width']*scale
    y1 = title.location['y']*scale + 5
    y2 = title_end.location['y']*scale + title_end.size['height']*(scale + 0.3) 

    try: 
        bottom = driver.find_element(By.XPATH, "//div[@class = '_2fiIRtMpITeCAzXc4cANKp _1mK-LVHGTTlcFpMsjItjYJ']")
        y2 = bottom.location['y']*scale + bottom.size['height']*(scale + 0.8)
    except NoSuchElementException:
        pass

    box = (x1, y1, x2, y2)  
  
    #crop the images based on the box 
    cropped_image = base_image.crop(box)
    base_image = base_image.resize(cropped_image.size)
    base_image.paste(cropped_image, (0, 0))
    base_image.save('{}/images/1title.png'.format(category))

def bodyScreenshot(category): 
    body = driver.find_elements(By.CLASS_NAME, "_1qeIAgB0cPwnLhDF9XSiJM")
            
    driver.execute_script("window.scrollTo(0, 200)")

    y_position = []

    for i, chunk in enumerate(body): 
        x = chunk.location['x'] 
        y = chunk.location['y'] - 48 #48 is the size of the banner (depends on the screen resolution but change later if needed) 

        if i != 0: 
            temp = y_position.pop()
            if chunk.location['y'] - 10 <= temp <= chunk.location['y'] + 10:
                driver.execute_script("window.scrollTo(0, {})".format(y))
            else:
                break

        time.sleep(0.4)

        chunk.screenshot('{}/images/body{}.png'.format(category, i))

        #add the margins on the side so it doesn't look squished 
        addMargin('{}/images/body{}.png'.format(category, i))

        #append the text to the list for tts later 
        body_text.append(chunk.text)
        
        #concatenate images if the word count is low 
        if i != 0 and len(chunk.text) <= 200: 
            im1 = Image.open('{}/images/body{}.png'.format(category, i-1))
            im2 = Image.open('{}/images/body{}.png'.format(category, i))
            dst = Image.new("RGB", (im1.width, im1.height + im2.height))
            dst.paste(im1, (0,0))
            dst.paste(im2, (0, im1.height))
            dst.save('{}/images/body{}.png'.format(category, i))

        time.sleep(1.4)

        y_position.append(chunk.size['height']+chunk.location['y'])

def commentScreenshot(category, number_of_comments = 2): 

    #click any expanding buttons for the comments
    try: 
        driver.find_element(By.XPATH, '//button[@class="_1nGapmdexvR0BuOkfAi6wa t1_hth39r7 O_Ica0k2O4KFcZyNfsJDU _2Gzh48SaLz7dQBCULfOC6V"]').click()
        time.sleep(2)
    except NoSuchElementException:
        pass

    #skip any bot comments (and mod comments)  
    comment_headers = driver.find_elements(By.XPATH, "//div[@data-testid = 'post-comment-header']")
    comments = driver.find_elements(By.XPATH, "//div[@data-testid = 'comment']")
    frames = driver.find_elements(By.XPATH, "//div[@class = '_3sf33-9rVAO_v4y0pIW_CH'] | //div[@class='_3sf33-9rVAO_v4y0pIW_CH _3kYyDFXW4SA2vk-vehWhXw']")

    new_frames = []

    #filter the frames list (since this class-name includes some junk)
    for frame in frames: 
        if "Continue this thread" not in frame.text: 
            new_frames.append(frame)

    counter = 0

    #look through the comment section and screenshot as necessary
    for header, comment in zip(comment_headers, comments):
        
        #THIS CLICK IS JUST TO AVOID HOVER EFFECTS FROM HAPPENING 
        comment.click()

        #extract _this_ number of comments 
        if counter == number_of_comments: 
            break 
        
        driver.execute_script("window.scrollTo(0, {})".format(header.location['y']-54))
        
        #skip any comment with MOD in it 
        if 'MOD' in header.text: 
            counter += 1 
            number_of_comments += 1
            continue

        #this line finds the body of the comment 
        body = comment.find_elements(By.XPATH, ".//p[@class = '_1qeIAgB0cPwnLhDF9XSiJM']")

        # if the comment is not that long, just save the whole comment frame as one screenshot
        if len(comment.text) < 525: 
            driver.execute_script("window.scrollTo(0, {})".format(new_frames[counter].location['y']-48))
            time.sleep(2)
            new_frames[counter].screenshot('{}/images/comment{}.png'.format(category, counter))
            comment_text.append(comment.text)
            time.sleep(1.5)

        # if the comment is long, parce it up 
        else: 
            #################take screenshot of the frame and first paragraph (kinda disgusting but it is what it is)##############
            driver.save_screenshot('{}/images/comment{}_0.png'.format(category, counter))
            time.sleep(1.5)
            base_image = Image.open('{}/images/comment{}_0.png'.format(category, counter))

            x1 = new_frames[counter].location['x'] * scale
            y1 = 48 * scale  #after scrolling the y1-location is on the top anyway
            x2 = (new_frames[counter].location['x'] + new_frames[counter].size['width']) * (scale + 0.05)
            y2 = 48 + header.size['height'] * 2 * scale + body[0].size['height'] * (scale + 0.1)

            box = (x1, y1, x2, y2)  

            cropped_image = base_image.crop(box)
            base_image = base_image.resize(cropped_image.size)
            base_image.paste(cropped_image, (0, 0))
            base_image.save('{}/images/comment{}_0.png'.format(category, counter))

            #append the texts of the comments 
            comment_text.append(body[0].text)
            #########################################################################################

            for i, para in enumerate(body[1:]): 
                driver.execute_script("window.scrollTo(0, {})".format(para.location['y']-48))         #scroll to paragraph

                time.sleep(0.4)
                para.screenshot('{}/images/comment{}_{}.png'.format(category, counter, i + 1))
                addMargin('{}/images/comment{}_{}.png'.format(category, counter, i + 1))
                
                #concatenate images if the paragraph length is too short 
                if i != 0 and len(para.text) <= 200:
                    im1 = Image.open('{}/images/comment{}_{}.png'.format(category, counter, i))
                    im2 = Image.open('{}/images/comment{}_{}.png'.format(category, counter, i + 1))
                    dst = Image.new("RGB", (im1.width, im1.height + im2.height))
                    dst.paste(im1, (0,0))
                    dst.paste(im2, (0, im1.height))
                    dst.save('{}/images/comment{}_{}.png'.format(category, counter, i+1))

                time.sleep(1.4)
    
                comment_text.append(para.text)

        counter += 1

def addMargin(path): 
    #crop the black margin based on the height of the image
    base_image = Image.open('concatenate.png')
    im2 = Image.open(path)

    height = im2.height
    width = 30 
    box = (0, 0, width, height)
    cropped_image = base_image.crop(box)
    base_image = base_image.resize(cropped_image.size)
    base_image.paste(cropped_image, (0, 0))

    #cropped black margin (im1 is the same thing as base_image but whatever)
    im1 = base_image

    #concatenate the images horizontally 
    #fill in the left margin
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    dst.save(path)

    #fill in the right margin 
    im2 = Image.open(path)
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im2, (0,0))
    dst.paste(im1, (im2.width, 0))
    dst.save(path)

def slow_typing(element, text): 
   for character in text: 
      element.send_keys(character)
      time.sleep(0.03)

def speechFiles(category): 
    language = 'en'

    #check if there is an existing directory for the category 
    dir = os.path.join("{}/tts".format(category))

    if os.path.exists(dir): 
        shutil.rmtree(dir) 
        
    os.mkdir(dir)

    #make an mp3 file for the title and convert to wav
    mytext = title_text[0]
    myobj = gtts.gTTS(text=mytext, lang = language, slow = False)
    myobj.save("{}/tts/1title.mp3".format(category))

    #convert to wav 
    sound = AudioSegment.from_mp3("{}/tts/1title.mp3".format(category))
    sound.export("{}/tts/1title.wav".format(category), format = 'wav')
    os.remove("{}/tts/1title.mp3".format(category))

    #make an mp3 file for the body of the post and convert to wav
    if body_text: 
        for i, text in enumerate(body_text): 
            mytext = text
            myobj = gtts.gTTS(text=mytext, lang = language, slow = False)
            myobj.save("{}/tts/body{}.mp3".format(category, i))

            #convert to wav 
            sound = AudioSegment.from_mp3("{}/tts/body{}.mp3".format(category, i))
            sound.export("{}/tts/body{}.wav".format(category, i), format = 'wav')
            os.remove("{}/tts/body{}.mp3".format(category, i))

    #make an mp3 file for the comment 
    for counter, text in enumerate(comment_text):
        mytext = text
        myobj = gtts.gTTS(text=mytext, lang = language, slow = False)
        myobj.save("{}/tts/comment{}.mp3".format(category, counter))

        #convert to wav
        sound = AudioSegment.from_mp3("{}/tts/comment{}.mp3".format(category, counter))
        sound.export("{}/tts/comment{}.wav".format(category, counter), format = 'wav')
        os.remove("{}/tts/comment{}.mp3".format(category, counter))

    #speed up all the wav files inside the existing directory
    for audiofile in os.scandir('{}/tts/'.format(category)):
        speedup.speedup(audiofile)
        
def logIn():            # Log In Function.
    try:
        login = driver.find_element(By.LINK_TEXT, 'Log In')
        login.click() 
        driver.switch_to.frame(driver.find_element(By.CLASS_NAME, "_25r3t_lrPF3M6zD2YkWvZU"))
        time.sleep(3)
        username_in = driver.find_element(By.ID, "loginUsername")

        slow_typing(username_in, username)

        pass_in = driver.find_element(By.ID, "loginPassword")

        slow_typing(pass_in, password)

        pass_in.send_keys(Keys.ENTER)
        time.sleep(1)

    except NoSuchElementException:
        print("bruh xd xd")

# Manual testing section 
# driver.get("https://www.reddit.com/r/AskReddit/comments/v6ozs3/serious_what_event_in_your_life_still_fucks_with/tack%20?depth=1")
# time.sleep(10)

if __name__ == "__main__":
    subreddits = [subreddit.strip('\n') for subreddit in open('subreddits.txt', 'r').readlines()]

    subreddit = subreddits[random.randint(0, len(subreddits))]
    rank = random.randint(0, 30)
    links = get_links(subreddit, category = 'top', timeframe = 'all', rank = rank)
    
    #get screenshots from the subreddit
    getScreenshots(links, subreddit, 6) 
    
    #generate the movie
    movie(subreddit)

    #post on tiktok
    tiktok(subreddit, rank) 

    #post on youtube 
    youtube(subreddit, rank)
