from moviepy.editor import *
import librosa 
import math
from PIL import Image
import random 

def movie(category):
    # the full pathnames of the audios and images within the category 
    audioclip = ['{}/tts/'.format(category) + audiofile.name for audiofile in os.scandir('{}/tts/'.format(category))]
    imageclip = ['{}/images/'.format(category)+ imagefile.name for imagefile in os.scandir('{}/images/'.format(category))]
    duration = [] 

    #find the length of the tts files and find out when to splice 
    for name in audioclip:
        length = librosa.get_duration(filename=name)

        #(since the video max length is 1 minute) break the clips when total length will exceed 60 seconds
        if sum(duration) + length > 60: 
            print(duration)
            print(sum(duration))
            break 
        
        duration.append(math.ceil(length))

    imageclip = imageclip[:len(duration)]
    audioclip = audioclip[:len(duration)]
    
    for image_path in imageclip: 
        base_image = Image.open(image_path)

        #I'm doing this cuz moviepy doesn't load the images properly if their image dimensions aren't even... WTF 
        if base_image.width%2 != 0: 
            box = (1, 0, base_image.width, base_image.height)  
        
            #crop the images based on the box 
            cropped_image = base_image.crop(box)
            base_image = base_image.resize(cropped_image.size)
            base_image.paste(cropped_image, (0, 0))
            base_image.save(image_path)

        if base_image.height%2 != 0: 
            box = (0, 1, base_image.width, base_image.height)  
    
            #crop the images based on the box 
            cropped_image = base_image.crop(box)
            base_image = base_image.resize(cropped_image.size)
            base_image.paste(cropped_image, (0, 0))
            base_image.save(image_path)

        #resize image so it fits on the background nicely 
        base_image.thumbnail([400, 512], Image.ANTIALIAS)
        base_image.save(image_path, "png")

    clips = [ImageClip(m).set_duration(duration[i]).set_audio(AudioFileClip(audioclip[i])) for i,m in enumerate(imageclip)]

    #load the background video (tf2) and trim it 
    path = 'backgroundvids/background{}.mp4'.format(random.randint(1,3))

    start_time = random.randint(20, 300)
    background = VideoFileClip(path).subclip(start_time, start_time + sum(duration))
    
    #combine the clips into one long clip and put it on top of the background videoclip
    final = CompositeVideoClip([background, concatenate_videoclips(clips, method = 'compose').set_position(('center', 140))])
    final.write_videofile("{}/{}.mp4".format(category, category), fps = 24)

if __name__ == '__main__':
    movie('AskReddit')
