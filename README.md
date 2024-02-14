# Moodbot - Emotion-based Music Player

## Overview
Moodbot is a simple emotion-based music player that leverages facial emotion detection to recommend and play music based on the user's mood. The application captures the user's facial expressions through the computer's camera, determines the emotion detected, and then plays a corresponding music playlist.

## Features
- **Real-time Emotion Detection:** Utilizes a pre-trained deep learning model to detect facial emotions in real-time.
- **Emotion-Genre Mapping:** Associates detected emotions with predefined music genres (e.g., happy, sad, angry, neutral).
- **YouTube Playlist Integration:** Fetches random songs from predefined YouTube playlists associated with each emotion.
- **Graphical User Interface (GUI):** A user-friendly GUI built using Tkinter for a seamless experience.
- **Music Playback:** Integrates with the `mpv` media player to play the selected music.

## Requirements
Make sure you have the required Python libraries installed. You can install them using the following command:
```bash
pip3 install -r requirements.txt
```

## Usage
1. Run the `main.py` script to launch the Moodbot application.
2. The camera feed will display in the GUI, and the application will continuously analyze facial expressions.
3. Press the "Press me to detect" button to initiate emotion detection manually.
4. Alternatively, choose an emotion from the dropdown menu for manual music selection.
5. The application will fetch a random song from the corresponding playlist and display its thumbnail and details.
6. Press the "PLAY" button to start playing the selected song.
