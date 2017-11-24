# Chromecast Slackbot


### Purpose
This is a slack bot that can communicate with a Chromecast to play videos.  The bot must live on the same lan as the Chromecast.

### Dependencies
* Coded for Python 3.
* This bot uses [pychromecast](https://github.com/balloob/pychromecast).  We use [this](https://github.com/ur1katz/pychromecast) fork due to broken YouTube compatibility.  See discussion [here](https://www.bountysource.com/issues/27672511-youtubecontroller-doesn-t-display-video).
* [Pack You](https://github.com/llazzaro/packyou) is used to handle github dependencies.
* The Python [Slack Client](https://github.com/slackapi/python-slackclient) is used for slack.


### Set Up
Slack Bot functionality based off of [this](https://medium.com/@julianmartinez/how-to-write-a-slack-bot-with-python-code-examples-4ed354407b98) tutorial.  We require both a `BOT_ID` and a `SLACK_BOT_TOKEN` to be set as environment variables.

You will need to:
* `pip install slackclient`
* `pip install packyou`

or `pip3`

Running the `python3 chromecast_slackbot.py` will create an instance of the bot and run the necessary set up functions.

### Commands
* `help` displays help information
* `find casts` tells the bot to look for Chromecasts on it's network.  This will overwrite any casts it knows.  This must be run in order for the bot to know any Chromecasts for it to cast to.
* `list casts` tells the bot to list the titles of the casts it knows
* `play [youtube id] on [cast]` plays a youtube video on the indicated Chromecast.  The cast must be a Chromecast that the bot knows about; you can find these with `list casts`.  A youtube id is the unique id in the youtube URL following `v=`
