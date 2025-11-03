# Inbuilt Modules
import datetime
import os
import glob
import time
from anyio import current_time
import win32api
import requests
import webbrowser
import urllib.parse
import urllib.request
import requests
# Installed Modules
import pathlib
from tkinter import *
import mysql.connector
from pygame import GL_CONTEXT_MAJOR_VERSION, mixer
from mutagen.mp3 import MP3
from bs4 import BeautifulSoup
from pydub import AudioSegment
from PIL import Image, ImageTk
from yt_dlp import YoutubeDL
from tkinter import ttk, messagebox
from win10toast import ToastNotifier
from tkinter import filedialog as fd
from pythumb import Thumbnail
from youtubesearchpython import VideosSearch

# Path of current directory
file_path = pathlib.Path(__file__).parent.resolve()

# Theme File
theme = open("Theme.txt", "r")

# PyGame Mixer Initiation
mixer.init()

# ComputerName
computer_name = win32api.GetComputerName()

paused = False
song_end = False
play = False
current_path = ""
current_name = ""
volume_set = 1

Dark = ""
Light = ""

if theme.read() == "Dark":
    Dark = True
    Light = False

else:
    Dark = False
    Light = True

topic, name_save, category1 = "", "", ""


song_list = []
name_list = []
thumbnail_list = []
thumbnailplay_list = []
category_list = []


est_time = 0
est_length = 0
current_time = 0

# Database Initiation
try:
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="harsh3304",
        database="MusicPlayer"
    )

except:
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="harsh3304"
    )

# Cursor Initiation
mycursor = mydatabase.cursor()

# Database Creation
try:
    mycursor.execute("CREATE DATABASE MusicPlayer")
    mycursor.execute("USE MusicPlayer")

except:
    pass

# Table Creation
try:
    table = "CREATE TABLE All_Songs(SONG_NAME VARCHAR(255),CATEGORY VARCHAR(8),SONG_PATH VARCHAR(255) ,THUMBNAIL VARCHAR(255),THUMBNAIL_PLAY VARCHAR(255))"
    mycursor.execute(table)

except:
    pass

# Folder Setup
list_of_files = os.listdir("./Dependencies//")
list_of_folder = ["DownloadedSongs", "Thumbnails", "ThumbnailsPlay"]

if "Dependencies" in os.listdir():
    for folder in list_of_folder:
        if folder not in list_of_files:
            os.makedirs("./Dependencies//" + folder)
        else:
            pass
else:
    os.makedirs('Dependencies')
    for folder in list_of_folder:
        os.makedirs("./Dependencies//" + folder)

main_window = Tk()
main_window.title("SoulSync")
main_window.geometry('1100x660')
main_window.maxsize(1100, 660)
main_window.minsize(1100, 660)

stop_btn = Button()
pause_btn = Button()
next_btn = Button()
previous_btn = Button()
volLabel = Button()
style1 = ttk.Style()
toaster = ToastNotifier()

# MainScreen ImagePaths
folder_location_main = str(file_path) + "\\Dependencies\\images\\MainScreen\\"
BG_location_main = folder_location_main + "BG.png"
AddSong_main = folder_location_main + "Add_Song.png"
AddFolder_main = folder_location_main + "Add_Folder.png"
GoOnline_main = folder_location_main + "GoOnline.png"
SongDisplay_BG_main = folder_location_main + "SongDisplay_BG.png"
AllSongs_main = folder_location_main + "AllSongs.png"
SleepCat_main = folder_location_main + "Sleep.png"
PartyCat_main = folder_location_main + "Party.png"
WorkoutCat_main = folder_location_main + "Workout.png"
LoveCat_main = folder_location_main + "Love.png"

# Dark MainScreen ImagePaths
dark_folder_location_main = str(file_path) + "\\Dependencies\\images\\MainScreen\\Dark\\"
Dark_BG_location_main = dark_folder_location_main + "Dark_HUD.png"
Dark_AddSong_main = dark_folder_location_main + "Dark_Add_Song.png"
Dark_AddFolder_main = dark_folder_location_main + "Dark_Add_From_Folder.png"
Dark_GoOnline_main = dark_folder_location_main + "Dark_GoOnline.png"
Dark_SongDisplay_BG_main = dark_folder_location_main + "Dark_Music_Label.png"
Dark_AllSongs_main = dark_folder_location_main + "Dark_All_Songs.png"
Dark_SleepCat_main = dark_folder_location_main + "Dark_Sleep.png"
Dark_PartyCat_main = dark_folder_location_main + "Dark_Party.png"
Dark_WorkoutCat_main = dark_folder_location_main + "Dark_Workout.png"
Dark_LoveCat_main = dark_folder_location_main + "Dark_Love.png"
Dark_Logo_main = dark_folder_location_main + "Dark_SoulSync_Logo.png"
Dark_Rect_main = dark_folder_location_main + "Dark_Rect.png"
Dark_Delete_main = dark_folder_location_main + "Dark_Delete.png"
Dark_Default_main = dark_folder_location_main + "Dark_Default.png"

# Light MainScreen ImagePaths
light_folder_location_main = str(file_path) + "\\Dependencies\\images\\MainScreen\\Light\\"
Light_BG_location_main = light_folder_location_main + "Light_HUD.png"
Light_AddSong_main = light_folder_location_main + "Light_Add_Song.png"
Light_AddFolder_main = light_folder_location_main + "Light_Add_From_Folder.png"
Light_GoOnline_main = light_folder_location_main + "Light_GoOnline.png"
Light_SongDisplay_BG_main = light_folder_location_main + "Light_Music_Label.png"
Light_AllSongs_main = light_folder_location_main + "Light_All_Songs.png"
Light_SleepCat_main = light_folder_location_main + "Light_Sleep.png"
Light_PartyCat_main = light_folder_location_main + "Light_Party.png"
Light_WorkoutCat_main = light_folder_location_main + "Light_Workout.png"
Light_LoveCat_main = light_folder_location_main + "Light_Love.png"
Light_Logo_main = light_folder_location_main + "Light_SoulSync_Logo.png"
Light_Rect_main = light_folder_location_main + "Light_Rect.png"
Light_Delete_main = light_folder_location_main + "Light_Delete.png"
Light_Default_main = light_folder_location_main + "Light_Default.png"

# HUD ImagePaths
folder_location_HUD = str(file_path) + "\\Dependencies\\images\\HUD\\"
Previous_location_HUD = folder_location_HUD + "Previous_Button.png"
Next_location_HUD = folder_location_HUD + "Next_Button.png"
Play_location_HUD = folder_location_HUD + "Play_Button.png"
Pause_location_HUD = folder_location_HUD + "Pause_Button.png"
Stop_location_HUD = folder_location_HUD + "Stop_Button.png"
FullVolume_location_HUD = folder_location_HUD + "Full_Volume.png"
MediumVolume_location_HUD = folder_location_HUD + "Medium_Volume.png"
LowVolume_location_HUD = folder_location_HUD + "Low_Volume.png"
MutedVolume_location_HUD = folder_location_HUD + "Muted_Volume.png"

# Dark HUD ImagePaths
Dark_folder_location_HUD = str(file_path) + "\\Dependencies\\images\\HUD\\Dark\\"
Dark_Previous_location_HUD = Dark_folder_location_HUD + "Dark_Previous_Button.png"
Dark_Next_location_HUD = Dark_folder_location_HUD + "Dark_Next_Button.png"
Dark_Play_location_HUD = Dark_folder_location_HUD + "Dark_Play_Button.png"
Dark_Pause_location_HUD = Dark_folder_location_HUD + "Dark_Pause_Button.png"
Dark_Stop_location_HUD = Dark_folder_location_HUD + "Dark_Stop_Button.png"
Dark_FullVolume_location_HUD = Dark_folder_location_HUD + "Dark_Full_Volume.png"
Dark_MediumVolume_location_HUD = Dark_folder_location_HUD + "Dark_Medium_Volume.png"
Dark_LowVolume_location_HUD = Dark_folder_location_HUD + "Dark_Low_Volume.png"
Dark_MutedVolume_location_HUD = Dark_folder_location_HUD + "Dark_Muted_Volume.png"

# Light HUD ImagePaths
Light_folder_location_HUD = str(file_path) + "\\Dependencies\\images\\HUD\\Light\\"
Light_Previous_location_HUD = Light_folder_location_HUD + "Light_Previous_Button.png"
Light_Next_location_HUD = Light_folder_location_HUD + "Light_Next_Button.png"
Light_Play_location_HUD = Light_folder_location_HUD + "Light_Play_Button.png"
Light_Pause_location_HUD = Light_folder_location_HUD + "Light_Pause_Button.png"
Light_Stop_location_HUD = Light_folder_location_HUD + "Light_Stop_Button.png"
Light_FullVolume_location_HUD = Light_folder_location_HUD + "Light_Full_Volume.png"
Light_MediumVolume_location_HUD = Light_folder_location_HUD + "Light_Medium_Volume.png"
Light_LowVolume_location_HUD = Light_folder_location_HUD + "Light_Low_Volume.png"
Light_MutedVolume_location_HUD = Light_folder_location_HUD + "Light_Muted_Volume.png"

# BG_Images_Dark
dark_folder_location_images = str(file_path) + "\\Dependencies\\images\\MainScreen\\Dark\\"
All_songs_Dark_image = dark_folder_location_images + "All_Songs_Dark.png"
Love_Dark_image = dark_folder_location_images + "Love_Dark.png"
Workout_Dark_image = dark_folder_location_images + "Workout_Dark.png"
Party_Dark_image = dark_folder_location_images + "Party_Dark.png"
Sleep_Dark_image = dark_folder_location_images + "Sleep_Dark.png"

# BG_Images_Light
light_folder_location_images = str(file_path) + "\\Dependencies\\images\\MainScreen\\Light\\"
All_songs_Light_image = light_folder_location_images + "All_Songs_Light.png"
Love_Light_image = light_folder_location_images + "Love_Light.png"
Workout_Light_image = light_folder_location_images + "Workout_Light.png"
Party_Light_image = light_folder_location_images + "Party_Light.png"
Sleep_Light_image = light_folder_location_images + "Sleep_Light.png"

# MainScreen ImageLoading
if Light:
    BG = PhotoImage(file=Light_BG_location_main)
    Add_Song = PhotoImage(file=Light_AddSong_main)
    Add_from_Folder = PhotoImage(file=Light_AddFolder_main)
    Go_Online = PhotoImage(file=Light_GoOnline_main)
    ML = PhotoImage(file=Light_SongDisplay_BG_main)
    All_Songs = PhotoImage(file=Light_AllSongs_main)
    Sleep = PhotoImage(file=Light_SleepCat_main)
    Workout = PhotoImage(file=Light_WorkoutCat_main)
    Love = PhotoImage(file=Light_LoveCat_main)
    Party = PhotoImage(file=Light_PartyCat_main)
    IMG_BG = PhotoImage(file=Light_Rect_main)
    Logo = PhotoImage(file=Light_Logo_main)
    Delete = PhotoImage(file=Light_Delete_main)
    Default = PhotoImage(file=Light_Default_main)

else:
    BG = PhotoImage(file=Dark_BG_location_main)
    Add_Song = PhotoImage(file=Dark_AddSong_main)
    Add_from_Folder = PhotoImage(file=Dark_AddFolder_main)
    Go_Online = PhotoImage(file=Dark_GoOnline_main)
    ML = PhotoImage(file=Dark_SongDisplay_BG_main)
    All_Songs = PhotoImage(file=Dark_AllSongs_main)
    Sleep = PhotoImage(file=Dark_SleepCat_main)
    Workout = PhotoImage(file=Dark_WorkoutCat_main)
    Love = PhotoImage(file=Dark_LoveCat_main)
    Party = PhotoImage(file=Dark_PartyCat_main)
    IMG_BG = PhotoImage(file=Dark_Rect_main)
    Logo = PhotoImage(file=Dark_Logo_main)
    Delete = PhotoImage(file=Dark_Delete_main)
    Default = PhotoImage(file=Dark_Default_main)

# Dark MainScreen ImageLoading
Dark_BG = PhotoImage(file=Dark_BG_location_main)
Dark_Add_Song = PhotoImage(file=Dark_AddSong_main)
Dark_Add_from_Folder = PhotoImage(file=Dark_AddFolder_main)
Dark_Go_Online = PhotoImage(file=Dark_GoOnline_main)
Dark_ML = PhotoImage(file=Dark_SongDisplay_BG_main)
Dark_All_Songs = PhotoImage(file=Dark_AllSongs_main)
Dark_Sleep = PhotoImage(file=Dark_SleepCat_main)
Dark_Workout = PhotoImage(file=Dark_WorkoutCat_main)
Dark_Love = PhotoImage(file=Dark_LoveCat_main)
Dark_Party = PhotoImage(file=Dark_PartyCat_main)
Dark_IMG_BG = PhotoImage(file=Dark_Rect_main)
Dark_Logo = PhotoImage(file=Dark_Logo_main)
Dark_Delete = PhotoImage(file=Dark_Delete_main)
Dark_Default = PhotoImage(file=Dark_Default_main)

# Light MainScreen ImageLoading
Light_BG = PhotoImage(file=Light_BG_location_main)
Light_Add_Song = PhotoImage(file=Light_AddSong_main)
Light_Add_from_Folder = PhotoImage(file=Light_AddFolder_main)
Light_Go_Online = PhotoImage(file=Light_GoOnline_main)
Light_ML = PhotoImage(file=Light_SongDisplay_BG_main)
Light_All_Songs = PhotoImage(file=Light_AllSongs_main)
Light_Sleep = PhotoImage(file=Light_SleepCat_main)
Light_Workout = PhotoImage(file=Light_WorkoutCat_main)
Light_Love = PhotoImage(file=Light_LoveCat_main)
Light_Party = PhotoImage(file=Light_PartyCat_main)
Light_IMG_BG = PhotoImage(file=Light_Rect_main)
Light_Logo = PhotoImage(file=Light_Logo_main)
Light_Delete = PhotoImage(file=Light_Delete_main)
Light_Default = PhotoImage(file=Light_Default_main)

# HUD ImageLoading
if Light:
    Play = PhotoImage(file=Light_Play_location_HUD)
    Pause = PhotoImage(file=Light_Pause_location_HUD)
    Stop = PhotoImage(file=Light_Stop_location_HUD)
    Next = PhotoImage(file=Light_Next_location_HUD)
    Previous = PhotoImage(file=Light_Previous_location_HUD)
    HighVol = PhotoImage(file=Light_FullVolume_location_HUD)
    MediumVol = PhotoImage(file=Light_MediumVolume_location_HUD)
    LowVol = PhotoImage(file=Light_LowVolume_location_HUD)
    Mute = PhotoImage(file=Light_MutedVolume_location_HUD)
else:
    Play = PhotoImage(file=Dark_Play_location_HUD)
    Pause = PhotoImage(file=Dark_Pause_location_HUD)
    Stop = PhotoImage(file=Dark_Stop_location_HUD)
    Next = PhotoImage(file=Dark_Next_location_HUD)
    Previous = PhotoImage(file=Dark_Previous_location_HUD)
    HighVol = PhotoImage(file=Dark_FullVolume_location_HUD)
    MediumVol = PhotoImage(file=Dark_MediumVolume_location_HUD)
    LowVol = PhotoImage(file=Dark_LowVolume_location_HUD)
    Mute = PhotoImage(file=Dark_MutedVolume_location_HUD)

Dark_Play = PhotoImage(file=Dark_Play_location_HUD)
Dark_Pause = PhotoImage(file=Dark_Pause_location_HUD)
Dark_Stop = PhotoImage(file=Dark_Stop_location_HUD)
Dark_Next = PhotoImage(file=Dark_Next_location_HUD)
Dark_Previous = PhotoImage(file=Dark_Previous_location_HUD)
Dark_HighVol = PhotoImage(file=Dark_FullVolume_location_HUD)
Dark_MediumVol = PhotoImage(file=Dark_MediumVolume_location_HUD)
Dark_LowVol = PhotoImage(file=Dark_LowVolume_location_HUD)
Dark_Mute = PhotoImage(file=Dark_MutedVolume_location_HUD)

Light_Play = PhotoImage(file=Light_Play_location_HUD)
Light_Pause = PhotoImage(file=Light_Pause_location_HUD)
Light_Stop = PhotoImage(file=Light_Stop_location_HUD)
Light_Next = PhotoImage(file=Light_Next_location_HUD)
Light_Previous = PhotoImage(file=Light_Previous_location_HUD)
Light_HighVol = PhotoImage(file=Light_FullVolume_location_HUD)
Light_MediumVol = PhotoImage(file=Light_MediumVolume_location_HUD)
Light_LowVol = PhotoImage(file=Light_LowVolume_location_HUD)
Light_Mute = PhotoImage(file=Light_MutedVolume_location_HUD)

# BG ImageLoading Dark
All_Song_Dark = PhotoImage(file=All_songs_Dark_image)
Love_Dark = PhotoImage(file=Love_Dark_image)
Party_Dark = PhotoImage(file=Party_Dark_image)
Workout_Dark = PhotoImage(file=Workout_Dark_image)
Sleep_Dark = PhotoImage(file=Sleep_Dark_image)

# BG ImageLoading Light
All_Song_Light = PhotoImage(file=All_songs_Light_image)
Love_Light = PhotoImage(file=Love_Light_image)
Party_Light = PhotoImage(file=Party_Light_image)
Workout_Light = PhotoImage(file=Workout_Light_image)
Sleep_Light = PhotoImage(file=Sleep_Light_image)


def downloadImage(query, fileLocation, name, n):
    URL = "https://www.google.com/search?tbm=isch&q=" + query + " song cover"
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')
    print(soup)
    imgTags = soup.find_all('img', class_='DS1iW')
    print(imgTags)

    count = 0
    for i in imgTags:
        if count == n: break

        try:
            urllib.request.urlretrieve(i['src'], f'{fileLocation}' + str(name + "_raw") + '.png')
            count += 1
        except Exception as e:
            raise e

def reset():
    global play
    play = False
    mixer.music.stop()
    NameLabel.config(text=" ")
    song_current_time.config(text="", foreground="grey1")
    song_total_time.config(text="")

    NameLabel2.config(text="", foreground="turquoise4")
    ImageLabel.config(image="")

    volLabel.destroy()
    previous_btn.destroy()
    next_btn.destroy()
    pause_btn.destroy()
    volume_slider.destroy()
    stop_btn.destroy()
    song_slider.destroy()


def song_current_info():
    global play
    global est_time
    global name_list
    global current_name
    global Light
    global song_slider

    try:
        current_time = mixer.music.get_pos() / 1000
        est_time = round(current_time, 1)
        est_time += 0.5
        cur_index = name_list.index(current_name)
        list_len = int(len(name_list)) - 1
        if est_time >= est_length:
            if cur_index == list_len:
                reset()
            else:
                previous_song()

        if Light:
            color = "#f16c83"
        else:
            color = "#014964"
        if play:
            time_format = time.strftime('%M:%S', time.gmtime(current_time))
            song_current_time.config(text=time_format, foreground=color)
            song_slider.config(value=current_time)

            song_current_time.after(1000, song_current_info)

        else:
            pass

    except:
        pass


def song_slide(*args):
    song_current_info()


def go_online():
    download_window = Toplevel()
    download_window.maxsize(370, 430)
    download_window.minsize(370, 430)
    download_window.geometry("370x430")
    download_window.title("Go Online")

    theme = open("Theme.txt", "r")
    theme_current = theme.read()
    theme.close()

    # GoOnline ImagePaths
    folder_location_online = str(file_path) + "\\Dependencies\\images\\GoOnline\\" + theme_current + "\\" + theme_current
    Submit_online = folder_location_online + "_Submit.png"
    DownloadButton_online = folder_location_online + "_Download.png"
    CancelButton_online = folder_location_online + "_Cancel.png"
    CancelButton2_online = folder_location_online + "_Cancel_Main.png"
    GoSite_Button_online = folder_location_online + "_Go_To_Site.png"
    BG_1_online = folder_location_online + "_GoOnline_Main.png"
    BG_Link_online = folder_location_online + "_Link_Download.png"
    BG_2_online = folder_location_online + "_GoOnline.png"

    ProvideLink_Button_online = str(file_path) + "\\Dependencies\\images\\GoOnline\\Provide_Link.png"

    # GoOnline ImageLoading
    Submit_button = PhotoImage(file=Submit_online)
    Go_To_Site_button = PhotoImage(file=GoSite_Button_online)
    Download_button = PhotoImage(file=DownloadButton_online)
    Provide_Link_button = PhotoImage(file=ProvideLink_Button_online)
    Cancel_button = PhotoImage(file=CancelButton_online)
    Cancel_button2 = PhotoImage(file=CancelButton2_online)
    BG_1 = PhotoImage(file=BG_1_online)
    BG_Link = PhotoImage(file=BG_Link_online)
    BG_2 = PhotoImage(file=BG_2_online)

    def goPage():
        """This function takes the user to the webpage of the song"""
        global topic
        if topic == "":
            messagebox.showerror("Use brain please", "Required field detected empty")
            download_window.destroy()
            os.system("Download.py")
        else:
            search_title = topic
            video_search = VideosSearch(search_title, limit=1)
            result = video_search.result()
            link = result["result"][0]['link']
            webbrowser.open(link)

    def cancel():
        main_screen("None")
        download_window.destroy()

    def screen2():
        global topic
        global temp
        global name_save
        global category1

        topic = topicEntryBox.get()

        if topic == "":
            messagebox.showerror("Use brain please", "Required field detected empty")
            download_window.destroy()
            go_online()

        else:
            name_save = nameSaveEntry.get()

            if CategoryEntryBox1.get() == "" or CategoryEntryBox1.get() == "Party/Love/Workout/Sleep":
                category1 = "None"

            elif CategoryEntryBox1.get() == "Sleep" or CategoryEntryBox1.get() == "sleep":
                category1 = "Sleep"

            elif CategoryEntryBox1.get() == "Love" or CategoryEntryBox1.get() == "love":
                category1 = "Love"

            elif CategoryEntryBox1.get() == "None" or CategoryEntryBox1.get() == "none":
                category1 = "None"

            elif CategoryEntryBox1.get() == "Workout" or CategoryEntryBox1.get() == "workout":
                category1 = "Workout"

            elif CategoryEntryBox1.get() == "Party" or CategoryEntryBox1.get() == "party":
                category1 = "Party"

            else:
                category1 = "None"

            BG_label.config(image=BG_2)

            try:
                os.remove("thumb.png")
            except:
                pass
            video_search = VideosSearch(topic, limit=1)
            result = video_search.result()

            link = result["result"][0]['link']
            id = result["result"][0]['id']

            thumb = Thumbnail(link)
            thumb.fetch('mqdefault')
            thumb.save("")

            temp_id = id+".jpg"
            os.rename(temp_id, "thumb.png")
        
            temp = ImageTk.PhotoImage(Image.open("thumb.png"))
            thumbnail = Label(download_window, image=temp)
            thumbnail.place(x=26, y=20)


            topicEntryBox.destroy()
            nameSaveEntry.destroy()
            Submit_but.destroy()
            Provide_Link_bt.destroy()
            Cancel_but.destroy()
            CategoryEntryBox1.destroy()

            Go_to_site_bt = Button(download_window, image=Go_To_Site_button, border=0, bg="#020113", activebackground="#020113",
                                   command=goPage)
            Go_to_site_bt.place(x=51, y=234)

            Download_bt = Button(download_window, image=Download_button, border=0, bg="#020113", activebackground="#020113",
                                 command=download)
            Download_bt.place(x=51, y=284)

            Cancel_bt = Button(download_window, image=Cancel_button2, border=0, bg="#020113", activebackground="#020113",
                               command=cancel)
            Cancel_bt.place(x=51, y=334)

            if Light:
                Go_to_site_bt.config(bg="#1C2238", activebackground="#1C2238")
                Download_bt.config(bg="#1C2238", activebackground="#1C2238")
                Cancel_bt.config(bg="#1C2238", activebackground="#1C2238")

    def download():
        global topic
        global name_save
        global category1

        try:
            os.remove("thumb.png")
        except:
            pass

        category = category1.replace(" ", "")

        messagebox.showinfo("Sorry for trouble :(", "You will get message once download is complete")

        download_window.title("Download-Go Online")

        video_search = VideosSearch(topic, limit=1)
        result = video_search.result()

        title = result["result"][0]['title']
        link = result["result"][0]['link']
    

        if name_save == "":
            name_save = title
        else:
            name_save = name_save

        length = len(name_save)

        if length > 25:
            name_to_save = name_save[:26]
        else:
            name_to_save = name_save

        search_query = name_to_save

        to_download = str(file_path) + "\\Dependencies\\Thumbnails\\"

        downloadImage(name_to_save, to_download, name_to_save,5)

        image_to_resize = os.path.join(file_path, "Dependencies", "Thumbnails", f"{search_query}_raw.png")
        
        resize_path = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(search_query) + "_thumbnail.png"
        save_path = str(file_path) + "\\Dependencies\\ThumbnailsPlay\\" + str(search_query) + "_thumbnailplay.png"

        imge = Image.open(image_to_resize)
        crop_image = imge.resize((40, 40))
        crop_image.save(resize_path)

        see_contact_img = imge.resize((80, 80))
        see_contact_img.save(save_path)
        os.remove(image_to_resize)
        #os.remove("music.png")

        audio_downloder = YoutubeDL({'format': 'bestaudio/audio', 'codec': 'wav',
                                     'preferredquality': '192', 'noplaylist': True,
                                     'outtmpl': name_to_save + '.%(ext)s'})

        audio_downloder.extract_info(link)

        list_of_files = os.listdir()

        if name_to_save + ".webm" in list_of_files:
            target = name_to_save + ".webm"

        else:
            target = name_to_save + ".m4a"

        wav_audio = AudioSegment.from_file(target)
        os.remove(target)
        song_download = str(file_path) + "\\Dependencies\\DownloadedSongs\\" + name_to_save + ".mp3"
        wav_audio.export(song_download, format="mp3")

        thumbnail_path = resize_path
        thumbnail_play = save_path
        filename = song_download

        Formula = "INSERT INTO All_Songs (SONG_NAME,CATEGORY,SONG_PATH,THUMBNAIL, THUMBNAIL_PLAY) VALUES(%s, %s, %s, %s, %s)"
        song_save = (name_to_save, category, filename, thumbnail_path, thumbnail_play)

        mycursor.execute(Formula, song_save)
        mydatabase.commit()

        toaster.show_toast("Done :)", "Your songs have been successfully added to SoulSync", threaded=True,
                           duration=15)

        cancel()
        messagebox.showinfo("Finally", "Download Complete\nYou will now be redirected to main screen")

    def link_download():
        topicEntryBox.destroy()
        Submit_but.destroy()
        Provide_Link_bt.destroy()
        CategoryEntryBox1.destroy()
        Cancel_but.destroy()
        nameSaveEntry.destroy()

        BG_label.config(image=BG_Link)

        download_window.title("Link Download-Go Online")

        def screen3():
            global name
            global temp
            global link2
            global category1

            link = linkEntry.get()
            link2 = link

            if link2 == "" or link2 == " ":
                messagebox.showerror("U crazy?", "Link missing")
                download_window.destroy()
                go_online()
            else:
                name_save2 = nameSaveEntry2.get()
                name = name_save2

                if CategoryEntry.get() == "" or CategoryEntry.get() == "Party/Love/Workout/Sleep":
                    category1 = "None"

                elif CategoryEntry.get() == "Sleep" or CategoryEntry.get() == "sleep":
                    category1 = "Sleep"

                elif CategoryEntry.get() == "Love" or CategoryEntry.get() == "love":
                    category1 = "Love"

                elif CategoryEntry.get() == "None" or CategoryEntry.get() == "none":
                    category1 = "None"

                elif CategoryEntry.get() == "Workout" or CategoryEntry.get() == "workout":
                    category1 = "Workout"

                elif CategoryEntry.get() == "Party" or CategoryEntry.get() == "party":
                    category1 = "Party"

                else:
                    category1 = "None"

                BG_label.config(image=BG_2)

                try:
                    os.remove("thumb.png")
                except:
                    pass

                temp_id = urllib.parse.urlparse(link2)

                id = temp_id[4]

                thumb = Thumbnail(link)
                thumb.fetch('mqdefault')
                thumb.save("")
                
                try:
                    temp_id2 = id.replace("v=", "") + ".jpg"
                except:
                    temp_id2 = id
        
                os.rename(temp_id2, "thumb.png")
            
                temp = ImageTk.PhotoImage(Image.open("thumb.png"))
                thumbnail = Label(download_window, image=temp)
                thumbnail.place(x=26, y=20)

                linkEntry.destroy()
                Submit_bt.destroy()
                CategoryEntry.destroy()
                Cancel_but3.destroy()
                nameSaveEntry2.destroy()

                Download_bt = Button(download_window, image=Download_button, border=0, bg="#020113", activebackground="#020113",
                                     command=download_link)
                Download_bt.place(x=51, y=240)

                Cancel_bt = Button(download_window, image=Cancel_button2, border=0, bg="#020113", activebackground="#020113",
                                   command=cancel)
                Cancel_bt.place(x=51, y=295)
                
                if Light:
                    Download_bt.config(bg="#1C2238", activebackground="#1C2238")
                    Cancel_bt.config(bg="#1C2238", activebackground="#1C2238")

        def download_link():
            global link2
            global name
            global category1

            try:
                os.remove("thumb.png")
            except:
                pass

            messagebox.showinfo("Sorry for Trouble :(", "You will get message when your download is complete.")

            length = len(name)

            if length > 25:
                name_to_save = name[:26]
            else:
                name_to_save = name

            category = category1.replace(" ", "")

            audio_downloder = YoutubeDL({'format': 'bestaudio/audio', 'codec': 'wav',
                                         'preferredquality': '192', 'noplaylist': True,
                                         'outtmpl': name_to_save + '.%(ext)s'})

            audio_downloder.extract_info(link2)

            list_of_files = os.listdir()

            if name_to_save + ".webm" in list_of_files:
                target = name_to_save + ".webm"

            else:
                target = name_to_save + ".m4a"

            wav_audio = AudioSegment.from_file(target)
            song_download = str(file_path) + "\\Dependencies\\DownloadedSongs\\" + name_to_save + ".mp3"
            wav_audio.export(song_download, format="mp3")
            os.remove(target)

            search_query = name_to_save

            to_download = str(file_path) + "\\Dependencies\\Thumbnails\\"
            downloadImage(name_to_save, to_download, name_to_save,5)

            image_to_resize = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(search_query) + "_raw.png"
            resize_path = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(search_query) + "_thumbnail.png"
            save_path = str(file_path) + "\\Dependencies\\ThumbnailsPlay\\" + str(
                search_query) + "_thumbnailplay.png"

            imge = Image.open(image_to_resize)
            crop_image = imge.resize((40, 40))
            crop_image.save(resize_path)

            see_contact_img = imge.resize((80, 80))
            see_contact_img.save(save_path)

            os.remove(image_to_resize)

            thumbnail_path = resize_path
            thumbnail_play = save_path
            filename = song_download

            Formula = "INSERT INTO All_Songs (SONG_NAME,CATEGORY,SONG_PATH,THUMBNAIL, THUMBNAIL_PLAY) VALUES(%s, %s, %s, %s, %s)"
            song_save = (name_to_save, category, filename, thumbnail_path, thumbnail_play)

            mycursor.execute(Formula, song_save)
            mydatabase.commit()

            toaster.show_toast("Done :)", "Your songs have been successfully added to SoulSync", threaded=True,
                               duration=15)

            cancel()
            messagebox.showinfo("Finally :)", "Download Complete!\nYou will now be redirected to MainScreen.")


        def catentrydel(*args):
            """Function to clear CategoryEntryBox on click on EntryBox"""
            CategoryEntry.delete(0, END)

        linkEntry = Entry(download_window, width="22", bd=0, bg="#015E88", fg="#bbbcbb",
                          font=("Bahnschrift SemiDark Condensed", 19))
        linkEntry.place(x=23, y=128)

        nameSaveEntry2 = Entry(download_window, width="22", bd=0, bg="#015E88", fg="#bbbcbb",
                               font=("Bahnschrift SemiDark Condensed", 19))
        nameSaveEntry2.place(x=23, y=215)


        CategoryEntry = Entry(download_window, width="22", bd=0, bg="#015E88", fg="#bbbcbb",
                              font=("Bahnschrift SemiDark Condensed", 19))
        CategoryEntry.place(x=23, y=300)
        CategoryEntry.insert(END, "Party/Love/Workout/Sleep")
        CategoryEntry.bind("<Button-1>", catentrydel)

        Submit_bt = Button(download_window, image=Submit_button, border=0, bg="#020113", activebackground="#020113",
                           command=screen3)
        Submit_bt.place(x=58, y=362)
        Cancel_but3 = Button(download_window, image=Cancel_button, border=0, bg="#020113", activebackground="#020113",
                             command=cancel)
        Cancel_but3.place(x=205, y=362)

        if Light:
            nameSaveEntry2.config(bg="#8E495D", fg="#1C1F32")
            linkEntry.config(bg="#8E495D", fg="#1C1F32")
            CategoryEntry.config(bg="#8E495D", fg="#1C1F32")
            Submit_bt.config(bg="#8E495D", activebackground="#1C1F32")
            Cancel_but3.config(bg="#8E495D", activebackground="#1C1F32")

    def catentrydel(*args):
        """Function to clear CategoryEntryBox on click on EntryBox"""
        CategoryEntryBox1.delete(0, END)

    BG_label = Label(download_window, image=BG_1, border=0)
    BG_label.place(x=0, y=0)

    topicEntryBox = Entry(download_window, relief=FLAT, width="22", bg="#015E88", fg="#bbbcbb",
                          font=("Bahnschrift SemiDark Condensed", 19))
    topicEntryBox.place(x=23, y=128)

    nameSaveEntry = Entry(download_window, relief=FLAT, width="22", bg="#015E88", fg="#bbbcbb",
                          font=("Bahnschrift SemiDark Condensed", 19))
    nameSaveEntry.place(x=23, y=215)

    CategoryEntryBox1 = Entry(download_window, relief=FLAT, width="22", bg="#015E88", fg="#bbbcbb",
                              font=("Bahnschrift SemiDark Condensed", 19))
    CategoryEntryBox1.place(x=23, y=300)
    CategoryEntryBox1.insert(END, "Party/Love/Workout/Sleep")
    CategoryEntryBox1.bind("<Button-1>", catentrydel)

    Submit_but = Button(download_window, image=Submit_button, border=0, bg="#020113", activebackground="#020113",
                        command=screen2)
    Submit_but.place(x=58, y=362)

    Cancel_but = Button(download_window, image=Cancel_button, border=0, bg="#020113", activebackground="#020113",
                        command=cancel)
    Cancel_but.place(x=205, y=362)

    Provide_Link_bt = Button(download_window, image=Provide_Link_button, border=0, bg="gray1", activebackground="gray1",
                             command=link_download)
    Provide_Link_bt.place(x=98, y=398)

    if Light:
        topicEntryBox.config(bg="#8E495D")
        nameSaveEntry.config(bg="#8E495D")
        CategoryEntryBox1.config(bg="#8E495D")
        Submit_but.config(bg="#8E495D", activebackground="#1C1F32")
        Cancel_but.config(bg="#8E495D", activebackground="#1C1F32")
        Provide_Link_bt.config(bg="#1C1F32", activebackground="#1C1F32")

    mainloop()


def add_song():
    # GUI Window Initiation
    addwindow = Toplevel()
    addwindow.maxsize(370, 430)
    addwindow.minsize(370, 430)
    addwindow.geometry("370x430")
    addwindow.title("Add Song")

    theme = open("Theme.txt", "r")
    theme_current = theme.read()
    theme.close()

    # AddSongs ImagePaths
    folder_location_add = str(file_path) + "\\Dependencies\\images\\AddSong\\" + theme_current + "\\"
    BG_location_add = folder_location_add + theme_current + "_Add_Song.png"
    SubmitButton_location_add = folder_location_add + theme_current + "_Submit.png"
    CancelButton_location_add = folder_location_add + theme_current + "_Cancel.png"

    # AddSongs ImageLoading
    BG2 = PhotoImage(file=BG_location_add)
    Submit_button = PhotoImage(file=SubmitButton_location_add)
    Cancel_button = PhotoImage(file=CancelButton_location_add)

    BG_label = Label(addwindow, image=BG2, border=0)
    BG_label.place(x=0, y=0)

    def submit_add():
        """This is function which will run when submit button is clicked"""
        nameEntryget = NameEntryBox.get()
        name_of_song1 = nameEntryget

        inital_dir = "C:\\Users\\" + computer_name + "\\Music"

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir=inital_dir,
            filetypes=[("Songs", ".mp3")])

        if filename == "":
            messagebox.showerror("U crazy?", "Please select a song next time")
            addwindow.destroy()
        else:
            search_query_name = os.path.basename(filename)
            search_query_split = search_query_name.split(".")
            search_query = search_query_split[0]
            to_download = str(file_path) + "\\Dependencies\\Thumbnails\\"

            if name_of_song1 == "":
                name_of_song1 = search_query
            else:
                pass

            length = len(name_of_song1)

            if length > 25:
                name_of_song = name_of_song1[:26]
            else:
                name_of_song = name_of_song1

            categoryEntryget1 = categoryEntryBox.get()
            categoryEntryget = categoryEntryget1.replace(" ", "")

            if categoryEntryget == "" or categoryEntryget == "Party/Love/Workout/Sleep":
                category = "None"

            elif categoryEntryget == "Sleep" or categoryEntryget == "sleep":
                category = "Sleep"

            elif categoryEntryget == "Love" or categoryEntryget == "love":
                category = "Love"

            elif categoryEntryget == "None" or categoryEntryget == "none":
                category = "None"

            elif categoryEntryget == "Workout" or categoryEntryget == "workout":
                category = "Workout"

            elif categoryEntryget == "Party" or categoryEntryget == "party":
                category = "Party"

            else:
                category = "None"

            downloadImage(name_of_song, to_download, search_query,5)

            image_to_resize = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(search_query) + "_raw.png"
            resize_path = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(search_query) + "_thumbnail.png"
            save_path = str(file_path) + "\\Dependencies\\ThumbnailsPlay\\" + str(search_query) + "_thumbnailplay.png"

            imge = Image.open(image_to_resize)
            crop_image = imge.resize((40, 40))
            crop_image.save(resize_path)

            imge2 = Image.open(image_to_resize)
            see_contact_img = imge2.resize((80, 80))
            see_contact_img.save(save_path)

            os.remove(image_to_resize)

            thumbnail_path = resize_path
            thumbnail_play = save_path

            Formula = "INSERT INTO All_Songs (SONG_NAME,CATEGORY,SONG_PATH,THUMBNAIL, THUMBNAIL_PLAY) VALUES(%s, %s, %s, %s, %s)"
            song_save = (name_of_song, category, filename, thumbnail_path, thumbnail_play)

            mycursor.execute(Formula, song_save)
            mydatabase.commit()
            all_song()
            addwindow.destroy()

    def catentrydel(*args):
        """Function to clear CategoryEntryBox on click on EntryBox"""
        categoryEntryBox.delete(0, END)
        return None
    
    if Light:
        color = "#8f475d"
    else:
        color = "#015E88"

    # Main code
    NameEntryBox = Entry(addwindow, relief=FLAT, width="22", bg=color, fg="#bbbcbb",
                         font=("Bahnschrift SemiDark Condensed", 19))
    NameEntryBox.place(x=23, y=128)

    categoryEntryBox = Entry(addwindow, relief=FLAT, width="22", bg=color, fg="#bbbcbb",
                             font=("Bahnschrift SemiDark Condensed", 19))
    categoryEntryBox.place(x=23, y=215)
    categoryEntryBox.insert(END, "Party/Love/Workout/Sleep")
    categoryEntryBox.bind("<Button-1>", catentrydel)

    submitButton = Button(addwindow, image=Submit_button, activebackground="gray1", border=0, bg="gray1",
                          command=submit_add)
    submitButton.place(x=58, y=362)

    cancelbutton = Button(addwindow, image=Cancel_button, border=0, activebackground="gray1", bg="gray1",
                          command=addwindow.destroy)
    cancelbutton.place(x=205, y=362)

    mainloop()


def add_folder():
    global song_list
    global name_list
    global thumbnail_list

    initial_dir = "C:\\Users\\" + computer_name + "\\Music"

    folder_path = fd.askdirectory(title='Select a Folder', initialdir=initial_dir)

    if folder_path == "":
        messagebox.showerror("U crazy?", "Please select a folder next time")
    else:
        targetPattern = str(folder_path) + "/*.mp3"
        songs = glob.glob(targetPattern)

        name_tosave_list = []
        path_tosave_list = []

        messagebox.showwarning("Sorry for Trouble",
                               "The program might freeze from some seconds just wait for it to get normal. You will receive a message when songs are added to Player")
        for s in songs:
            to_name = s.split("\\")
            raw_name = to_name[-1]
            raw_save = raw_name.split(".")
            to_save = raw_save[0]
            path = folder_path + "/" + str(raw_name)
            path_tosave_list.append(path)
            name_tosave_list.append(to_save)

        category = "None"

        to_download = str(file_path) + "\\Dependencies\\Thumbnails\\"
        for (name_of_song1, filename) in zip(name_tosave_list, path_tosave_list):
            length = len(name_of_song1)
            if length > 25:
                name_of_song = name_of_song1[:26]
            else:
                name_of_song = name_of_song1

            downloadImage(name_of_song1, to_download, name_of_song, 5)

            image_to_resize = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(name_of_song) + "_raw.png"
            resize_path = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(name_of_song) + "_thumbnail.png"
            save_path = str(file_path) + "\\Dependencies\\ThumbnailsPlay\\" + str(name_of_song) + "_thumbnailplay.png"

            imge = Image.open(image_to_resize)
            crop_image = imge.resize((50, 50))
            crop_image.save(resize_path)

            see_contact_img = imge.resize((120, 120))
            see_contact_img.save(save_path)

            os.remove(image_to_resize)

            thumbnail_path = resize_path
            thumbnail_play = save_path

            Formula = "INSERT INTO All_Songs (SONG_NAME,CATEGORY,SONG_PATH,THUMBNAIL, THUMBNAIL_PLAY) VALUES(%s, %s, %s, %s, %s)"
            song_save = ((name_of_song, category, filename, thumbnail_path, thumbnail_play))

            mycursor.execute(Formula, song_save)
            mydatabase.commit()

        toaster = ToastNotifier()
        toaster.show_toast("Done :)", "Your songs have been successfully added to SoulSync", threaded=True, duration=15)
        all_song()
        messagebox.showinfo("Thenks for waiting", "Songs have been added successfully.")


def rewind(song_path, song_name, category, thumbnail_play):
    global play
    global song_slider
    global est_time
    global current_time

    reset()
    play_music(song_path, song_name, category, thumbnail_play)
    

def play_music(song_path, song_name, category, thumbnail_play):
    global current_path
    global current_name
    global volume_set
    global est_length
    global est_time
    global play
    global stop_btn
    global pause_btn
    global next_btn
    global previous_btn
    global volLabel
    global NameLabel

    current_name = song_name
    current_path = song_path

    stop_music()

    play = True


    def mute(*args):
        global volume_set
        setvolume = 0
        volume_set = setvolume
        mixer.music.set_volume(setvolume)
        volume_slider.config(value=setvolume)
        volLabel.config(image=Mute, command=unmute)
        main_window.bind("<m>", unmute)

    def unmute(*args):
        global volume_set
        setvolume = 1
        volume_set = setvolume
        mixer.music.set_volume(setvolume)
        volume_slider.config(value=setvolume)
        volLabel.config(image=HighVol, command=mute)
        main_window.bind("<m>", mute)

    def volume_control(x):
        global volume_set
        global volLabel
        setvolume = volume_slider.get()
        image_vol = round(setvolume, 1)
        if image_vol == 0.7 or image_vol == 0.6 or image_vol == 0.5:
            volLabel.config(image=MediumVol)
        elif image_vol == 0.1 or image_vol == 0.2 or image_vol == 0.3 or image_vol == 0.4:
            volLabel.config(image=LowVol)
        elif image_vol == 0.8 or image_vol == 0.9 or image_vol == 1.0:
            volLabel.config(image=HighVol)
        elif image_vol == 0.0:
            volLabel.config(image=Mute)

        mixer.music.set_volume(setvolume)
        volume_set = setvolume

    def volume_down(*args):
        global volume_set
        volume_set -= 0.1

        if volume_set <= 0:
            volume_set = 0
        else:
            pass

        mixer.music.set_volume(volume_set)

        setvolume = volume_slider.get()
        image_vol = round(setvolume, 1)

        if image_vol == 0.7 or image_vol == 0.6 or image_vol == 0.5:
            volLabel.config(image=MediumVol)
        elif image_vol == 0.1 or image_vol == 0.2 or image_vol == 0.3 or image_vol == 0.4:
            volLabel.config(image=LowVol)
        elif image_vol == 0.8 or image_vol == 0.9 or image_vol == 1.0:
            volLabel.config(image=HighVol)
        elif image_vol == 0.0:
            volLabel.config(image=Mute)

        volume_slider.config(value=volume_set)
        main_window.bind("<Down>", volume_down)

    def volume_up(*args):
        global volume_set
        volume_set += 0.1

        if volume_set >= 1:
            volume_set = 1
        else:
            pass

        setvolume = volume_slider.get()
        image_vol = round(setvolume, 1)

        if image_vol == 0.7 or image_vol == 0.6 or image_vol == 0.5:
            volLabel.config(image=MediumVol)
        elif image_vol == 0.1 or image_vol == 0.2 or image_vol == 0.3 or image_vol == 0.4:
            volLabel.config(image=LowVol)
        elif image_vol == 0.8 or image_vol == 0.9 or image_vol == 1.0:
            volLabel.config(image=HighVol)
        elif image_vol == 0.0:
            volLabel.config(image=Mute)

        mixer.music.set_volume(volume_set)
        volume_slider.config(value=volume_set)
        main_window.bind("<Up>", volume_up)

    song_load = MP3(song_path)
    song_length_raw = song_load.info.length
    est_length = int(song_length_raw)
    song_length = time.strftime('%M:%S', time.gmtime(song_length_raw))
    song_total_time.config(text=song_length, foreground="cyan")
    CategoryLabel1.config(text=category, foreground="cyan")

    thumbnail = PhotoImage(file=thumbnail_play)
    ImageLabel.config(image=thumbnail)
    ImageLabel.image = thumbnail

    currentlengthname = len(current_name)
    if currentlengthname > 15:
        current_name1 = current_name[0:15]
    else:
        current_name1 = current_name

    NameLabel2.config(text=current_name1, foreground="cyan")

    previous_btn = Button(main_window, image=Previous, border=0, bg="Gray1", activebackground="Gray1",
                          command=next_song)
    previous_btn.place(x=481, y=610)

    stop_btn = Button(main_window, image=Stop, border=0, bg="Gray1", activebackground="Gray1", command=stop_music)
    stop_btn.place(x=536, y=610)
    

    pause_btn = Button(main_window, image=Pause, border=0, bg="Gray1", activebackground="Gray1",
                       command=lambda: pause_music(paused))
    pause_btn.place(x=591, y=610)
    

    next_btn = Button(main_window, image=Next, border=0, bg="Gray1", activebackground="Gray1", command=previous_song)
    next_btn.place(x=646, y=610)
    

    global song_slider
    if Light:
        style1.configure("myStyle.Horizontal.TScale", background="#1B1F31")
    else:
        style1.configure("myStyle.Horizontal.TScale", background="#0D0F19")

    song_slider = ttk.Scale(main_window, from_=0, to=est_length, command=song_slide, length=720,
                            style="myStyle.Horizontal.TScale")
    song_slider.place(x=326, y=587)

    volLabel = Button(main_window, image=HighVol, background='gray1', activebackground="gray1", bd=0, command=mute)
    volLabel.place(x=930, y=618)

    global volume_slider
    volume_slider = ttk.Scale(main_window, from_=0, to=1, orient=HORIZONTAL, value=volume_set, command=volume_control,
                              length=120, style="myStyle.Horizontal.TScale")
    volume_slider.place(x=967, y=622)

    if volume_set == 0.7 or volume_set == 0.6 or volume_set == 0.5:
        volLabel.config(image=MediumVol)
    elif volume_set == 0.1 or volume_set == 0.2 or volume_set == 0.3 or volume_set == 0.4:
        volLabel.config(image=LowVol)
    elif volume_set == 0.8 or volume_set == 0.9 or volume_set == 1.0:
        volLabel.config(image=HighVol)
    elif volume_set == 0.0:
        volLabel.config(image=Mute)

    if Light:
        stop_btn.config(bg="#1B1F31", activebackground="#1B1F31")
        pause_btn.config(bg="#1B1F31", activebackground="#1B1F31")
        next_btn.config(bg="#1B1F31", activebackground="#1B1F31")
        previous_btn.config(bg="#1B1F31", activebackground="#1B1F31")
        volLabel.config(bg="#1B1F31", activebackground="#1B1F31")
        NameLabel2.config(bg="#1B1F31", foreground="#f16c83")
        song_total_time.config(bg="#1B1F31", foreground="#f16c83")
        CategoryLabel1.config(bg="#1B1F31", foreground="#f16c83")
    else:
        stop_btn.config(bg="#0D0F19", activebackground="#0D0F19")
        pause_btn.config(bg="#0D0F19", activebackground="#0D0F19")
        next_btn.config(bg="#0D0F19", activebackground="#0D0F19")
        previous_btn.config(bg="#0D0F19", activebackground="#0D0F19")
        volLabel.config(bg="#0D0F19", activebackground="#0D0F19")
        NameLabel2.config(bg="#0D0F19", foreground="#014964")
        song_total_time.config(bg="#0D0F19", foreground="#014964")
        CategoryLabel1.config(bg="#0D0F19", foreground="#014964")
        

    main_window.bind("<m>", mute)
    main_window.bind("<Down>", volume_down)
    main_window.bind("<Up>", volume_up)
    main_window.bind("<BackSpace>", stop_music)
    main_window.bind("<space>", lambda x: pause_music(paused))
    main_window.bind("<Right>", previous_song)
    main_window.bind("<Left>", next_song)
    main_window.bind("0", lambda x: rewind(song_path, song_name, category, thumbnail_play))

    mixer.music.load(song_path)
    mixer.music.play(loops=0)

    currentlengthname2 = len(current_name)
    if currentlengthname2 > 16:
        current_name2 = current_name[0:20]
    else:
        current_name2 = current_name

    NameLabel.config(text=current_name2)
    song_current_info()


def stop_music(*args):
    global play

    try:
        play = False
        mixer.music.stop()
        NameLabel.config(text=" ")

        song_current_time.config(text="", foreground="gray1")
        song_total_time.config(text="", foreground="gray1")

        NameLabel2.config(text="", foreground="turquoise4")
        CategoryLabel1.config(text="", foreground="turquoise4")
        ImageLabel.config(image="")

        volLabel.destroy()
        previous_btn.destroy()
        next_btn.destroy()
        pause_btn.destroy()
        volume_slider.destroy()
        stop_btn.destroy()
        song_slider.destroy()
    except:
        pass


def pause_music(is_paused):
    global paused
    paused = is_paused

    if paused:
        if Light:
            pause_btn.config(image=Light_Pause)
        else:
            pause_btn.config(image=Dark_Pause)
        mixer.music.unpause()
        paused = False
    else:
        if Light:
            pause_btn.config(image=Light_Play)
        else:
            pause_btn.config(image=Dark_Play)
        mixer.music.pause()
        paused = True


def next_song(*args):
    global pause_btn
    global current_path
    global current_name

    try:
        for songs in song_list:
            if songs == current_path:
                cur_index = song_list.index(songs)

                if cur_index == 0:
                    pass
                else:
                    next_song = song_list[cur_index - 1]
                    name_song = name_list[cur_index - 1]
                    category = category_list[cur_index - 1]
                    thumbnail = thumbnailplay_list[cur_index - 1]
                    current_name = name_song
                    current_path = next_song
                    pause_btn.config(text="Pause")
                    stop_music()
                    play_music(next_song, name_song, category, thumbnail)

    except:
        pass


def previous_song(*args):
    global pause_btn
    global current_path
    global current_name
    try:
        for songs in song_list:
            if songs == current_path:
                cur_index = song_list.index(songs)
                next_song = song_list[cur_index + 1]
                name_song = name_list[cur_index + 1]
                category = category_list[cur_index + 1]
                thumbnail = thumbnailplay_list[cur_index + 1]
                current_name = name_song
                current_path = next_song
                pause_btn.config(text="Pause")
                stop_music()
                play_music(next_song, name_song, category, thumbnail)

                break

    except:
        pass


def delete(song_name):
    if play:
        stop_music()
        command = f"DELETE FROM ALL_SONGS WHERE SONG_NAME='{song_name}';"
        mycursor.execute(command)
        mydatabase.commit()
        main_screen()
    else:
        command = f"DELETE FROM ALL_SONGS WHERE SONG_NAME='{song_name}';"
        mycursor.execute(command)
        mydatabase.commit()
        main_screen()


def main_screen(cat="None"):
    global Light
    global song_list
    global name_list
    global current_name
    global current_path
    global thumbnail_list
    global thumbnailplay_list
    global category_list
    global current_thumbnail
    global all_name_list
    global all_thumbnail_list
    global all_thumbnailplay_list
    global all_category_list
    global light_image
    global dark_image

    wrapper1 = LabelFrame(main_window, width="1900", height="100", background="Blue", bd=0)
    if Light:
        mycanvas = Canvas(wrapper1, background="#1C2238", borderwidth=0, highlightthickness=0, width=803, height=545)
    else:
        mycanvas = Canvas(wrapper1, background="#010113", borderwidth=0, highlightthickness=0, width=803, height=545)

    mycanvas.pack(side=LEFT, expand=False, padx=0)

    yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=mycanvas.yview)
    yscrollbar.pack(side=RIGHT, fill="y", expand=False)

    mycanvas.configure(yscrollcommand=yscrollbar.set)

    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))

    myframe = Frame(mycanvas)
    Label1 = Label(myframe)
    mycanvas.create_window((0, 0), window=myframe, anchor="n")

    def OnMouseWheel(event):
        mycanvas.yview_scroll(-1 * (int(event.delta / 120)), "units")

    mycanvas.bind_all("<MouseWheel>", OnMouseWheel)

    wrapper1.place(x=305, y=2)

    see = "SELECT * from All_Songs"
    mycursor.execute(see)
    show_result = mycursor.fetchall()

    all_list, all_name_list, all_thumbnail_list, all_thumbnailplay_list, all_category_list = [], [], [], [], []
    cat_list, cat_name_list, cat_thumbnail_list, cat_thumbnailplay_list, cat_category_list = [], [], [], [], []

    for song in show_result:
        all_name_list.append(song[0])
        all_category_list.append(song[1])
        all_list.append(song[2])
        all_thumbnail_list.append(song[3])
        all_thumbnailplay_list.append(song[4])

        if song[1] == cat:
            cat_list.append(song[2])
            cat_name_list.append(song[0])
            cat_category_list.append(cat)
            cat_thumbnail_list.append(song[3])
            cat_thumbnailplay_list.append(song[4])

    if cat == "None":
        song_list = all_list
        name_list = all_name_list
        category_list = all_category_list
        thumbnail_list = all_thumbnail_list
        thumbnailplay_list = all_thumbnailplay_list

        if Light:
            Label2 = Label(myframe, image=All_Song_Light, background="#010113", border=0)
        else:
            Label2 = Label(myframe, image=All_Song_Dark, background="#010113", border=0)

    else:
        song_list = cat_list
        name_list = cat_name_list
        category_list = cat_category_list
        thumbnail_list = cat_thumbnail_list
        thumbnailplay_list = cat_thumbnailplay_list

        light_image_title = f"{light_folder_location_main}{cat}_Light.png"
        dark_image_title = f"{dark_folder_location_main}{cat}_Dark.png"

        light_image = PhotoImage(file = light_image_title)
        dark_image = PhotoImage(file = dark_image_title)

        if Light:
            Label2 = Label(myframe, image=light_image, background="#010113", border=0)
        else:
            Label2 = Label(myframe, image=dark_image, background="#010113", border=0)


    Label2.grid(row=0, column=0)

    list_len = len(song_list)

    for i in range(0, list_len):
        current_path1 = song_list[i]
        current_name1 = name_list[i]
        current_category = category_list[i]
        current_thumbnail = thumbnail_list[i]
        current_playthumnail = thumbnailplay_list[i]

        current_path = current_path1
        current_name = current_name1

        song_load = MP3(current_path)
        song_length_raw = song_load.info.length
        song_length = time.strftime('%M:%S', time.gmtime(song_length_raw))

        play_command = (lambda current_path2=current_path1, current_name=current_name,
                               current_category1=current_category,
                               current_playthumbnail1=current_playthumnail: play_music(current_path2,
                                                                                       current_name,
                                                                                       current_category1,
                                                                                       current_playthumbnail1))

        global BG_button
        BG_Button = Button(myframe, image=ML, border=0, activebackground="#1C2238", background="#1C2238",
                           command=play_command)

        BG_Button.grid(row=i + 300, ipady=5)

        thumbnail = ImageTk.PhotoImage(Image.open(current_thumbnail))

        thumbnail_btn = Button(myframe, image=thumbnail, borderwidth=0, activebackground="#010113",
                               background="#010113",
                               command=play_command)
        thumbnail_btn.grid(row=i + 300, padx=10, ipady=0, sticky=W)

        name_Button = Button(myframe, text=current_name, bd=0, activebackground="#010113", background="#010113",
                             fg="#8b0f23",
                             font=("Microsoft JhengHei UI", 13, "bold"),
                             command=play_command)
        name_Button.grid(row=i + 300, padx=69, ipady=5, sticky=W)

        length_Button = Button(myframe, text=song_length, bd=0, activebackground="#010113", background="#010113",
                               fg="#8b0f23",
                               font=("Calibri Light", 13, "bold"),
                               command=play_command)
        length_Button.grid(row=i + 300, sticky=E, padx=(0, 15), ipady=5)

        DelButton = Button(myframe, bd=0, activebackground="#010113", background="#010113", image=Delete,
                           command=lambda songname1=current_name: delete(songname1))
        DelButton.grid(row=i + 300, sticky=E, padx=(0, 90), ipady=5)

        DefPlayerButton = Button(myframe, bd=0, image=Default, activebackground="#010113", background="#010113",
                                 command=lambda songpath1=current_path1: os.startfile(songpath1))
        DefPlayerButton.grid(row=i + 300, sticky=E, padx=(0, 140), ipady=5)

        thumbnail_btn.image = thumbnail

        if Light:
            BG_Button.config(activebackground="#1C2238")
            thumbnail_btn.config(activebackground="#f26d83", background="#f26d83")
            name_Button.config(activebackground="#f26d83", background="#f26d83",fg="#8b0f23",activeforeground="#8b0f23")
            length_Button.config(activebackground="#f26d83", background="#f26d83",fg="#8b0f23",activeforeground="#8b0f23")
            DelButton.config(activebackground="#f26d83", background="#f26d83")
            DefPlayerButton.config(activebackground="#f26d83", background="#f26d83")
        else:
            BG_Button.config(activebackground="#080404", background="#041024")
            thumbnail_btn.config(activebackground="#050505", background="#0D0D0D")
            name_Button.config(activebackground="#050505", background="#0D0D0D",fg="#014964",activeforeground="#014964")
            length_Button.config(activebackground="#050505", background="#0D0D0D",fg="#014964",activeforeground="#014964")
            DelButton.config(activebackground="#050505", background="#0D0D0D")
            DefPlayerButton.config(activebackground="#050505", background="#0D0D0D")


def all_song(cat="None"):
    global Dark
    global Light

    main_screen("None")

    if Dark:
        if cat == "Party":
            Party_but.config(image=Dark_Party, bg="#0D0D0D", activebackground="#0D0D0D", command=party)
        elif cat == "Sleep":
            Sleep_but.config(image=Dark_Sleep, bg="#0D0D0D", activebackground="#0D0D0D", command=sleep)
        elif cat == "Love":
            Love_but.config(image=Dark_Love, bg="#0D0D0D", activebackground="#0D0D0D", command=love)
        elif cat == "Workout":
            Workout_but.config(image=Dark_Workout, bg="#0D0D0D", activebackground="#0D0D0D", command=workout)
        elif cat == "None":
            Party_but.config(image=Dark_Party, bg="#0D0D0D", activebackground="#0D0D0D", command=party)
            Sleep_but.config(image=Dark_Sleep, bg="#0D0D0D", activebackground="#0D0D0D", command=sleep)
            Love_but.config(image=Dark_Love, bg="#0D0D0D", activebackground="#0D0D0D", command=love)
            Workout_but.config(image=Dark_Workout, bg="#0D0D0D", activebackground="#0D0D0D", command=workout)

    elif Light:
        if cat == "Party":
            Party_but.config(image=Light_Party, bg="#292F49", activebackground="#292F49", command=party)
        elif cat == "Sleep":
            Sleep_but.config(image=Light_Sleep, bg="#292F49", activebackground="#292F49", command=sleep)
        elif cat == "Love":
            Love_but.config(image=Light_Love, bg="#292F49", activebackground="#292F49", command=love)
        elif cat == "Workout":
            Workout_but.config(image=Light_Workout, bg="#292F49", activebackground="#292F49", command=workout)
        elif cat == "None":
            Party_but.config(image=Light_Party, bg="#292F49", activebackground="#292F49", command=party)
            Sleep_but.config(image=Light_Sleep, bg="#292F49", activebackground="#292F49", command=sleep)
            Love_but.config(image=Light_Love, bg="#292F49", activebackground="#292F49", command=love)
            Workout_but.config(image=Light_Workout, bg="#292F49", activebackground="#292F49", command=workout)


def party():
    global Dark
    global Light

    main_screen("Party")

    if Dark:
        Sleep_but.config(image=Dark_Sleep, bg="#0D0D0D", activebackground="#0D0D0D", command=sleep)
        Love_but.config(image=Dark_Love, bg="#0D0D0D", activebackground="#0D0D0D", command=love)
        Workout_but.config(image=Dark_Workout, bg="#0D0D0D", activebackground="#0D0D0D", command=workout)
        Party_but.config(image=Dark_All_Songs, bg="#0D0D0D", activebackground="#0D0D0D",
                         command=lambda: all_song("Party"))
    elif Light:
        Sleep_but.config(image=Light_Sleep, bg="#292F49", activebackground="#292F49", command=sleep)
        Love_but.config(image=Light_Love, bg="#292F49", activebackground="#292F49", command=love)
        Workout_but.config(image=Light_Workout, bg="#292F49", activebackground="#292F49", command=workout)
        Party_but.config(image=Light_All_Songs, bg="#292F49", activebackground="#292F49",
                         command=lambda: all_song("Party"))


def workout():
    global Dark
    global Light

    main_screen("Workout")

    if Dark:
        Party_but.config(image=Dark_Party, bg="#0D0D0D", activebackground="#0D0D0D", command=party)
        Sleep_but.config(image=Dark_Sleep, bg="#0D0D0D", activebackground="#0D0D0D", command=sleep)
        Love_but.config(image=Dark_Love, bg="#0D0D0D", activebackground="#0D0D0D", command=love)
        Workout_but.config(image=Dark_All_Songs, bg="#0D0D0D", activebackground="#0D0D0D",
                           command=lambda: all_song("Workout"))

    elif Light:
        Party_but.config(image=Light_Party, bg="#292F49", activebackground="#292F49", command=party)
        Sleep_but.config(image=Light_Sleep, bg="#292F49", activebackground="#292F49", command=sleep)
        Love_but.config(image=Light_Love, bg="#292F49", activebackground="#292F49", command=love)
        Workout_but.config(image=Light_All_Songs, bg="#292F49", activebackground="#292F49",
                           command=lambda: all_song("Workout"))


def love():
    global Dark
    global Light

    main_screen("Love")

    if Dark:
        Party_but.config(image=Dark_Party, bg="#0D0D0D", activebackground="#0D0D0D", command=party)
        Sleep_but.config(image=Dark_Sleep, bg="#0D0D0D", activebackground="#0D0D0D", command=sleep)
        Workout_but.config(image=Dark_Workout, bg="#0D0D0D", activebackground="#0D0D0D", command=workout)
        Love_but.config(image=Dark_All_Songs, bg="#0D0D0D", activebackground="#0D0D0D",
                        command=lambda: all_song("Love"))

    elif Love:
        Party_but.config(image=Light_Party, bg="#292F49", activebackground="#292F49", command=party)
        Sleep_but.config(image=Light_Sleep, bg="#292F49", activebackground="#292F49", command=sleep)
        Workout_but.config(image=Light_Workout, bg="#292F49", activebackground="#292F49", command=workout)
        Love_but.config(image=Light_All_Songs, bg="#292F49", activebackground="#292F49",
                        command=lambda: all_song("Love"))


def sleep():
    global Dark
    global Light

    main_screen("Sleep")

    if Dark:
        Party_but.config(image=Dark_Party, bg="#0D0D0D", activebackground="#0D0D0D", command=party)
        Love_but.config(image=Dark_Love, bg="#0D0D0D", activebackground="#0D0D0D", command=love)
        Workout_but.config(image=Dark_Workout, bg="#0D0D0D", activebackground="#0D0D0D", command=workout)
        Sleep_but.config(image=Dark_All_Songs, bg="#0D0D0D", activebackground="#0D0D0D",
                         command=lambda: all_song("Sleep"))

    elif Light:
        Party_but.config(image=Light_Party, bg="#292F49", activebackground="#292F49", command=party)
        Love_but.config(image=Light_Love, bg="#292F49", activebackground="#292F49", command=love)
        Workout_but.config(image=Light_Workout, bg="#292F49", activebackground="#292F49", command=workout)
        Sleep_but.config(image=Light_All_Songs, bg="#292F49", activebackground="#292F49",
                         command=lambda: all_song("Sleep"))


def theme_change():
    global Dark
    global Light
    global Dark_BG
    global Dark_Add_Song
    global Dark_Add_from_Folder
    global Dark_Go_Online
    global Dark_ML
    global Dark_All_Songs
    global Dark_Sleep
    global Dark_Workout
    global Dark_Love
    global Dark_Party
    global Dark_IMG_BG
    global Dark_Logo
    global Light_BG
    global Light_Add_Song
    global Light_Add_from_Folder
    global Light_Go_Online
    global Light_ML
    global Light_All_Songs
    global Light_Sleep
    global Light_Workout
    global Light_Love
    global Light_Party
    global Light_IMG_BG
    global Light_Logo
    global Theme_Change
    global AddSongButton
    global AddFolderButton
    global Go_Online_but
    global Sleep_but
    global Workout_but
    global Love_but
    global Party_but
    global BG_label
    global IBG
    global ML
    global Light_ML
    global Dark_ML
    global Delete
    global Default

    global stop_btn
    global pause_btn
    global next_btn
    global previous_btn
    global volLabel
    global paused

    global Play
    global Pause
    global Stop
    global Next
    global Previous
    global HighVol
    global MediumVol
    global LowVol
    global Mute

    global NameLabel
    global NameLabel2
    global song_current_time
    global song_total_time
    global ImageLabel
    global CategoryLabel1

    if Dark:
        temp = open("Theme.txt", "w")
        temp.write("Light")
        temp.close()
        Dark = False
        Light = True

        BG_label.config(image=Light_BG)
        IBG.config(image=Light_IMG_BG)

        Theme_Change.config(image=Light_Logo, bg="#292F49", activebackground="#292F49")
        AddSongButton.config(image=Light_Add_Song, bg="#292F49", activebackground="#292F49")
        AddFolderButton.config(image=Light_Add_from_Folder, bg="#292F49", activebackground="#292F49")
        Go_Online_but.config(image=Light_Go_Online, bg="#292F49", activebackground="#292F49")
        Sleep_but.config(image=Light_Sleep, bg="#292F49", activebackground="#292F49")
        Workout_but.config(image=Light_Workout, bg="#292F49", activebackground="#292F49")
        Love_but.config(image=Light_Love, bg="#292F49", activebackground="#292F49")
        Party_but.config(image=Light_Party, bg="#292F49", activebackground="#292F49")
        ML = PhotoImage(file=Light_SongDisplay_BG_main)
        Delete = PhotoImage(file=Light_Delete_main)
        Default = PhotoImage(file=Light_Default_main)
        Play = PhotoImage(file=Light_Play_location_HUD)
        Pause = PhotoImage(file=Light_Pause_location_HUD)
        Stop = PhotoImage(file=Light_Stop_location_HUD)
        Next = PhotoImage(file=Light_Next_location_HUD)
        Previous = PhotoImage(file=Light_Previous_location_HUD)
        HighVol = PhotoImage(file=Light_FullVolume_location_HUD)
        MediumVol = PhotoImage(file=Light_MediumVolume_location_HUD)
        LowVol = PhotoImage(file=Light_LowVolume_location_HUD)
        Mute = PhotoImage(file=Light_MutedVolume_location_HUD)

        

        NameLabel.config(bg="#1B1F31", foreground="#f16c83")
        song_current_time.config(bg="#1B1F31", foreground="#f16c83")
        song_total_time.config(bg="#1B1F31", foreground="#f16c83")
        ImageLabel.config(bg="#1B1F31")
        NameLabel2.config(bg="#1B1F31", foreground="#f16c83")
        CategoryLabel1.config(bg="#1B1F31", foreground="#f16c83")

        style1.configure("myStyle.Horizontal.TScale", background="#1B1F31")

        if paused:
            stop_btn.config(image=Light_Stop, bg="#1B1F31", activebackground="#1B1F31")
            pause_btn.config(image=Light_Play, bg="#1B1F31", activebackground="#1B1F31")
            next_btn.config(image=Light_Next, bg="#1B1F31", activebackground="#1B1F31")
            previous_btn.config(image=Light_Previous, bg="#1B1F31", activebackground="#1B1F31")
            volLabel.config(image=Light_HighVol, bg="#1B1F31", activebackground="#1B1F31")
        else:
            try:
                stop_btn.config(image=Light_Stop, bg="#1B1F31", activebackground="#1B1F31")
                pause_btn.config(image=Light_Pause, bg="#1B1F31", activebackground="#1B1F31")
                next_btn.config(image=Light_Next, bg="#1B1F31", activebackground="#1B1F31")
                previous_btn.config(image=Light_Previous, bg="#1B1F31", activebackground="#1B1F31")
                volLabel.config(image=Light_HighVol, bg="#1B1F31", activebackground="#1B1F31")
            except:
                pass

        main_screen()
        all_song("None")


    elif Light:
        temp = open("Theme.txt", "w")
        temp.write("Dark")
        temp.close()
        Dark = True
        Light = False

        BG_label.config(image=Dark_BG)
        IBG.config(image=Dark_IMG_BG)

        Theme_Change.config(image=Dark_Logo, bg="#0D0D0D", activebackground="#0D0D0D")
        AddSongButton.config(image=Dark_Add_Song, bg="#0D0D0D", activebackground="#0D0D0D")
        AddFolderButton.config(image=Dark_Add_from_Folder, bg="#0D0D0D", activebackground="#0D0D0D")
        Go_Online_but.config(image=Dark_Go_Online, bg="#0D0D0D", activebackground="#0D0D0D")
        Sleep_but.config(image=Dark_Sleep, bg="#0D0D0D", activebackground="#0D0D0D")
        Workout_but.config(image=Dark_Workout, bg="#0D0D0D", activebackground="#0D0D0D")
        Love_but.config(image=Dark_Love, bg="#0D0D0D", activebackground="#0D0D0D")
        Party_but.config(image=Dark_Party, bg="#0D0D0D", activebackground="#0D0D0D")
        ML = PhotoImage(file=Dark_SongDisplay_BG_main)
        Delete = PhotoImage(file=Dark_Delete_main)
        Default = PhotoImage(file=Dark_Default_main)
        Play = PhotoImage(file=Dark_Play_location_HUD)
        Pause = PhotoImage(file=Dark_Pause_location_HUD)
        Stop = PhotoImage(file=Dark_Stop_location_HUD)
        Next = PhotoImage(file=Dark_Next_location_HUD)
        Previous = PhotoImage(file=Dark_Previous_location_HUD)
        HighVol = PhotoImage(file=Dark_FullVolume_location_HUD)
        MediumVol = PhotoImage(file=Dark_MediumVolume_location_HUD)
        LowVol = PhotoImage(file=Dark_LowVolume_location_HUD)
        Mute = PhotoImage(file=Dark_MutedVolume_location_HUD)
        style1.configure("myStyle.Horizontal.TScale", background="#0D0F19")

        NameLabel.config(bg="#0D0F19", foreground="#014964")
        song_current_time.config(bg="#0D0F19", foreground="#014964")
        song_total_time.config(bg="#0D0F19", foreground="#014964")
        ImageLabel.config(bg="#0D0F19", foreground="#014964")
        NameLabel2.config(bg="#0D0F19", foreground="#014964")
        CategoryLabel1.config(bg="#0D0F19", foreground="#014964")

        if paused:
            stop_btn.config(image=Dark_Stop, bg="#0D0F19", activebackground="#0D0F19")
            pause_btn.config(image=Dark_Play, bg="#0D0F19", activebackground="#0D0F19")
            next_btn.config(image=Dark_Next, bg="#0D0F19", activebackground="#0D0F19")
            previous_btn.config(image=Dark_Previous, bg="#0D0F19", activebackground="#0D0F19")
            volLabel.config(image=Dark_HighVol, bg="#0D0F19", activebackground="#0D0F19")
        else:
            try:
                stop_btn.config(image=Dark_Stop, bg="#0D0F19", activebackground="#0D0F19")
                pause_btn.config(image=Dark_Pause, bg="#0D0F19", activebackground="#0D0F19")
                next_btn.config(image=Dark_Next, bg="#0D0F19", activebackground="#0D0F19")
                previous_btn.config(image=Dark_Previous, bg="#0D0F19", activebackground="#0D0F19")
                volLabel.config(image=Dark_HighVol, bg="#0D0F19", activebackground="#0D0F19")
            except:
                pass

        main_screen()
        all_song("None")


if __name__ == '__main__':
    BG_label = Label(main_window, image=BG, border=0)
    BG_label.place(x=0, y=0)

    IBG = Label(main_window, image=IMG_BG, relief="flat", border=0)
    IBG.place(x=301, y=1)

    Theme_Change = Button(main_window, image=Logo, border=0, bg="#0D0D0D", activebackground="#0D0D0D",
                          command=theme_change)
    Theme_Change.place(x=0, y=10)

    AddSongButton = Button(main_window, image=Add_Song, border=0, bg="#0D0D0D", activebackground="#0D0D0D",
                           command=add_song)
    AddSongButton.place(x=25, y=134)

    AddFolderButton = Button(main_window, image=Add_from_Folder, border=0, bg="#0D0D0D", activebackground="#0D0D0D",
                             command=add_folder)
    AddFolderButton.place(x=25, y=176)

    Go_Online_but = Button(main_window, image=Go_Online, border=0, bg="#0D0D0D", activebackground="#0D0D0D",
                           command=go_online)
    Go_Online_but.place(x=25, y=218)

    # HUD
    NameLabel = Label(main_window, text=" ", font=("Century Gothic", 18), foreground="white", background="#0D0F19")
    NameLabel.place(x=500, y=558)

    song_current_time = Label(main_window, text=" ", foreground="#f16c83", background="#0D0F19",
                              font=("Century Gothic", 11, "bold"))
    song_current_time.place(x=283, y=587)

    song_total_time = Label(main_window, text=" ", foreground="gray1", background="#0D0F19",
                            font=("Century Gothic", 11, "bold"))
    song_total_time.place(x=1050, y=587)

    # Current
    ImageLabel = Label(main_window, background="#0D0F19")
    ImageLabel.place(x=8, y=566)

    NameLabel2 = Label(main_window, text=" ", font=("Century Gothic", 15), foreground="turquoise4",
                       background="#0D0F19")
    NameLabel2.place(x=95, y=569)

    CategoryLabel1 = Label(main_window, text=" ", font=("Century Gothic", 14), foreground="turquoise4",
                           background="#0D0F19")
    CategoryLabel1.place(x=95, y=599)

    # Playlist Bar
    Sleep_but = Button(main_window, image=Sleep, border=0, bg="#0D0D0D", activebackground="#0D0D0D", command=sleep)
    Sleep_but.place(x=25, y=434)

    Workout_but = Button(main_window, image=Workout, border=0, bg="#0D0D0D", activebackground="#0D0D0D",
                         command=workout)
    Workout_but.place(x=25, y=476)

    Love_but = Button(main_window, image=Love, border=0, bg="#0D0D0D", activebackground="#0D0D0D", command=love)
    Love_but.place(x=25, y=350)

    Party_but = Button(main_window, image=Party, border=0, bg="#0D0D0D", activebackground="#0D0D0D", command=party)
    Party_but.place(x=25, y=392)

    if Light:
        Theme_Change.config(bg="#292F49", activebackground="#292F49")
        AddSongButton.config(bg="#292F49", activebackground="#292F49")
        AddFolderButton.config(bg="#292F49", activebackground="#292F49")
        Go_Online_but.config(bg="#292F49", activebackground="#292F49")
        Sleep_but.config(bg="#292F49", activebackground="#292F49")
        Workout_but.config(bg="#292F49", activebackground="#292F49")
        Love_but.config(bg="#292F49", activebackground="#292F49")
        Party_but.config(bg="#292F49", activebackground="#292F49")
        NameLabel.config(bg="#1B1F31", foreground="#f16c83")
        song_current_time.config(bg="#1B1F31", foreground="#f16c83")
        song_total_time.config(bg="#1B1F31", foreground="#f16c83")
        ImageLabel.config(bg="#1B1F31")
        NameLabel2.config(bg="#1B1F31")
        CategoryLabel1.config(bg="#1B1F31", foreground="#f16c83")

    else:
        NameLabel.config(bg="#0D0F19", foreground="#014964")
        song_current_time.config(bg="#0D0F19", foreground="#014964")


    main_screen()


    mainloop()
