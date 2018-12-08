from urllib.parse import urljoin

import requests


class NetworkManager:
    def __init__(self, broadcast_url: str):
        self.broadcast_url = broadcast_url

    def new_block(self, block_json: str):
        return requests.post(
            urljoin(self.broadcast_url, "/peer/block"), json=block_json)

    def fetch_blocks(self):
        return requests.get(urljoin(self.broadcast_url, "/peer/block")).json()
