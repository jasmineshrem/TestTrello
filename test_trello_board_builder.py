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
        trello_board_builder.delete_initial_board_lists(cls.t, cls.masterboard)
        for list_name, cards in motherboard.items():
            trello_list = cls.t.create_list(cls.masterboard, list_name)
            list(cls.t.create_card(cls.masterboard, trello_list, card) for card in cards)
        cls.new_boards = trello_board_builder.create_new_boards_from_lists_on_source_board(cls.t, cls.masterboard)
        list(trello_board_builder.delete_initial_board_lists(cls.t, board) for board in cls.new_boards)

    @classmethod
    def tearDownClass(cls):
        list(cls.t.close_board(board) for board in cls.t.get_open_boards() if board.name in [
            "motherboard", "System 1", "System 2", "System 3"])

    def test_create_new_boards_from_lists_on_source_board(self):
        self.assertCountEqual(["System 1", "System 2", "System 3"], get_names_of(self.new_boards))

    def test_delete_initial_board_lists(self):
        old_lists = ["To Do", "Doing", "Done"]
        for old_list in old_lists:
            self.assertTrue(old_list not in self.t.get_open_lists(self.masterboard))

    def test_create_lists_on_new_boards(self):
        created_lists = trello_board_builder.create_lists_on_new_boards(self.t, self.new_boards)
        result = [
                  'In Progress', 'Coding Done', 'QA', 'Final QA', 'QA Approved', 'In Progress',
                  'Coding Done', 'QA', 'Final QA', 'QA Approved', 'In Progress', 'Coding Done',
                  'QA', 'Final QA', 'QA Approved'
                  ]
        self.assertCountEqual(result, get_names_of(created_lists))

    def test_create_card_with_url_to_new_boards(self):
        trello_board_builder.create_cards_with_url_to_new_boards(self.t, self.masterboard, self.new_boards)
        for card in ["System 1", "System 2", "System 3"]:
            self.assertTrue(card in get_names_of(self.t.get_cards_on_board(self.masterboard)))

    def test_clone_cards_to_new_boards(self):
        new_cards = trello_board_builder.clone_cards_to_new_boards(self.t, self.masterboard, self.new_boards)
        names_of_cards = get_names_of(new_cards)
        result = [
                'System 2 - Task 1', 'System 2 - Task 2', 'System 2 - Task 3',
                'System 1 - Task 1', 'System 1 - Task 2', 'System 1 - Task 3',
                'System 3 - Task 1', 'System 3 - Task 2', 'System 3 - Task 3'
                 ]
        self.assertCountEqual(result, names_of_cards)
