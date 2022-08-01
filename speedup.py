from pydub import AudioSegment
from pydub import AudioSegment
from pydub import playback

def speedup(path): 
    root = path 
    sound = AudioSegment.from_file(root)
    so = sound.speedup(1.3, 160, 25)
    so.export(path, format = 'wav')
