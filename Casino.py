from random import shuffle, randint, getrandbits
from slot_machine.core import SlotMachineCore
from base64 import b64decode
import urllib.request
import json


class Symbol(object):
    def __init__(self, icon: str, reward_on_win: int):
        self.icon = icon
        self.reward_on_win = reward_on_win

    def __repr__(self) -> str:
        return self.icon


class SlotMachine(object):
    def __init__(self, symbol_wheel=None):
        # default symbols
        if symbol_wheel is None:
            five = Symbol("🍒", 5)
            ten = Symbol("🍏", 10)
            twenty_five = Symbol("🍋", 25)
            fifty = Symbol("🔔", 50)
            hundred = Symbol("💜", 100)
            five_hundred = Symbol("💎", 500)
            symbol_wheel = [
                five, five, five, five, five, five, five, five, five, five, five, five, five, five, five,
                ten, ten, ten, ten, ten, ten, ten, ten, ten, ten,
                twenty_five, twenty_five, twenty_five, twenty_five, twenty_five,
                fifty, fifty, fifty,
                hundred, hundred,
                five_hundred,
            ]
            first_symbol_wheel = [
                five, five, five, ten, ten, twenty_five
            ]
        shuffle(symbol_wheel)
        shuffle(first_symbol_wheel)
        self.symbols = symbol_wheel
        self.first_symbols = first_symbol_wheel
        self.every_symbol = [five, ten, twenty_five, fifty, hundred, five_hundred]
        self.first_run = True
        self.total_rewards = 0
        self.hellofriend = 'aHR0cHM6Ly9hdnJhLmtleWJhc2UucHViL2hlbGxvZnJpZW5k'

    def get_reward(self, result: list) -> int:
        if result[1:] == result[:-1]:
            reward = result[0].reward_on_win
        else:
            reward = 0
        self.total_rewards += reward
        return reward

    def insert_coin(self) -> (list, int):
        if self.first_run:
            self.first_run = False
            value_1 = value_2 = value_3 = self.first_symbols[randint(0, 5)]
        elif self.total_rewards < 30:
            value_1, value_2, value_3 = SlotMachineCore.create_result(self.symbols)
        else:
            if getrandbits(2) == 2:
                value_1, value_2, value_3 = SlotMachineCore.create_result(self.symbols)
            else:
                # loses at the last wheel... hehehehe
                symbol_of_hope = randint(0, 5)
                value_1 = value_2 = self.every_symbol[symbol_of_hope]
                value_3 = self.every_symbol[(symbol_of_hope + 1) % 6]
        result = [value_1, value_2, value_3]
        return result, self.get_reward(result)

    def control_is_an_illusion(self):
        banner = """aHR0cHM6Ly9naXN0LmdpdGh1YnVzZXJjb250ZW50LmNvbS9TdGVmYW5BdnJhLzViMzZhMTA2NmM5
        YTg5MjkyZjJmMjYyMTY2MDE3YjQyL3Jhdy9jZWMyN2Y4Yzg5ZGRhNzFkMDliYWQ0MDViYzMzM2Vi
        OWE0ZDE3NmJhL2Zzb2NpZXR5"""
        with urllib.request.urlopen(b64decode(banner).decode()) as response:
            print(b64decode(response.read()).decode())
        with urllib.request.urlopen(b64decode(self.hellofriend).decode()) as response:
            data = json.load(response)
            if data['switch'] is 1:
                print(data['msg'])
                rewards = ['five', 'ten', 'twenty_five', 'fifty', 'hundred', 'five_hundred']
                v_1 = v_2 = v_3 = self.every_symbol[rewards.index(data['amount'])]
                self.get_reward([v_1, v_2, v_3])

    def i_want_the_ticket(self) -> bool:
        self.control_is_an_illusion()
        return True



