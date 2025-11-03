import os

file_path = 'E:\\PYTHON PROJECTS\\MusicPlayer_2.0\\Dependencies\\Test Songs\\Fearless.mp3'

if os.path.exists(file_path):
    print("File exists!")
else:
    print("File not found.")
