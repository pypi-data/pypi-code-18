import itunespy
from borkivskyy_coursework.arrays import DynamicArray
from borkivskyy_coursework.song import Song
import random


def input_data():
    """
    None -> array, array

    Return user's input and check if such data exist.

    :return: artists and genres arrays
    """
    artists_list = DynamicArray()
    genres_list = DynamicArray()
    print("Enter at least one artist")
    while True:
        artist_inp = input("Enter artist's name or Enter to finish: ")
        try:
            if len(artist_inp) > 0 or len(artists_list) == 0:
                artist = itunespy.search_artist(artist_inp)
                artists_list.append(artist)
            else:
                break
        except LookupError:
            print("There is no such artist in iTunes database. Try someone else.")
            continue

    while True:
        answer = input("Would you like to know genres of your artists?(yes/no) ")
        if answer.lower() == "no":
            break
        elif answer.lower() == "yes":
            genres_set = set()
            for i in artists_list:
                for a in i[0].get_albums():
                    genres_set.add(a.primary_genre_name)

            genres_set = sorted(list(genres_set))
            print("\nGenres of your artists:\n")
            for g in genres_set:
                print(g)
            print("\n")
            break
        else:
            print("Invalid answer!")
            continue


    while True:
        genre = input("Enter genre or Enter to finish: ")
        if len(genre) > 0 or len(genres_list) == 0:
            if len(genre) == 0:
                continue
            ch = False
            for art in artists_list:
                albums = art[0].get_albums()
                for album in albums:
                    if album.primary_genre_name == genre:
                        ch = True
            if not ch:
                print("Your artist does not work in this genre. Try another one.")
                continue
            genres_list.append(genre)
        elif len(genre) == 0:
            break

    return artists_list, genres_list


def time_estimate():
    """
    None -> (int)

    Estimate time of journey. User enters time or distance(speed estimates automatically)

    :return: time of journey in milliseconds.
    """
    while True:
        mode = input("What you exactly know about journey?(time/distance)")

        if mode.lower() == "time":
            while True:
                time = input("Enter the time in format: 'hh:mm' ")
                ch = False
                for i in range(5):
                    if i != 2 and time[i] not in "0123456789":
                        print("Invalid number! Try one more time!")
                        ch = True

                    if i == 2 and time[i] != ":":
                        print("Invalid time format! Try one more time!")
                        ch = True
                if ch:
                    continue

                return (((int(time[0:2]) * 60) + int(time[3:5])) * 60000)

        elif mode.lower() == "distance":
            speeds = {"hiking" : 5, "car" : 60, "train" : 100, "plane" : 150}
            while True:
                try:
                    distance = float(input("Enter the distance(km): "))
                    break
                except ValueError:
                    print("Invalid input! Try one more time!")
                    continue

            while True:
                transport = input("What transport you will use?(hiking/car/train/plane)")
                if transport not in speeds:
                    print("Invalid transport! Try one more time!")
                    continue
                else:
                    speed = speeds[transport]
                    break

            return int(distance / speed * 3600000)

        else:
            print("Incorrect input! Try one more time!")
            continue


def get_songs(artists_list, genres_list):
    """
    Check if songs are valid and add them to the array; counts length of all songs

    :param artists_list: list of artists
    :param genres_list: list of genres
    :return: list of Song-objects, total legnth of songs
    """
    songs = DynamicArray()
    length = 0
    for artist_inp in artists_list:
        artist = itunespy.search_artist(artist_inp[0].artist_name)
        albums = artist[0].get_albums()
        for album in albums:
            if album.primary_genre_name in genres_list:
                try:
                    album_search = itunespy.search_album(album.collection_name)
                except LookupError:
                    continue
                tracks = album_search[0].get_tracks()
                for track in tracks:
                    if track.primary_genre_name in genres_list:
                        print(track)
                        songs.append(Song(track.track_name, track.artist_name, track.collection_name, track.track_time))
                        length += track.track_time

    return songs, length


def build_playlist(songs, length, time):
    """

    :param songs: list of songs
    :param length: total length of all songs
    :param time: estimated time
    :return: songs which are included in playlist
    """
    result_songs = DynamicArray()

    ch = time <= length

    while time > 0:
        song = random.choice(songs)
        time -= song.length
        result_songs.append(song)
        if ch:
            songs.remove(song)

    return result_songs


def main():
    """
    Main process
    """
    print("\n--- BEGINNING ---\n")

    print("Input process...\n")
    artists_list, genres_list = input_data()
    print("\n--------------\n")

    print("Time estimating process...\n")
    time = time_estimate()
    print("\n--------------\n")

    print("Getting songs process...\n")
    songs, length = get_songs(artists_list, genres_list)
    print("\n--------------\n")

    print("Building playlist process...\n")
    playlist = build_playlist(songs, length, time)
    print("\n--------------\n")


    print("Your playlist:\n")
    for i in playlist:
        i.info()

    print("\n--- THE END ---\n")


main()
