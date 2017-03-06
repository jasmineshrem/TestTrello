#!python

import trello_class
import nose
import unittest
import trello_token
import logging

logging.disable(logging.CRITICAL)


def get_names_of(things):
    return list(x.name for x in things)


class TestMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.t = trello_class.TrelloClass(trello_token.API_KEY, trello_token.TOKEN)
        cls.board = cls.t.create_board("Test1")

    @classmethod
    def tearDownClass(cls):
        boards = cls.t.get_open_boards()
        for board in boards:
            if board.name == "Test1" or board.name == "DeleteMe":
                cls.t.close_board(board)

    def test_get_open_boards(self):
        boards = self.t.get_open_boards()
        self.assertTrue("Test1" in get_names_of(boards))

    def test_get_board(self):
        self.assertEqual("Test1", self.t.get_board("Test1").name)

    def test_close_board(self):
        board = self.t.create_board("DeleteMe")
        self.t.close_board(board)

    def test_get_open_lists(self):
        open_lists = self.t.get_open_lists(self.board)
        for trello_list in ["To Do", "Doing", "Done"]:
            self.assertTrue(trello_list in get_names_of(open_lists))

    def test_create_list(self):
        self.t.create_list(self.board, "TestList1")
        open_lists = self.t.get_open_lists(self.board)
        self.assertTrue("TestList1" in get_names_of(open_lists))
        self.t.close_list(self.board, "TestList1")

    def test_get_list(self):
        self.t.create_list(self.board, "GetMe")
        open_lists = self.t.get_open_lists(self.board)
        print(get_names_of(open_lists))
        self.assertTrue("GetMe" in get_names_of(open_lists))

    def test_get_cards_on_board(self):
        test_list = self.t.get_list(self.board, "To Do")
        card_to_delete = self.t.create_card(self.board, test_list, "getCards")
        cards = self.t.get_cards_on_board(self.board)
        self.assertTrue("getCards" in get_names_of(cards))
        self.t.delete_card(card_to_delete)

    def test_get_cards_on_list(self):
        trello_list = self.t.get_list(self.board, "To Do")
        self.t.create_card(self.board, trello_list, "DeleteCard")
        cards = self.t.get_cards_on_list(self.board, "To Do")
        self.assertTrue("DeleteCard" in get_names_of(cards))

    def test_create_card(self):
        trello_list = self.t.get_list(self.board, "To Do")
        self.t.create_card(self.board, trello_list, "DeleteCard")
        cards = self.t.get_cards_on_list(self.board, "To Do")
        self.assertTrue("DeleteCard" in get_names_of(cards))
