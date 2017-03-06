#!python

import trello_board_builder
import unittest
import trello_class
import logging
import nose
import trello_token

logging.disable(logging.CRITICAL)

motherboard = {
        "System 1": ["System 1 - Task 1", "System 1 - Task 2", "System 1 - Task 3"],
        "System 2": ["System 2 - Task 1", "System 2 - Task 2", "System 2 - Task 3"],
        "System 3": ["System 3 - Task 1", "System 3 - Task 2", "System 3 - Task 3"]
        }


def get_names_of(things):
    return list(x.name for x in things)


class TestMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.t = trello_class.TrelloClass(trello_token.API_KEY, trello_token.TOKEN)
        cls.masterboard = cls.t.create_board("motherboard")
        for trello_list in cls.t.get_open_lists(cls.masterboard):
            cls.t.close_list(cls.masterboard, trello_list.name)
        for list_name, cards in motherboard.items():
            trello_list = cls.t.create_list(cls.masterboard, list_name)
            for card in cards:
                cls.t.create_card(cls.masterboard, trello_list, card)

    @classmethod
    def tearDownClass(cls):
        for board in cls.t.get_open_boards():
            if board.name in ["motherboard", "System 1", "System 2", "System 3"]:
                cls.t.close_board(board)

    def test_create_new_boards_from_lists_on_source_board(self):
        new_boards = trello_board_builder.create_new_boards_from_lists_on_source_board(self.t, self.masterboard)
        self.assertCountEqual(["System 1", "System 2", "System 3"], get_names_of(new_boards))

    def test_create_card_with_url_to_new_boards(self):
        new_boards = trello_board_builder.create_new_boards_from_lists_on_source_board(self.t, self.masterboard)
        trello_board_builder.create_cards_with_url_to_new_boards(self.t, self.masterboard, new_boards)
        for card in ["System 1", "System 2", "System 3"]:
            self.assertTrue(card in get_names_of(self.t.get_cards_on_board(self.masterboard)))

    def test_clone_cards_to_new_boards(self):
        new_boards = trello_board_builder.create_new_boards_from_lists_on_source_board(self.t, self.masterboard)
        new_cards = trello_board_builder.clone_cards_to_new_boards(self.t, self.masterboard, new_boards)
        names_of_cards = get_names_of(new_cards)
        result = [
                'System 2 - Task 1', 'System 2 - Task 2', 'System 2 - Task 3',
                'System 1 - Task 1', 'System 1 - Task 2', 'System 1 - Task 3',
                'System 3 - Task 1', 'System 3 - Task 2', 'System 3 - Task 3']
        # self.fail(new_cards)
        self.assertCountEqual(result, names_of_cards)
