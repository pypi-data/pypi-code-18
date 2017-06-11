from typing import List

from stuffer.core import MultiAction, Action

from stuffer import apt


class SpotifyClient(MultiAction):
    def children(self) -> List[Action]:
        return [
            apt.SourceList("partner", "deb http://archive.canonical.com/ubuntu xenial partner"),
            apt.Install("spotify-client")
        ]
