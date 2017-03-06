#!python
import trello_class


def get_names_of(things):
    return list(x.name for x in things)


def create_new_boards_from_lists_on_source_board(trello_obj, board):
    trello_lists = board.open_lists()
    new_boards = []
    for trello_list in trello_lists:
        new_boards.append(trello_obj.create_board(trello_list.name))
    return new_boards


def create_cards_with_url_to_new_boards(trello_obj, source_board, new_boards):
    for board in new_boards:
        trello_list = trello_obj.get_list(source_board, board.name)
        card = trello_obj.create_card(board, trello_list, board.name)
        card.attach(name=board.name, url=next(get_board_url(new_boards, trello_list.name)))


def get_board_url(new_boards, name):
    for board in new_boards:
        if board.name == name:
            yield board.url


def clone_cards_to_new_boards(trello_obj, source_board, new_boards):
    new_list = []
    for board, trello_list in get_list_and_board(trello_obj, source_board, new_boards):
        backlog = trello_obj.create_list(board, "Backlog")
        cards = trello_obj.get_cards_on_list(source_board, trello_list.name)
        new_list.extend(list(clone_cards_to_backlog(trello_obj, board, backlog, card) for card in cards))
    return new_list


def get_list_and_board(trello_obj, source_board, new_boards):
    for trello_list in trello_obj.get_open_lists(source_board):
        for board in new_boards:
            if board.name == trello_list.name:
                yield board, trello_list


def clone_cards_to_backlog(trello_obj, board, trello_list, card):
    return trello_obj.create_card(board, trello_list, card.name, source=card.id)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--master-board", required=True)
    parser.add_argument("--api-key", required=True)
    parser.add_argument("--token", required=True)
    args = parser.parse.args()
    trello_obj = trello_class.TrelloClass(args.api_key, args.token)
    new_boards = create_new_boards_from_lists_on_source_board(trello_obj, args.master_board)
    create_cards_with_url_to_new_boards(trello_obj, args.masterboard, new_boards)
    clone_cards_to_new_boards(trello_obj, args.masterboard, new_boards)
