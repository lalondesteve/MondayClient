import os
import requests
import logging

from dotenv import load_dotenv
import MondayClient.queries
from MondayClient.board import BoardCollection
from MondayClient.board import Board

# Setup environment variables
load_dotenv()
TOKEN = os.getenv("MONDAY_TOKEN")
API_URL = "https://api.monday.com/v2"


class Client:
    # Temporary for testing
    BOARD = os.getenv("MONDAY_BOARD")
    logging.getLogger(f"{__name__}.mondayclient")

    def __init__(self, token=TOKEN):
        self.token = token
        self.headers = {"Authorization": self.token}
        self.queries = MondayClient.queries
        self._boards = None
        self._board = None

    def execute_query(self, query, variables=None):
        data = {'query': query}
        if variables is not None:
            v = {'variables': variables}
            data.update(v)
        logging.debug(f'executing query : {data}')
        try:
            r = requests.post(url=API_URL, json=data, headers=self.headers)
            logging.debug(f'{r}')
        except Exception as e:
            # logging.exception(e)
            raise e
        else:
            logging.debug(f'Response: {r.json()}')
            return r.json()

    @property
    def boards(self):
        if not self._boards:
            r = self.execute_query(self.queries.get.boards())
            boards = r["data"].get("boards")
            self._boards = BoardCollection(boards, self)
        return self._boards

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        if isinstance(value, dict) and 'item_id' in value:
            # straight loading of board and item without useless queries
            board_id = value['board_id']
            item_id = value['item_id']
            self._board = Board(None, self, None, board_id=board_id, item_id=item_id)
            return
        if isinstance(value, dict):
            # in case user sends back the result of for i in self.boards
            value = value.get('board_id')
        elif isinstance(value, list) and len(value) == 1:
            # some queries give results in lists
            value = value[0]
        if not self._boards:
            # prevent useless loading of boards
            try:
                self._board = Board(None, self, None, board_id=value)
            except Exception:
                raise
            else:
                return
        raise ModuleNotFoundError
        # self._board = self.boards[value]


if __name__ == '__main__':
    mc = MondayClient.Client()
    mc.board = {'board_id': mc.BOARD, 'item_id': 714143499}