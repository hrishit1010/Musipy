import os
import random
import pathlib
import mysql.connector

file_path = pathlib.Path(__file__).parent.resolve()

# Database Initiation
try:
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="harsh3304",
        database="MUSICPLAYER"
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
    mycursor.execute("CREATE DATABASE MUSICPLAYER")
    mycursor.execute("USE MUSICPLAYER")
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

name_list = []
category_list = []
path_list = []
thumbnail_list = []
thumbnailplay_list = []

song_name_list = ["Night we Met", "Sparkle", "Back To You", "Thousand Years", "Watsahi no Uso Instrumental",
                  "Night Changes", "Dont Let Me Go", "Saturday Nights",
                  "Watermelon Sugar", "Make You Mine", "Bang Bang", "Cheap Thrills",
                  "Deadwood", "Unstoppable", "Fearless"]  # , "Eternal Youth"]

category_list_choice = ["Love", "Love", "Love", "Love",
                        "Sleep", "Sleep", "Sleep", "Sleep",
                        "Party", "Party", "Party", "Party",
                        "Workout", "Workout", "Workout"]  # , "Workout"]

folder_location = str(file_path) + "\\Dependencies\\Test Songs\\"
folder_location_thumb = str(file_path) + "\\Dependencies\\Thumbnails\\"
folder_location_thumbplay = str(file_path) + "\\Dependencies\\ThumbnailsPlay\\"

length_mus = random.randint(8, 12)

for i in range(0, length_mus):
    song_name = random.choice(song_name_list)

    index = song_name_list.index(song_name)

    category = category_list_choice[index]
    path = folder_location + str(song_name + ".mp3")
    thumbnail = folder_location_thumb + str(song_name + "_thumbnail.png")
    thumbnailplay = folder_location_thumbplay + str(song_name + "_thumbnailplay.png")

    name_list.append(song_name)
    category_list.append(category)
    path_list.append(path)
    thumbnail_list.append(thumbnail)
    thumbnailplay_list.append(thumbnailplay)

    song_name_list.remove(song_name)
    category_list_choice.remove(category)

name_length = len(name_list)

for i in range(0, name_length):
    song_name = name_list[i]
    category = category_list[i]
    path = path_list[i]
    thumbnail = thumbnail_list[i]
    thumbnailplay = thumbnailplay_list[i]

    Formula = "INSERT INTO All_Songs (SONG_NAME,CATEGORY,SONG_PATH,THUMBNAIL, THUMBNAIL_PLAY) VALUES(%s, %s, %s, %s, %s)"
    song_save = (song_name, category, path, thumbnail, thumbnailplay)

    mycursor.execute(Formula, song_save)
    mydatabase.commit()

print(length_mus, "songs added to SoulSync")

input("\nPress ANY KEY to redirect to MainScreen...")
os.system("SoulSync.pyw")
quit()
