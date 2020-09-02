from MondayClient.board import Board
from MondayClient.base import MondayCollection


class BoardCollection(MondayCollection):
    def __init__(self, boards, client):
        super().__init__(client)
        self.collection = {board['board_id']: Board(board, client, self)
                           for board in boards}

    def update_board(self, board_id, board):
        self.collection[board_id] = Board(board, self.client, self)
