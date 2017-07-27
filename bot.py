import slackclient
import time
import random

SOCKET_DELAY = 1

slackName = "git_link"
slackToken = "xoxb-215044459410-wC4FoEGTJLBC1EVWBo1gexH1"
botID = "U6B1ADHC2"

pyChat_sc = slackclient.SlackClient(slackToken)


def is_private(event):
    return event.get("channel").startswith("D")


def get_mention(user):
    return '<@{user}>'.format(user=user)

pyChat_slack_mention = get_mention(botID)


def for_bot(event):
    type = event.get("type")
    if type and type == "message" and not(event.get("user") == slackToken):
        if is_private(event):
            return True
        text = event.get("text")
        channel = event.get("channel")
        if pyChat_slack_mention in text.strip().split():
            return True


def is_hi(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(each in tokens for each in ['hello', 'bonjour', 'hey', 'hi', 'sup', 'morning', 'hola', 'ohai', 'yo'])


def is_bye(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(each in tokens for each in ['bye', 'goodbye', 'revoir', 'adios', 'later', 'cya'])


#def get_ID(message):



def say_hi(user_mention):
    response_template = random.choice(['Hi, {mention} I will notify you '
                                       'when there is a github pull request to be merged'])
    return response_template.format(mention=user_mention)


def say_bye(user_mention):
    response_template = random.choice(['see you later {mention}', 'adios amigo', 'Bye {mention}!', "Glad to help!"])
    return response_template.format(mention=user_mention)


def handle_message(message, user, channel):
    if is_hi(message):
        user_mention = get_mention(user)
        post_message(message=say_hi(user_mention), channel=channel)
    elif is_bye(message):
        user_mention = get_mention(user)
        post_message(message=say_bye(user_mention), channel=channel)


def post_message(message, channel):
    pyChat_sc.api_call('chat.postMessage', channel=channel, text=message, as_user=True)


def run():
    if pyChat_sc.rtm_connect():
        print("[.] git_link is ON...")
        while True:
            event_list = pyChat_sc.rtm_read()
            if len(event_list)>0:
                for event in event_list:
                    print(event)
                    if for_bot(event):
                        handle_message(message=event.get("text"), user=event.get("user"), channel=event.get("channel"))
                    time.sleep(SOCKET_DELAY)
    else:
        print("[!] Connection to Slack failed.")

if __name__ == '__main__':
    run()
