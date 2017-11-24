from __future__ import print_function
import os
import time
from slackclient import SlackClient
from packyou.github.ur1katz.pychromecast import pychromecast as urpycast
from packyou.github.ur1katz.pychromecast.controllers.youtube import YouTubeController as urytc


BOT_ID = os.environ.get('BOT_ID')
AT_BOT = "<@" + BOT_ID + ">"
READ_WEBSOCKET_DELAY = 1


class SlackBot:
    # COMMANDS = {
    #     'DO': 'do',
    #     'FINDCASTS': 'find chromecasts'
    # }

    def __init__(self):
        self.known_casts = {}
        self.start_up_slack_bot()

    def find_chromecasts(self):
        self.known_casts = {}
        for cast in urpycast.get_chromecasts():
            self.known_casts[cast.device.friendly_name] = cast

    def cast_name_list(self):
        cast_names = []
        for cast_name in self.known_casts.keys():
            cast_names.append(cast_name)
        return cast_names

    def handle_command(self, command, channel):
        """
            Receives commands directed at the bot and determines if they
            are valid commands. If so, then acts on the commands. If not,
            returns back what it needs for clarification.
        """

        if command.startswith('do'):
            response = "Sure...write some more code then I can do that!"
        elif command.startswith('find casts'):
            self.find_chromecasts()
            response = "Looking for some chromecasts!  I found %s!" % self.cast_name_list()
        else:
            response = "Not sure what you mean. Feel free to ask for *HELP* though."

        self.slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    def parse_slack_output(self, slack_rtm_output):
        """
            The Slack Real Time Messaging API is an events firehose.
            this parsing function returns None unless a message is
            directed at the Bot, based on its ID.
        """
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and AT_BOT in output['text']:
                    # return text after the @ mention, whitespace removed
                    return output['text'].split(AT_BOT)[1].strip().lower(), \
                           output['channel']
        return None, None

    def start_up_slack_bot(self):
        self.slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
        if self.slack_client.rtm_connect():
            print('chromecast bot up and running')
            while True:
                command, channel = self.parse_slack_output(self.slack_client.rtm_read())
                if command and channel:
                    print("Handling Command [%s] on Channel [%s]" % (command, channel))
                    self.handle_command(command, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection Failed")


def main():
    bot = SlackBot()

if __name__ == "__main__":
    main()
