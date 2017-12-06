from __future__ import print_function
import os
import time
import re
from slackclient import SlackClient
from packyou.github.ur1katz.pychromecast import pychromecast as urpycast
from packyou.github.ur1katz.pychromecast.controllers.youtube import YouTubeController as urytc


BOT_ID = os.environ.get('BOT_ID')
AT_BOT = "<@" + BOT_ID + ">"
EMOJI_PATTERN = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')

class ChromeCastHandler:
    def __init__(self):
        self.known_casts = {}

    def cast_name_list(self):
        cast_names = []
        for cast_name in self.known_casts.keys():
            cast_names.append(cast_name)
        return cast_names

    # Return Cast by name, or false if not found
    def fetch_cast(self, cast_name):
        if cast_name in self.known_casts:
            return self.known_casts[cast_name]
        else:
            return None

    def find_chromecasts(self):
        self.known_casts = {}
        for cast in urpycast.get_chromecasts():
            self.known_casts[re.sub(EMOJI_PATTERN, '', cast.device.friendly_name).strip()] = SlackCast(cast)

    def send_video_to_chromecast(self, cast_name, youtube_id):
        cast = self.fetch_cast[cast_name]
        if cast:
            cast.play_youtube_video(youtube_id)
            return True
        else:
            return False

class SlackCast:
    def __init__(self, cast):
        self.cast = cast
        self.youtube_controller = urytc()
        self.cast.register_handler(self.youtube_controller)

    def play_youtube_video(self, youtube_id):
        if not self.youtube_controller.in_session:
            self.youtube_controller.play_video(youtube_id)
        else:
            self.youtube_controller.add_to_queue(youtube_id)



class SlackBot:
    def __init__(self, read_websocket_delay = 1):
        self.read_websocket_delay = read_websocket_delay
        self.chromecast_handler = ChromeCastHandler()

    def handle_command(self, command, channel):
        downcase_command = command.lower()
        try:
            if downcase_command.startswith('find casts'):
                self.chromecast_handler.find_chromecasts()
                response = "Looking for some chromecasts!  I found %s!" % self.chromecast_handler.cast_name_list()
            elif downcase_command.startswith('list casts'):
                response = "I'm a smart bot!  I know about these chromecasts: %s!" % self.chromecast_handler.cast_name_list()
            elif downcase_command.startswith('play'):
                response = self.parse_play_command(command)
            elif downcase_command.startswith('help'):
                response = "What can this bot do?\n" \
                           "`help` will display this info\n" \
                           "`find casts` will tell the bot to find the chromecasts it can access\n" \
                           "`list casts` will tell the bot to reveal the chromecasts it know\n" \
                           "`play [youtube id] on [cast]` plays a video on the named chromecast"
            else:
                response = "Not sure what you mean. Feel free to ask for *HELP* though."
        except Exception as e:
            print(e)
            response = "Man it looks like Travis coded the slackbot poorly.  You should tell him about it @quasimonomial"

        self.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    def parse_play_command(self, command):
        youtube_id = command.split()[1]
        cast_name = command.split(' on ')[1]
        if self.chromecast_handler.send_video_to_chromecast(cast_name, youtube_id):
            return 'playing song'
        else:
            return 'chormecast not found'


    def parse_slack_output(self, slack_rtm_output):
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and AT_BOT in output['text']:
                    return output['text'].split(AT_BOT)[1].strip(), output['channel']
        return None, None

    def start_up_slack_bot(self, initial_find_casts = False):
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
        if self.slack_client.rtm_connect():
            print('chromecast bot up and running')
            if initial_find_casts:
                self.chromecast_handler.find_chromecasts()
            while True:
                command, channel = self.parse_slack_output(self.slack_client.rtm_read())
                if command and channel:
                    print("Handling Command [%s] on Channel [%s]" % (command, channel))
                    self.handle_command(command, channel)
                time.sleep(self.read_websocket_delay)
        else:
            print("Connection Failed")


def main():
    bot = SlackBot()
    bot.start_up_slack_bot(True)


if __name__ == "__main__":
    main()
