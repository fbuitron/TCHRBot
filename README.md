# TCHRBot
HRBot is an idea that came at work about having a pointing system based on HR friendly comments or actions among ourselves.

##Goal
Being able to keep count on a leaderboard of slack users. Users can suggest another one to gain points or to lose points. Other members have to vote for the points to actually be increased or decreased.

## How does it work?
A user can suggest an increment or decrement of points to other users. After that it is needed 3 reactions from other memebers of the channel for the request to have an impact.

Request look like:

`@hr <COMMAND> <TARGET_USER> <POINTS> <REASON>`

There are some rules for this reactions though:
- The user who sent the request cannot react to it's own message
- The target user cannot vote on a request that he has been tagged.
- A user can only vote once

All this rules are applied by hr bot!

## Example Interaction

```@hr kudos @jsmith 200 For helping me with my computer```

This command is to suggest an increment of **200** points to the user **@jsmith**.

```@hr boo @jsmith 100 For saying the f word at lunch today```

This command is to suggest a decrease of **100** points to the user **@jsmith**.

```@hr leaderboard``` 

This command will print out a table with users and points.

```@hr help```

Prints a paragraph explaining the above commands.

## Requirements

- Python 2.7
- Slack Token and ID (Env Variables)



