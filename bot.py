import json
import random
import sys


def place_ships():
    placement = {
        '2': {
            'point': '21',
            'orientation': 'vertical'
        },
        '3': {
            'point': '14',
            'orientation': 'vertical'
        },
        '4': {
            'point': '35',
            'orientation': 'horizontal'
        },
        '5': {
            'point': '30',
            'orientation': 'horizontal'
        }
    }
    print json.dumps(placement)


class Bot(object):

    def __init__(self, ai='repeat_bot'):
        self.play = getattr(self, ai)
        random.seed()

    def construct_state(self, state):
        self.state = [[0, 0, 0, 0, 0, 0, 0, 0] for x in range(8)]
        self.free = []
        for x in range(8):
            for y in range(8):
                self.free.append((x, y))
        for move in state['hit']:
            move = tuple(map(int, move))
            x, y = move
            self.state[x][y] = 1
            self.free.remove(move)
        for move in state['missed']:
            move = tuple(map(int, move))
            x, y = move
            self.state[x][y] = -1
            self.free.remove(move)

    def random_move(self):
        move = self.free.pop(random.randint(0, len(self.free) - 1))
        return "".join(map(str, move))

    def repeat_bot(self, state):
        self.construct_state(state)
        move = {'move': self.random_move()}
        print json.dumps(move)


if __name__ == "__main__":
    state = json.loads(sys.argv[1])
    if state['cmd'] == 'init':
        place_ships()
    else:
        bot = Bot()
        bot.play(state)
