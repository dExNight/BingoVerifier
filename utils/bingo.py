import json
import os
from typing import Tuple
from pytoniq_core import Cell, Builder, Address, begin_cell


class BingoContract:

    def __init__(self, game_id: int, admin_address: str):
        self.game_id: int = game_id
        self.admin_address: Address = Address(admin_address)

    def construct_data(self) -> Cell:
        return begin_cell().store_uint(0, 1).store_uint(self.game_id, 64).store_address(self.admin_address).store_uint(0, 256).end_cell()

    def construct_code(self) -> Cell:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(
            current_dir, '../build/BingoRaffle.compiled.json')
        with open(json_path, 'r') as file:
            data = json.load(file)
            return Cell.one_from_boc(data["hex"])

    def calculate_state_init(self) -> Cell:
        data: Cell = self.construct_data()
        code: Cell = self.construct_code()
        return Builder().store_uint(0, 2).store_dict(code).store_dict(data).store_uint(0, 1).end_cell()

    def get_address(self) -> Address:
        state_init: Cell = self.calculate_state_init()

        address_hash: bytes = state_init.hash
        return Address((0, address_hash))

    def get_raffle_msg(self, query_id: int = 0) -> Tuple[Cell, float]:
        return begin_cell().store_uint(1, 32).store_uint(query_id, 64).end_cell(), 0.005
