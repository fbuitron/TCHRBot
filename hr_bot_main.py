import os
import time
import json
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = "U3YFM2A80"

# constants
AT_BOT = "<@" + BOT_ID + ">"

NUMBER_OF_REACTIONS = '3'
REBUKE_COMMAND = "boo"
CONGRAT_COMMAND = "kudos"
HELP_COMMAND = "help"
LEADER_BOARD_COMMAND = "leaderboard"

ERROR_SUFFIX = ". Type `@hr help` for instructions"

NOT_FOUND_MSGS = ['Not sure what you meant. I am still being coded by <@U02R9L8KP>! Sorry :pensive:','I am very busy right now! Maybe after a :coffee:', 'Nope']
INSTRUCTIONS_MSG = "Hi there! my name is HR. I can listen to complaints or praise between coworkers. You can raise a complaint by using the *" + REBUKE_COMMAND +"*"\
               " command or praise someone by using the *"+CONGRAT_COMMAND+"* command. Just tell me: `@hr "+CONGRAT_COMMAND+" @aric 200 He helped me with my computer` "\
               " If your message gets 3 OR + votes _@aric_ gets 200 points. On the contrary if you tell me: `@hr "+REBUKE_COMMAND+" @aric 500 he said the b word at lunch `"\
               " If your message gets 3 OR + votes _@aric_ losses 500 points. :warning: if you don't get enough votes you may loose some points!"\
               " Type `@hr "+LEADER_BOARD_COMMAND+"` to get the top 5 worst employees in the HR score."


# [{'text': '<@U3YFM2A80> kudos <@U03G12D6J> 200 She did Wackos Billboard', 'ts': '1485921472.000012', 'user': 'U02R9L8KP', 'team': 'T02RATPAE', 'type': 'message', 'channel': 'D3ZT1DZD4'}]
# [{'reaction': '+1', 'event_ts': '1485921479.839814', 'ts': '1485921479.000014', 'item': {'type': 'message', 'ts': '1485921472.000012', 'channel': 'D3ZT1DZD4'}, 'user': 'U02R9L8KP', 'item_user': 'U02R9L8KP', 'type': 'reaction_added'}]
# instantiate Slack & Twilio clients
TEST_TEXT = [{'text': '<@U3YFM2A80> kudos <@U03G12D6J> 200 She did Wackos Billboard', 'ts': '1485921472.000012', 'user': 'U02R9L8KP', 'team': 'T02RATPAE', 'type': 'message', 'channel': 'D3ZT1DZD4'}]
slack_client = SlackClient('xoxb-134531078272-AJPhKvvxEIfEgttuSA68wQAH')

list_of_operations = []

class HR_Operation:
    def __init__(self, author, isPositive, target, amount, reason, channel, timestamp):
        self.author = author
        self.isPositive = isPositive
        self.target = target
        self.amount = amount
        self.reason = reason
        self.channel = channel
        self.timestamp = timestamp
        self.votes = []
    
    def addVote(vote):
        self.votes.append(vote)

class MSG_Votes:
    def __init__(self, reaction, channel, userReacting, msg_ts):
        self.reaction = reaction
        self.channel = channel
        self.userReacting = userReacting
        self.msg_ts = msg_ts

def publish(text,channel):
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=text, as_user=True)

def handle_command(hr_operation):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    print(hr_operation.author)
    print(hr_operation.reason)
    print(hr_operation.target)
    print(hr_operation.amount)
    print(hr_operation.channel)

    list_of_operations.append(hr_operation)

    # response = NOT_FOUND_MSGS[0]
    # if (hr_operation.startswith(REBUKE_COMMAND)) or (command.startswith(CONGRAT_COMMAND)):
    response = "If you get at least *"+NUMBER_OF_REACTIONS+"* reactions, consider it done!"
    # elif command.startswith(LEADER_BOARD_COMMAND):
    #     print("What are we doing here")
    print(response)
    publish(response, hr_operation.channel)
    # slack_client.api_call("chat.postMessage", channel=channel,
                        #   text=response, as_user=True)

def handle_reaction(vote):
    #Look for the operation and add vote if found
    print("TO BE IMPLEMENTED")

def handle_help(channel):
    publish(INSTRUCTIONS_MSG, channel)

def handle_leader_board(channel):
    publish("NOT YET IMPLEMENTED :see_no_evil:", channel)

def isUser(subStr):
    return subStr.startswith("<@U")

def parse_txt(msg_str, channel):
    errorMsg = None
    isPositive = None
    target = None
    amount = None
    reason = None
    valid = False
    bySpace = msg_str.split(" ")
    if len(bySpace) >= 2:
        if bySpace[0] == AT_BOT:
            if bySpace[1] in [CONGRAT_COMMAND, REBUKE_COMMAND]:
                if bySpace[1] == CONGRAT_COMMAND:
                    isPositive = True
                else:
                    isPositive = False
                if isUser(bySpace[2]):
                    target = bySpace[2]
                    if (bySpace[3].isdigit()):
                        amount = bySpace[3]
                        if (len(bySpace) > 4):
                            reason = " ".join(bySpace[4:])
                            valid = True
                    else:
                        errorMsg = "Expected the number of points not this *"+bySpace[3]+"*"
                else:
                    errorMsg = "Need to put a user after the command instead of *"+bySpace[2]+"*"

            elif bySpace[1] == HELP_COMMAND:
                valid = True
                handle_help(channel)
            elif bySpace[1] == LEADER_BOARD_COMMAND:
                handle_leader_board(channel)
                valid = True
            else:
                errorMsg = "You used the wrong command *"+bySpace[1]+"*"
        else:
            errorMsg = "C'mon! You can do better than that"
    else:
        errorMsg = "At least you mentioned me :smiley:"
    return errorMsg, valid, target, isPositive, amount, reason

def parse_msg(msg_json):
    channel = msg_json["channel"]
    errorMSG, valid, target, isPositive, amount, reason = parse_txt(msg_json["text"], channel)
    if (errorMSG):
        print("ERROR!")
        print(errorMSG)
        msgResponse = errorMSG + ERROR_SUFFIX
        publish(msgResponse,channel)
    elif isPositive:
        channel = msg_json["channel"]
        author = msg_json["user"]
        timestamp = msg_json["ts"]
        op = HR_Operation(author,isPositive, target, amount, reason, channel, timestamp)
        handle_command(op)
    elif valid:
        # msgResponse = errorMSG + ERROR_SUFFIX
        # publish(msgResponse,channel)
        print("Is Valid")
    else:
        msgResponse = errorMSG + ERROR_SUFFIX
        publish(msgResponse,channel)

def parse_reaction(reaction_json):
    if reaction_json["item"]:
        print(reaction_json["item"])
        print(reaction_json["item"]["ts"])
        print(reaction_json["item"]["channel"])
        vote = MSG_Votes(reaction_json["reaction"], reaction_json["item"]["channel"],reaction_json["user"],reaction["item"]["ts"])
        handle_reaction(vote)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    print(slack_rtm_output)
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return parse_msg(output)
                # return output['text'].split(AT_BOT)[1].strip().lower(), \
                #        output['channel']
            # if output and 'reaction' in output:
                # parse_reaction(output)
    return None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            operation = parse_slack_output(slack_client.rtm_read())
            if operation:
                handle_command(operation)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


    
