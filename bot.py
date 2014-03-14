import json
import random
import sys


class Placement(object):

    def __init__(self):
        self.state = [[0 for y in range(8)] for x in range(8)]
        random.seed()
        self.placement = {}

    def place_ships(self):
        for length in range(5, 1, -1):
            self.place_ship(length)
        print json.dumps(self.placement)

    def valid_placement(self, point, length, direction):
        try:
            if direction == 'horizontal':
                x = point[0]
                for y in range(point[1], point[1] + length):
                    if self.state[x][y] != 0:
                        return False
                return True
            elif direction == 'vertical':
                y = point[1]
                for x in range(point[0], point[0] + length):
                    if self.state[x][y] != 0:
                        return False
                return True
        except:
            pass
        return False

    def get_random_placement(self, length):
        direction = ['vertical', 'horizontal'][random.randint(0, 1)]
        point = [random.randint(0, 7), random.randint(0, 8 - length)]
        if direction == 'horizontal':
            point.reverse()
        return (direction, point)

    def place_ship(self, length):
        direction, point = self.get_random_placement(length)
        while not self.valid_placement(point, length, direction):
            direction, point = self.get_random_placement(length)
        if direction == 'horizontal':
            x = point[0]
            for y in range(point[1], point[1] + length):
                self.state[x][y] = 1
        else:
            y = point[1]
            for x in range(point[0], point[0] + length):
                self.state[x][y] = 1
        self.placement[str(length)] = {'point': "".join(map(str, reversed(point))),
                                       'orientation': direction}


MISS = -10
HIT = -5


class Bot(object):

    def __init__(self, ai='dumb_bot'):
        self.play = getattr(self, ai)
        random.seed()
        #self.log = open('play.log', 'a')

    def construct_state(self, state):
        self.state = [[0 for y in range(8)] for x in range(8)]
        self.free = []
        for x in range(8):
            for y in range(8):
                self.free.append((x, y))
        for move in state['hit']:
            move = tuple(map(int, move))
            y, x = move
            self.state[x][y] = HIT
            self.free.remove(move)
        for move in state['missed']:
            move = tuple(map(int, move))
            y, x = move
            self.state[x][y] = MISS
            self.free.remove(move)

    def mark_ships_naieve(self):
        for x in range(8):
            for y in range(8):
                if self.state[x][y] == HIT:
                    bounds = self.get_ship_bounds(x, y)
                    if bounds['x_min'] > 0:
                        self.state[bounds['x_min'] - 1][y] += 0.5
                    if bounds['x_max'] < 7:
                        self.state[bounds['x_max'] + 1][y] += 0.5
                    if bounds['y_min'] > 0:
                        self.state[x][bounds['y_min'] - 1] += 0.5
                    if bounds['y_max'] < 7:
                        self.state[x][bounds['y_max'] + 1] += 0.5

    def get_ship_bounds(self, x, y):
        # test X:
        x_min = x
        x_max = x
        x_bounded = True
        for x_off in reversed(range(0, x)):
            if self.state[x_off][y] == HIT:
                x_min = x_off
            elif self.state[x_off][y] < 0:
                break
            else:
                x_bounded = False
                break
        for x_off in range(x + 1, 8):
            if self.state[x_off][y] == HIT:
                x_max = x_off
            elif self.state[x_off][y] < 0:
                break
            else:
                x_bounded = False
                break
        res = {'x_min': x_min, 'x_max': x_max, 'x_bounded': x_bounded}
        y_min = y
        y_max = y
        y_bounded = True
        for y_off in reversed(range(0, y)):
            if self.state[x][y_off] == HIT:
                y_min = y_off
            elif self.state[x][y_off] < 0:
                break
            else:
                y_bounded = False
                break
        for y_off in range(y + 1, 8):
            if self.state[x][y_off] == HIT:
                y_max = y_off
            elif self.state[x][y_off] < 0:
                break
            else:
                y_bounded = False
                break
        res.update({'y_min': y_min, 'y_max': y_max, 'y_bounded': y_bounded})
        return res

    def random_move(self):
        move = self.free.pop(random.randint(0, len(self.free) - 1))
        return "".join(map(str, move))

    def max_value(self):
        maximum = 0
        for row in range(0, 8):
            if max(self.state[row]) > maximum:
                maximum = max(self.state[row])
        return maximum

    def max_move(self):
        max_row = 0
        maximum = 0
        for row in range(0, 8):
            if max(self.state[row]) > maximum:
                max_row = row
                maximum = max(self.state[row])
        max_col = self.state[max_row].index(max(self.state[max_row]))
        return "".join(map(str, (max_col, max_row)))

    def random_bot(self, state):
        self.construct_state(state)
        move = {'move': self.random_move()}
        print json.dumps(move)

    def dumb_bot(self, state):
        self.construct_state(state)
        self.mark_ships_naieve()
        #self.log.write(str(self.state) + '\n')
        #self.log.flush()
        move = {'move': self.random_move()}
        if self.max_value() > 0:
            move = {'move': self.max_move()}
        print json.dumps(move)

if __name__ == "__main__":
    state = json.loads(sys.argv[1])
    if state['cmd'] == 'init':
        place = Placement()
        place.place_ships()
    else:
        bot = Bot()
        bot.play(state)
