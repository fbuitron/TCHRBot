import unittest
import json
import hr_bot_main

class Test_bot_main(unittest.TestCase):

    def test_isUser(self):
        self.assertFalse(hr_bot_main.isUser("<U42342>"))
        self.assertTrue(hr_bot_main.isUser("<@Ufdfsf>"))
    
    def test_cleanUpUsername(self):
        user1 = "<@U2342342>"
        user2 = "<U34234234>"
        user3 = "U3423423434"

        result_user1 = hr_bot_main.clean_up_user_name(user1)
        result_user2 = hr_bot_main.clean_up_user_name(user2)
        result_user3 = hr_bot_main.clean_up_user_name(user3)

        self.assertTrue(result_user1 == "U2342342")
        self.assertTrue(user2 == result_user2)
        self.assertTrue(user3 == result_user3)

    def test_parse_reaction(self):
        input_reaction_added = '{"reaction": "grinning", "event_ts": "1487305363.215871", "ts": "1487305363.000016", "item": {"type": "message", "ts": "1487305358.000014", "channel": "D3ZT1DZD4"}, "user": "U02R9L8KP", "item_user": "U02R9L8KP", "type": "reaction_added"}'
        input_reaction_deleted = '{"reaction": "grinning", "event_ts": "1487305363.215871", "ts": "1487305363.000016", "item": {"type": "message", "ts": "1487305358.000014", "channel": "D3ZT1DZD4"}, "user": "U02R9L8KP", "item_user": "U02R9L8KP", "type": "reaction_deleted"}'
        input_reaction_wrong = '{"event_ts": "1487305363.215871", "ts": "1487305363.000016", "item": {"type": "message", "ts": "1487305358.000014"}, "user": "U02R9L8KP", "item_user": "U02R9L8KP", "type": "reaction_added"}'

        vote_added = hr_bot_main.parse_reaction(json.loads(input_reaction_added))
        self.assertTrue(isinstance(vote_added,hr_bot_main.MSG_Votes))
        self.assertTrue(vote_added.reaction == 'grinning')


if __name__ == '__main__':
    unittest.main()