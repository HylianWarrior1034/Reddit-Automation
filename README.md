# Reddit-Automation

This is my Reddit Automation tool for webscraping, screenshotting, splicing, and editing a YouTube shorts-styled Reddit Videos. 
There are additional features that automate the posting of the created videos to YouTube/TikTok on command (with some caveats explained later at the bottom). 

This first edition of my program includes four main files: 
1. start.py -> the main program that webscrapes Reddit 
2. movie.py -> takes in the screenshots and creates the videos
3. speedup.py -> takes in the text-to-speech files and speeds it up by a factor of 30% (change this factor if you'd like) 
4. autopost.py -> uploads the videos onto YouTube and TikTok automatically with desired titles. 

# Getting Started 
Before getting started, there are two things 

# Future Fixes
First, the screenshots from the Selenium Webdriver gets wonky if the post contains an image or a video clip. (Besides, images/video clips wouldn't even suit
these types of videos. Still, it's an issue). 

Second, the text-to-speech file, which is created using the gtts Python module, has many inherent flaws. Maybe the next step is making my own tts code or 
using TikTok's tts feature? 

Lastly (perhaps the most important), 
