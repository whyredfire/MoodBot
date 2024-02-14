import os
import random
import threading
import time
import tkinter as tk
import urllib.request
import warnings
from io import BytesIO

import cv2
import numpy as np
import yt_dlp
from PIL import Image, ImageTk
from keras.models import load_model
from keras.preprocessing import image
from pytube import YouTube
from audioplayer import AudioPlayer
from moviepy.editor import *

warnings.filterwarnings("ignore")

# Loading Keras model for Facial Emotion Detection
model = load_model("model3.h5")
face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Dictionary Containing all playlists and their Genres
playlist_dict = {
    "neutral": "https://www.youtube.com/playlist?list=RDCLAK5uy_l80pbx0UAQ7EWipFs57eQnUIB9KbaDEow&playnext=1&si=PZ-pQzrh89oC8DIQ",
    "happy": "https://music.youtube.com/playlist?list=RDCLAK5uy_kJWGcrtTC_zrbD6rKkBvOcht_vzijhX1A&playnext=1&si=AH4e0-3lgT9tIjz5",
    "sad": "https://music.youtube.com/playlist?list=RDCLAK5uy_mIY1OIxvwlIkS_U3MX6O5uHZXkB-LiJu8&playnext=1&si=81A90fIxhtAqSYWV",
    "angry": "https://www.youtube.com/playlist?list=PL-PfH-O9Jvs0DpXUXX1puvpHTNXhT_NCT"
}

ydl_opts = {
    'quiet': True,
    'extract_flat': True,
}
# Deleting all extra files that couldnt be deleted in the last run
for filename in os.listdir():
    if filename.endswith('.mp3') or filename.endswith('.mp4'):
        os.remove(f"{filename}")
# Extracting Thumbnail from the chosen song url
def urltoimg(image_url):
    with urllib.request.urlopen(image_url) as my_url_res:
        my_img_data = my_url_res.read()

    # Resizing Image to fit in GUI
    my_img = Image.open(BytesIO(my_img_data))
    base_width = 640
    wpercent = (base_width / float(my_img.size[0]))
    hsize = int((float(my_img.size[1]) * float(wpercent)))
    img = my_img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(img)
    return image

# Setting Global toggle states and active states
playing_state = False
music_file = ''
# Class Encapsulating all Features of the GUI
class CameraApp:

    def __init__(self):

        # Initializing the TKinter window
        self.root = tk.Tk()
        self.root.title("Moodbot")
        self.root.geometry("1280x510")

        # Creating a canvas for the camera feed
        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.grid(row=0, column=0, rowspan=2)

        # Initializing the Camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 480)
        self.cap.set(4, 640)
        self.show_camera_feed()

        # Create buttons

        # Capture Button which captivates a Users emotions
        self.button4 = tk.Button(self.root, text="Press me to detect", command=self.detect_emotion)
        self.button4.place(x=0, y=480, width=640, height=30)

        # Song Next Button
        self.regen = tk.Button(self.root, text="REGEN", command=self.manual_play,state=tk.DISABLED)
        self.regen.place(x=640, y=450, width=213, height=60)

        # Volume Up Button
        self.vol_up = tk.Button(self.root, text="VOL UP", command=self.volume_up, state=tk.DISABLED)
        self.vol_up.place(x=1067, y=450, width=213, height=30)

        # Volume Down Button
        self.vol_down = tk.Button(self.root, text="VOL DOWN", command=self.volume_down, state=tk.DISABLED)
        self.vol_down.place(x=1067, y=480, width=213, height=30)

        # Song Pause/Play Button
        self.playpause = tk.Button(self.root, text="PLAY/PAUSE", command=self.pause_play, pady=5, padx=5, state=tk.DISABLED)
        self.playpause.place(x=853, y=450, width=214, height=60)

        # Drop Down Menu for Manual selection of Emotion-Genre
        self.playemotion = tk.Button(self.root, text="Click me to load!", command=self.manual_play)
        self.playemotion.place(x=853, y=390, width=107, height=60)
        self.clicked = tk.StringVar()
        self.clicked.set("Emotions")
        self.popup = tk.OptionMenu(self.root, self.clicked, "Happy", "Sad", "Angry", "Neutral")
        self.popup.place(x=960, y=390, width=107, height=60)

        # Create a placeholder for the thumbnail
        self.image_url = "https://img.youtube.com/vi/oBpaB2YzX8s/maxresdefault.jpg"
        self.image = urltoimg(self.image_url)
        self.thumbnail_label = tk.Label(self.root, image=self.image)
        self.thumbnail_label.place(x=640, y=0)

        # Placeholder Title, Welcome!
        self.yt_title = tk.Label(self.root, text="Welcome!")
        self.yt_title.place(x=640, y=360, width=640, height=30)
        
    # Activate UI
    def activate(self):
        self.vol_down["state"] = tk.NORMAL
        self.vol_up["state"] = tk.NORMAL
        self.regen["state"] = tk.NORMAL
        self.playpause["state"] = tk.NORMAL
        
    # Camera Feed integration with the created canvas to fit in GUI
    def show_camera_feed(self):
        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.canvas.img_tk = img_tk
        self.root.after(2, self.show_camera_feed)

    # Fetching random song from playlist
    def fetch_random_song(self, genre):
        if genre in playlist_dict:
            playlist_url = playlist_dict[genre]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)
                if 'entries' in playlist_info:
                    songs = playlist_info['entries']
                    if songs:
                        random_song = random.choice(songs)
                        return random_song['url']
        return None

    # Volume up
    def volume_up(self):
        global playing_state

        if playing_state:
            self.song.volume += 5
    # Volume Down
    def volume_down(self):
        global playing_state

        if playing_state:
            self.song.volume -= 5

    # Pausing Song
    def pause_play(self):
        global playing_state

        if not playing_state:
            self.song.resume()
            playing_state = True
        else:
            self.song.pause()
            playing_state = False

    # Tracker to delete song at End of Song
    def delete_song(self):
        for i in range(0, self.yt.length):
            time.sleep(1)
        self.song.close()
        os.remove(f"{self.yt.title}.mp3")
        os.remove(f"{self.yt.title}.mp4")
    # Daemon Thread to track duration of song till end
    def del_thread(self):
        self.delete = threading.Thread(target=self.delete_song)
        self.delete.daemon = True
        self.delete.start()

    # Playing a song from URL
    def play_song(self):
        global music_file
        global playing_state

        # Downloading file locally to run
        stream = self.yt.streams.get_lowest_resolution()
        stream.download()
        try:
            video = VideoFileClip(f"{self.yt.title}.mp4")
            audio = video.audio
            audio.write_audiofile(f"{self.yt.title}.mp3")
            time.sleep(5)
            music_file = f"{self.yt.title}.mp3"
            if music_file:
                self.song = AudioPlayer(music_file)
                self.song.play(loop=False, block=False)
                self.song.volume = 20
                playing_state = True
                self.del_thread()
        except IOError:
            print("Whoopsie, try again")


    # Changing Thumbnail once video is found
    def change_thumbnail(self):
        # If Thumbnail not Available or Not Found, Come back to default
        try:
            imageurl = "https://img.youtube.com/vi/%s/maxresdefault.jpg" % (self.random_song_url.split('=')[1])
            self.image = urltoimg(imageurl)
        except:
            self.image = urltoimg("https://img.youtube.com/vi/oBpaB2YzX8s/maxresdefault.jpg")

        # Setting Image to Label
        self.thumbnail_label = tk.Label(self.root, image=self.image)
        self.thumbnail_label.place(x=640, y=0)

        # Extracting Title and Duration and Author
        self.yt_title = tk.Label(self.root,
                                 text=f"{self.yt.author}, {self.yt.title}\nLength = {self.yt.length // 60}:\
{self.yt.length % 60 if self.yt.length % 60 >= 10 else ('0' + str(self.yt.length % 60))}")
        self.yt_title.place(x=640, y=360, width=640, height=30)

    # Manual Input playing
    def manual_play(self):
        if music_file != '':
            try:
                self.song.close()
                os.remove(f"{self.yt.title}.mp3")
                os.remove(f"{self.yt.title}.mp4")
                print("DELETED")
            except PermissionError or FileNotFoundError:
                pass
        self.activate()
        self.predicted_emotion = self.clicked.get()
        self.random_song_url = self.fetch_random_song(self.predicted_emotion.lower())
        self.yt = YouTube(self.random_song_url)
        self.play_song()
        self.change_thumbnail()

    # Emotion Detection Model to identify emotion at given instance
    def detect_emotion(self):
        # Deleting any active songs playing
        if music_file != '':
            try:
                self.song.close()
                os.remove(f"{self.yt.title}.mp3")
                os.remove(f"{self.yt.title}.mp4")
                print("DELETED")
            except PermissionError or FileNotFoundError:
                pass

        # Keras Model running to detect Emotion
        while True:
            ret, test_img = self.cap.read()
            if not ret:
                continue
            gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
            faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)
            for (x, y, w, h) in faces_detected:
                cv2.rectangle(test_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
                roi_gray = gray_img[y:y + w, x:x + h]
                roi_gray = cv2.resize(roi_gray, (48, 48))
                img_pixels = image.img_to_array(roi_gray)
                img_pixels = np.expand_dims(img_pixels, axis=0)
                img_pixels /= 255

                predictions = model.predict(img_pixels)
                max_index = np.argmax(predictions[0])
                emotions = ['angry', 'happy', 'neutral', 'sad']
                
                # Emotion Predicted
                self.predicted_emotion = emotions[max_index]
                
                # Song Randomizer Initiated
                self.random_song_url = self.fetch_random_song(self.predicted_emotion)
                
                # Creating a YouTube Object to extract Label and video Details
                self.yt = YouTube(self.random_song_url)

                # Activating Buttons
                self.activate()

                # Actions to update UI
                self.play_song()
                self.change_thumbnail()
                self.button4["text"]=self.predicted_emotion
                break
            return

    # Mainloop for tkinter to run
    def run(self):
        self.root.mainloop()

# Constructor initializing and object creation
app = CameraApp()
app.run()
