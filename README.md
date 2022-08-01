# Reddit-Automation

This is my Reddit Automation tool for webscraping, screenshotting, splicing, and editing a YouTube shorts-styled Reddit Videos. 
There are additional features that automate the posting of the created videos to YouTube/TikTok on command (with some caveats explained later at the bottom). 

This first edition of my program includes four main files: 
1. start.py -> the main program that webscrapes Reddit based on randomized parameters
2. movie.py -> takes in the screenshots and creates the videos
3. speedup.py -> takes in the text-to-speech files and speeds it up by a factor of 30% (change this factor if you'd like) 
4. autopost.py -> uploads the videos onto YouTube and TikTok automatically with desired titles. 

# Getting Started 
Before getting started, there are two things you MUST do to use the basic features of this program: 
1. Input your Reddit USERNAME and PASSWORD on "start.py" line 25 and 26. This will automatically log you into the Reddit page, so all the settings presets are kept. 
2. Download the Chrome WebDriver from https://chromedriver.chromium.org/downloads and upload the path to the WebDriver on line 28 of the same .py file. 

With these two setups, the program should run automatically and create the videos. However, if you want to post on YouTube and Tiktok, follow the additional steps:
1. Download https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid?hl=en which is an extension for Google Chrome for
downloading cookies from a webpage. 
2. Go to YouTube and TikTok WHILE LOGGED INTO THE ACCOUNT YOU WISH TO UPLOAD THE VIDEOS TO, and use the cookie extension to download the cookie.txt file.
3. Go to https://wikizell.com/netscape-http-cookie-to-json-converter/ and convert the downloaded txt file into readable JSON file. Copy and paste the contents 
onto "youtube-cookies.json" and "tiktok-cookies.json" respectively.

# Additional Customizations 
Currently, the background video for the final videos is a clip from a game called Team Fortress 2. If you want to change to something else, put any .mp4 file 
into "backgroundvids" file. The .mp4 file must have an aspect ratio of 9:16 and have zero volume. Splicing the videos can be done easily through VLC media
if you don't have Adobe. 

You can also include more subreddits in the "subreddits.txt" files, just watch out for including subreddits that may include images/videos. As mentioned above, it 
can mess up the output. 

# Future Fixes
First, the screenshots from the Selenium Webdriver gets wonky if the post contains an image or a video clip. (Besides, images/video clips wouldn't even suit
these types of videos. Still, it's an issue). 

Second, the text-to-speech file, which is created using the gtts Python module, has many inherent flaws. Maybe the next step is making my own tts code or 
using TikTok's tts feature? 

Lastly (perhaps the most important), 
