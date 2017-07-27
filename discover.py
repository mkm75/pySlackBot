import slackclient

slackName = "git_link"
slackToken = "xoxb-215044459410-wC4FoEGTJLBC1EVWBo1gexH1"

pyChat_sc = slackclient.SlackClient(slackToken)

is_ok = pyChat_sc.api_call("users.list").get("ok")
print(is_ok)

if is_ok:
    for user in pyChat_sc.api_call("users.list").get("members"):
        if user.get("name") == slackName:
            print(user.get("id"))




