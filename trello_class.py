#!python

from trello import TrelloClient


class TrelloClass:

    def __init__(self, api_key, token):
        self.client = TrelloClient(api_key=api_key, token=token)

    def get_client(self):
        return self.client

    def get_open_boards(self):
        return self.client.list_boards(board_filter="open")

    def get_board(self, board_name):
        return next(self.get_board_gen(board_name))

    def get_board_gen(self, board_name):
        for board in self.client.list_boards():
            if board.name == board_name:
                yield board

    def create_board(self, board_name):
        return self.client.add_board(board_name)

    def close_board(self, board):
        board.close()

    def get_open_lists(self, board):
        return board.open_lists()

    def create_list(self, board, list_name):
        return board.add_list(list_name)

    def get_list(self, board, list_name):
        return next(self.get_list_gen(board, list_name))

    def get_list_gen(self, board, list_name):
        for trello_list in self.get_open_lists(board):
            if trello_list.name == list_name:
                yield trello_list

    def close_list(self, board, list_name):
        self.get_list(board, list_name).close()

    def get_cards_on_board(self, board):
        return board.open_cards()

    def get_cards_on_list(self, board, list_name):
        return self.get_list(board, list_name).list_cards()

    def create_card(self, board, trello_list, card_name, source=None):
        if source:
            return board.get_list(trello_list.id).add_card(card_name, source=source)
        else:
            return board.get_list(trello_list.id).add_card(card_name)

    def get_card(self, card_name, board_name):
        return next(self.get_card_gen(card_name, board_name))

    def get_card_gen(self, card_name, board_name):
        for card in self.get_board(board_name).open_cards():
            if card.name == card_name:
                yield card

    def delete_card(self, card):
        self.client.get_card(card.id)
