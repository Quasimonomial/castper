from __future__ import print_function
import time
import pychromecast
from packyou.github.ur1katz.pychromecast import pychromecast as urpycast
from packyou.github.ur1katz.pychromecast.controllers.youtube import YouTubeController as uryt

class Listener:
    def __init__(self):
        self.known_casts = {}

    def find_chromecasts(self):
        self.known_casts = {}
        for cast in urpycast.get_chromecasts():
            self.known_casts[cast.device.friendly_name] = cast

    def print_state(self):
        print(self.known_casts)

    def send_video_to_chromecast(self, cast_name, youtube_id):
        youtube_controller = uryt()
        cast = self.known_casts[cast_name]
        cast.register_handler(youtube_controller)
        youtube_controller.play_video(youtube_id)


def main():
    listener = Listener()
    listener.find_chromecasts()
    listener.send_video_to_chromecast('Hackitorium 🌉🌈🎙🎶', 'eqzxBHSKVsQ')

if __name__ == "__main__":
    main()
