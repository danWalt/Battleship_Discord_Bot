import pprint
import random

UP = -1
DOWN = 1
NOMOVE = 0


class BGE:
    destroyer = [''] * 2
    cruiser = [''] * 3
    battleship = [''] * 4
    SHIPS = [destroyer, cruiser, battleship]
    CLEAR = ' '
    DIRECTIONS = [UP, DOWN, NOMOVE]

    def __init__(self, rows=None, cols=None):
        self.rows = rows
        self.cols = cols
        self.board = [[BGE.CLEAR for row in range(self.rows)] for col in
                      range(self.cols)]
        self.game_ships = []
        for ship in BGE.SHIPS:
            self.game_ships.append(self.place_ship(ship))
        self.ship_total_size = 0
        for ship in self.game_ships:
            self.ship_total_size += len(ship)
        self.turns = 0
        self.hit_number = 0
        self.miss_number = 0
        self.shots = []
        self.game_over = False
        while self.game_over == False:
            pprint.pprint(self.board)
            print('Please pick a coordinate you want to shoot')
            print('Pick row: ')
            r = int(input())
            print('Pick col: ')
            c = int(input())
            self.shoot(r, c)

    def find_start_point(self):
        start_point = (random.randint(0, self.rows - 1),
                       random.randint(0,
                                      self.cols - 1))
        start = self.board[start_point[0]][start_point[1]]
        while start != BGE.CLEAR:
            start_point = [random.randint(0, self.rows), random.randint(0,
                                                                        self.cols)]
            start = self.board[start_point[0]][start_point[1]]
        return start_point

    def get_move_direction(self):

        move_direction = [random.choice(BGE.DIRECTIONS), random.choice(
            BGE.DIRECTIONS)]
        while move_direction == [NOMOVE, NOMOVE] or move_direction == [UP,
                                                                       UP] \
                or move_direction == [DOWN, DOWN] or move_direction == [
            DOWN, UP] or move_direction == [UP, DOWN]:
            move_direction = [random.choice(BGE.DIRECTIONS), random.choice(
                BGE.DIRECTIONS)]

        return move_direction

    def set_ship(self, start_point, move_direction, ship_size):
        placements = ship_size - 1
        location = [start_point]
        current = start_point
        for placement in range(placements):
            new = (current[0] + move_direction[0], current[
                1] + move_direction[1])
            location.append(new)
            current = new
        return tuple(location)

    def place_ship(self, ship):
        ship_size = len(ship)

        start_point = self.find_start_point()

        move_direction = self.get_move_direction()
        ship_coordinates = self.set_ship(start_point, move_direction,
                                         ship_size)
        if not self.out_of_range(ship_coordinates):
            return self.place_ship(ship)
        elif not self.is_placement_free(ship_coordinates):
            return self.place_ship(ship)
        return ship_coordinates

    def game_stats(self):
        print('Number of turns: ', self.turns)
        print('Number of hits: ', self.hit_number)
        print('Number of misses: ', self.miss_number)

    def show_board(self):
        pprint.pprint(self.board)

    def shoot(self, row, column):
        if row > self.rows or row < 0 or column > self.cols or column < 0:
            return 'Invalid coordinates please try again'
        elif (row, column) in self.shots:
            return 'tile already shot, please try again'
        else:
            coord = (row, column)
            self.shots.append((row, column))
            self.turns += 1
            h = self.hit_number
            for ship in self.game_ships:
                hit = self.check_hit(coord, ship)
                if hit == 'X':
                    self.hit_number += 1
                    self.board[row][column] = hit
                    break
                else:
                    self.miss_number += 1
                    self.board[row][column] = hit
            if h < self.hit_number:
                print('Hit!')
            else:
                print('Miss!')
            self.check_victory()

    def is_placement_free(self, location):
        if len(self.game_ships) == 0:
            return True
        else:
            for ship in self.game_ships:
                for coordinates in ship:
                    for new_coordinates in location:
                        if coordinates == new_coordinates:
                            return False
        return True

    def out_of_range(self, ship_coordinates):
        for point in ship_coordinates:
            if point[0] > 7 or point[0] < 0 or point[1] > 7 or point[1] < 0:
                return False
        return True

    def check_hit(self, coord, ship):
        r = coord[0]
        c = coord[1]
        hit = 'O'
        for placement in ship:
            if coord == placement:
                hit = 'X'
                break
        return hit

    def check_victory(self):
        if self.hit_number == self.ship_total_size:
            self.game_over = True
            print('All ships down, you have won!')
        else:
            print('Ships are still floating! Keep playing')


def start_game(rows=8, col=8):
    return BGE(rows, col)


b = start_game()
b.show_board()
