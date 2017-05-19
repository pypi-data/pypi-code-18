def on_member_joined_channel(msg, server):
    if msg.get("channel") == "C0LKKMZC0":
        print("posting message to user {}".format(msg['user']))
        server.slack.post_message(msg['user'],
            "Welcome to Ad Hoc's #public channel! We're here for your technical questions about completing the homework. If you have non-technical questions, contact us at recruiting.group@adhocteam.us. Please use your real identity in all communications.",
            username="Ad Hoc Welcome Bot",
            icon_emoji=":adhoc:")
