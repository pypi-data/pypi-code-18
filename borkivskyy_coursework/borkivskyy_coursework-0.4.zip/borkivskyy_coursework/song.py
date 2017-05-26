class Song:
    """
    Class represent song.
    """
    def __init__(self, name, artist, album, length):
        self.name = name
        self.artist = artist
        self.album = album
        self.length = length

    def __str__(self):
        return self.name

    def time_to_min(self):
        """
        Change length of the song from milliseconds to minutes

        :return: time in minutes
        """
        seconds = self.length // 1000
        min = seconds // 60
        scd = seconds % 60
        str_scd = str(min)+":"+str(scd)
        return str_scd

    def info(self):
        print(self.name + " | " + self.artist + " | " + self.time_to_min())
