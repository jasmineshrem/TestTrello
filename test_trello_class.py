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
        cls.t.create_board("Test1")

    @classmethod
    def tearDownClass(cls):
        cls.t.close_board("Test1")

    def test_get_open_boards(self):
        boards = self.t.get_open_boards()
        self.assertTrue("Test1" in get_names_of(boards))

    def test_get_board(self):
        self.assertEqual("Test1", self.t.get_board("Test1").name)

    def test_close_board(self):
        self.t.create_board("DeleteMe")
        self.t.close_board("DeleteMe")

    def test_get_open_lists(self):
        open_lists = self.t.get_open_lists("Test1")
        for trello_list in ["To Do", "Doing", "Done"]:
            self.assertTrue(trello_list in get_names_of(open_lists))

    def test_create_list(self):
        self.t.create_list("Test1", "TestList1")
        open_lists = self.t.get_open_lists("Test1")
        self.assertTrue("TestList1" in get_names_of(open_lists))
        self.t.close_list("Test1", "TestList1")

    def test_get_list(self):
        self.t.create_list("Test1", "GetMe")
        open_lists = self.t.get_open_lists("Test1")
        self.assertTrue("GetMe" in get_names_of(open_lists))
        self.t.close_list("Test1", "GetMe")

    def test_get_cards_on_board(self):
        self.t.add_card("Test1", "To Do", "getCards")
        cards = self.t.get_cards_on_board("Test1")
        self.assertTrue("getCards" in get_names_of(cards))

    def test_get_cards_on_list(self):
        self.t.add_card("Test1", "To Do", "getCardsOnList")
        cards = self.t.get_cards_on_list("Test1", "To Do")
        self.assertTrue("getCardsOnList" in get_names_of(cards))

    def test_add_card(self):
        self.t.add_card("Test1", "To Do", "DeleteCard")
        cards = self.t.get_cards_on_list("Test1", "To Do")
        self.assertTrue("DeleteCard" in get_names_of(cards))

    def test_get_card(self):
        self.assertTrue(self.t.get_card("DeleteCard", "Test1"))
