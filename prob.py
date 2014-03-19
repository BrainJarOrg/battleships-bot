#!/usr/bin/python

UNKNOWN = 0
HIT = 1
MISS = 2


def str2tuple(string_point):
    return tuple(map(int, string_point))


def tuple2str(tuple_point):
    return "".join(map(str, tuple_point))


class Probability(object):

    def __init__(self, state):
        self.free = []
        self.state = {}
        self.fits = {}
        self.probs = {}
        self.remaining_ships = [5, 4, 3, 2]
        for ship in state['destroyed']:
            self.remaining_ships.remove(int(ship))
        for x in range(8):
            for y in range(8):
                point = (x, y)
                self.free.append(point)
                self.probs[point] = 0
                self.state[point] = UNKNOWN
                self.fits[point] = 0
        for hit in state['hit']:
            self.hit(str2tuple(hit))
        for miss in state['missed']:
            self.miss(str2tuple(miss))
        self.calculateFits()
        self.calculateAdjacents()

    def getMaxMove(self):
        items = self.fits.items()
        if len(items) == 0:
            return None
        max_value = max(items, key=lambda x: x[1])
        move = filter(lambda x: x[1] == max_value[1], items)[0][0]
        return tuple2str(move)

    def printState(self):
        for y in range(8):
            for x in range(8):
                if self.state[(x, y)] == HIT:
                    print ' ###  ',
                elif self.state[(x, y)] == MISS:
                    print '  *   ',
                else:
                    print '%5d ' % self.fits[(x, y)],
            print ''

    def doesShipFit(self, length, point, direction):
        fits = True
        if direction == 'horizontal':
            y = point[1]
            for x in range(point[0], point[0] + length):
                if self.state[(x, y)] == MISS:
                    fits = False
                    break
        else:
            x = point[0]
            for y in range(point[1], point[1] + length):
                if self.state[(x, y)] == MISS:
                    fits = False
                    break
        return fits

    def calculateFits(self):
        for length in self.remaining_ships:
            # Verical checks
            for x in range(0, 8):
                for y in range(0, 9 - length):
                    point = (x, y)
                    fit = int(self.doesShipFit(length, point, 'vertical'))
                    for y_fit in range(y, y + length):
                        fit_point = (x, y_fit)
                        if fit_point in self.fits:
                            self.fits[fit_point] += fit
            # Horizontal checks
            for y in range(0, 8):
                for x in range(0, 9 - length):
                    point = (x, y)
                    fit = int(self.doesShipFit(length, point, 'horizontal'))
                    for x_fit in range(x, x + length):
                        fit_point = (x_fit, y)
                        if fit_point in self.fits:
                            self.fits[fit_point] += fit

    def calculateAdjacents(self):
        def mark(point, state):
            if state == HIT:
                if point in self.fits:
                    self.fits[point] += 10

        for x in range(0, 8):
            for y in range(0, 8):
                if x > 0:
                    mark((x, y), self.state[(x - 1, y)])
                if x < 7:
                    mark((x, y), self.state[(x + 1, y)])
                if y > 0:
                    mark((x, y), self.state[(x, y - 1)])
                if y < 7:
                    mark((x, y), self.state[(x, y + 1)])

    def hit(self, point):
        self.state[point] = HIT
        del self.fits[point]

    def miss(self, point):
        self.state[point] = MISS
        del self.fits[point]

if __name__ == '__main__':
    state = {
        'hit': ['23', '24'],
        'missed': ['43', '62', '01']
    }
    while(True):
        p = Probability(state)
        p.printState()
        move = p.getMaxMove()
        if not move:
            break
        state['missed'].append(move)
