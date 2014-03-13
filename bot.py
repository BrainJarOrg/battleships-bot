import json
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

    def __init__(self, ai='repeat'):
        self.play = getattr(self, 'ai')

    def repeat(self, state):
        move = {"move": "11"}
        print json.dumps(move)


if __name__ == "__main__":
    state = json.loads(sys.argv[1])
    if state['cmd']:
        place_ships()
    else:
        bot = Bot()
        bot.play(state)
