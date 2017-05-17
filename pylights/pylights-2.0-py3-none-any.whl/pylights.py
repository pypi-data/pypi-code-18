import pyphue # Manages phillips hue lights
import time # Manages timing of notes
import librosa # Manages detection of onsets and onset strength
import pickle # Manages saving/loading of data
import os # Manages directories
import random # Manages random color generation
import numpy as np # Manages arrays and data returned from Librosa
from pygame import mixer # Plays mp3 files

class PyLights:
    def __init__(self, philipsBridge):
        self.bridge = philipsBridge
        self.harmonicLights = []
        self.percussiveLights = []

    def run(self):
        colorTheme = random.randint(0, 65535)
        lastBigBeat = 0
        primaryBrightness = 255
        tick = 0
        primaryOff = False

        for item in self.harmonicLights:
            if item[1]:
                self.bridge.setHue(item[0], colorTheme + random.randint(-5000, 5000))
                self.bridge.setSaturation(item[0], 255)
            self.bridge.turnOn(item[0])
            self.bridge.setBrightness(item[0],255)

        for item in self.percussiveLights:
            if item[1]:
                self.bridge.setHue(item[0], colorTheme + random.randint(-5000, 5000))
                self.bridge.setSaturation(item[0], 255)
            self.bridge.turnOn(item[0])
            self.bridge.setBrightness(item[0], 255)

        starttime = time.time()

        mixer.init()
        mixer.music.load(os.path.join(self.songPath, "%s" % self.fileName))

        #self.beat_times = map(lambda x: round(x * 500)/500, self.beat_times)
        #self.beat_times = list(set(self.beat_times)) #Eliminate notes that are very very similar to prevent lights from being triggered twice
        self.beat_times.sort()

        #self.harmonic_beat_times = map(lambda x: round(x * 500)/500, self.harmonic_beat_times)
        #self.percussive_beat_times = map(lambda x: round(x * 500)/500, self.percussive_beat_times)

        mixer.music.play()
        time.sleep(self.beat_times[0])
        for i, beatTime in enumerate(self.beat_times):
            tick = (tick + 1) % 2

            colorTheme = random.randint(0, 65535)

            harmonicBeat = bool(self.beat_times[i] in self.harmonic_beat_times)
            percussiveBeat = bool(self.beat_times[i] in self.percussive_beat_times)

            if harmonicBeat: # If a percussive beat is detected in this onset, fire off percussive lights
                brightnessValueFlash = min((PyLights.returnBrightness(self, tick, i)) + 15, 255)
                brightnessValue = PyLights.returnBrightness(self, tick, i)

                for light in self.harmonicLights:
                    if (light[3] == False):
                        light[3] = True
                        self.bridge.turnOn(light[0])

                    if light[1]:
                        self.bridge.setHue(light[0], colorTheme + random.randint(-5000, 5000))

                    if light[2]:
                        self.bridge.setBrightness(light[0], brightnessValueFlash)
                        self.bridge.setBrightness(light[0], 0)
                    else:
                        if (brightnessValue > 1):
                            self.bridge.setBrightness(light[0], brightnessValue)
                        else:
                            self.bridge.setBrightness(light[0], brightnessValue)
                            if (light[3]):
                                light[3] = False
                                self.bridge.turnOff(light[0])
            else:
                for light in self.harmonicLights:
                    if light[2]:
                        if (self.bridge.getBrightness(light[0]) == 0 and light[3]):
                            light[3] = False
                            self.bridge.turnOff(light[0])
                        else:
                            self.bridge.setBrightness(light[0], 0)

            if percussiveBeat: # If a percussive beat is detected in this onset, fire off percussive lights
                brightnessValueFlash = min((PyLights.returnBrightness(self, tick, i)) + 15, 255)
                brightnessValue = PyLights.returnBrightness(self, tick, i)

                for light in self.percussiveLights:
                    if (light[3] == False):
                        light[3] = True
                        self.bridge.turnOn(light[0])

                    if light[1]:
                        self.bridge.setHue(light[0], colorTheme + random.randint(-5000, 5000))

                    if light[2]:
                        self.bridge.setBrightness(light[0], brightnessValueFlash)
                        self.bridge.setBrightness(light[0], 0)
                    else:
                        if (brightnessValue > 1):
                            self.bridge.setBrightness(light[0], brightnessValue)
                        else:
                            self.bridge.setBrightness(light[0], brightnessValue)
                            if (light[3]):
                                light[3] = False
                                self.bridge.turnOff(light[0])
            else:
                for light in self.percussiveLights:
                    if light[2]:
                        if (self.bridge.getBrightness(light[0]) == 0 and light[3]):
                            light[3] = False
                            self.bridge.turnOff(light[0])
                        else:
                            self.bridge.setBrightness(light[0], 0)

            if (i < len(self.beat_times) - 1):
                timeToNextNote = max(beatTime - (time.time() - starttime), 0)
                time.sleep(timeToNextNote)

    def loadLight(self, lightId, harmonic=True, percussive=True, color=False, flash=False):
        if harmonic:
            if [lightId, color, flash] not in self.harmonicLights:
                self.harmonicLights.append([lightId, color, flash, True]) #Append light id to the primary light list, include color support info
        if percussive:
            if [lightId, color, flash] not in self.percussiveLights:
                self.percussiveLights.append([lightId, color, flash, True]) #Append light id to the primary light list, include color support info

    def loadAudio(self, fileName, songPath=None, dataPath=None, saveAndLoad=True, onsets=False): # Allows you to select an audio file, chose what path to look for the audio file, what path to save compiled data, and if to save compiled data
        if songPath == None:
            songPath = os.path.join(os.getcwd() + "/Songs/")

        if dataPath == None:
            dataPath = os.path.join(os.getcwd() + "/SongData/")

        self.songPath = songPath
        self.dataPath = dataPath
        self.fileName = fileName

        if not os.path.exists(songPath):
            os.makedirs(songPath)

        if not os.path.exists(dataPath):
            os.makedirs(dataPath)

        if (saveAndLoad):
            if (os.path.isfile(os.path.join(dataPath, "%s.txt" % fileName))):
                with open(os.path.join(dataPath, "%s.txt" % fileName), 'rb') as file:
                    readSongData = pickle.load(file)

                self.o_env = readSongData[0]
                self.harmonic_beat_times = readSongData[1]
                self.percussive_beat_times = readSongData[2]

            else:
                y, sr = librosa.load(os.path.join(songPath, "%s" % fileName))
                y_harmonic, y_percussive = librosa.effects.hpss(y)

                #Onsets
                #self.o_env = librosa.onset.onset_strength(y=y, sr=sr).tolist()
                #self.harmonic_beat_times = librosa.frames_to_time(librosa.onset.onset_detect(y=y_harmonic, sr=sr), sr=sr).tolist()
                #self.percussive_beat_times = librosa.frames_to_time(librosa.onset.onset_detect(y=y_percussive, sr=sr), sr=sr).tolist()

                # Beats
                self.o_env = librosa.onset.onset_strength(y=y, sr=sr).tolist()
                self.harmonic_beat_times = librosa.frames_to_time(librosa.beat.beat_track(y=y_harmonic, sr=sr)[1], sr=sr).tolist()
                self.percussive_beat_times = librosa.frames_to_time(librosa.beat.beat_track(y=y_percussive, sr=sr)[1], sr=sr).tolist()

                writeSongData = [self.o_env, self.harmonic_beat_times, self.percussive_beat_times]

                with open(os.path.join(dataPath, "%s.txt" % fileName), 'wb') as file:
                    pickle.dump(writeSongData, file)
        else:
            y, sr = librosa.load(os.path.join(songPath, "%s" % fileName))
            y_harmonic, y_percussive = librosa.effects.hpss(y)

            #Onsets
            #self.o_env = librosa.onset.onset_strength(y=y, sr=sr).tolist()
            #self.harmonic_beat_times = librosa.frames_to_time(librosa.onset.onset_detect(y=y_harmonic, sr=sr), sr=sr).tolist()
            #self.percussive_beat_times = librosa.frames_to_time(librosa.onset.onset_detect(y=y_percussive, sr=sr), sr=sr).tolist()

            # Beats
            self.o_env = librosa.onset.onset_strength(y=y, sr=sr).tolist()
            self.harmonic_beat_times = librosa.frames_to_time(librosa.beat.beat_track(y=y_harmonic, sr=sr)[1], sr=sr).tolist()
            self.percussive_beat_times = librosa.frames_to_time(librosa.beat.beat_track(y=y_percussive, sr=sr)[1], sr=sr).tolist()

        self.beat_times = self.harmonic_beat_times + self.percussive_beat_times
        self.beat_times.sort()

    def returnBrightness(self, tick, beatNumber):
        if (tick == 1):
            returnBrightnessValue = 255 - int(275 - (100 / (self.o_env[beatNumber] + 0.01)))
        else:
            returnBrightnessValue = int(275 - (100 / (self.o_env[beatNumber] + 0.01)))

        if (returnBrightnessValue < 125):
            returnBrightnessValue -= 50
        else:
            returnBrightnessValue += 50

        returnBrightnessValue = min(returnBrightnessValue, 255)
        returnBrightnessValue = max(returnBrightnessValue, 0)

        return returnBrightnessValue

# EXAMPLE CODE

# setIp = "192.168.1.1" # Change this to the IP of your philips hue bridge
# userId = "tLWZE6rPwKQbnYm-S6Gx9u5FVT8oJd9r5YYArxPL" # Change this to your user ID attained from your philips hue bridge, this way you do not have to constantly authorize
# myHue = pyphue.PyPHue(ip = setIp, user = userId, AppName = 'PyPhue', DeviceName = 'Desktop:YourUserName', wizard = False) # Use the PyPhue module to connect to your bridge

# pylights = PyLights(myHue)
# pylights.loadLight(lightId = '3', primary=True, color=True)
# pylights.loadLight(lightId = '2', primary=False, color=False)
# pylights.loadLight(lightId = '1', primary=False, color=False)
# pylights.loadAudio(fileName = "CurtainsDown.mp3", songPath = os.path.abspath("CustomSongPath"), dataPath = os.path.abspath("CustomDataPath"), saveAndLoad=True)
# pylights.run()