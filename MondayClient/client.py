import os
import requests

from dotenv import load_dotenv
import MondayClient.queries
from MondayClient.board import BoardCollection

# Setup environment variables
load_dotenv()
TOKEN = os.getenv("MONDAY_TOKEN")
API_URL = "https://api.monday.com/v2"


class Client:
    # Temporary for testing
    BOARD = os.getenv("MONDAY_BOARD")

    def __init__(self, token=TOKEN):
        self.token = token
        self.headers = {"Authorization": self.token}
        self.queries = MondayClient.queries
        self._boards = None
        self._board = None

    def execute_query(self, query, variables=None):
        data = {'query': query}
        if variables:
            v = {'variables': variables}
            data.update(v)
        try:
            r = requests.post(url=API_URL, json=data, headers=self.headers)
        except Exception as e:
            print(e)
            raise e
        else:
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
        if type(value) is dict:
            value = value.get('board_id')
        elif type(value) is list and len(value) == 1:
            value = value[0]
        self._board = self.boards[value]
