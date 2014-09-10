"""Solution for First Test Task of HeadHunter's School

Python3.4

author: Артем Безукладичный
mail: overmes@gmail.com
"""
import argparse


parser = argparse.ArgumentParser(description='Division in different number systems')
parser.add_argument('file', metavar='F', type=open, help='file')
args = parser.parse_args()

class Square:
    """Square representation
    """
    def __init__(self, xa, ya, xb, yb):
        """
        :param xa: left bottom x
        :param ya: left bottom y
        :param xb: right top x
        :param yb: right top y
        """
        if xa > xb:
            raise ValueError("xa > xb")
        if ya > yb:
            raise ValueError("ya > yb")
        self.xa = xa
        self.ya = ya
        self.xb = xb
        self.yb = yb

    def check_other(self, other):
        if not isinstance(other, Square):
            raise ValueError('Wrong input')

    def split_without_intersect(self, other):
        """Return squares from other which not intersect with self
        it not intersection return None
        """
        self.check_other(other)
        if self.has_intersect(other):
            left_part = self._get_left_part(other)
            right_part = self._get_right_part(other)
            top_part = self._get_top_part(other)
            bottom_part = self._get_bottom_part(other)

            result = [part for part in (left_part, right_part, top_part, bottom_part) if part]
        else:
            result = None
        return result

    def _get_left_part(self, other):
        if self.xa < other.xa:
            left_part = Square(self.xa, self.ya, other.xa, self.yb)
            if not left_part.empty():
                return left_part
        else:
            return None

    def _get_right_part(self, other):
        if self.xb > other.xb:
            right_part = Square(other.xb, self.ya, self.xb, self.yb)
            if not right_part.empty():
                return right_part
        else:
            return None

    def _get_bottom_part(self, other):
        if self.ya < other.ya:
            return Square(max(self.xa, other.xa), self.ya, min(self.xb, other.xb), other.ya)
        else:
            return None

    def _get_top_part(self, other):
        if self.yb > other.yb:
            return Square(max(self.xa, other.xa), other.yb, min(self.xb, other.xb), self.yb)
        else:
            return None

    def has_intersect(self, other):
        self.check_other(other)
        return self.xb > other.xa and other.xb > self.xa and self.ya < other.yb and self.yb > other.ya

    def empty(self):
        return self.xa == self.xb or self.ya == self.yb

    def __str__(self):
        return '({}, {}) ({}, {})'.format(self.xa, self.ya, self.xb, self.yb)

    def get_square(self):
        return (self.xb - self.xa)*(self.yb - self.ya)


class NotIntersectSquares:
    """Represent massive of Squares which not intersect
    """
    def __init__(self):
        self.squares = []

    def split_with_first_squares_with_intersect(self, insert_square):
        """If inserted square intersect with self.squares return not intersection parts
        else return None
        """
        for square in self.squares:
            split_result = insert_square.split_without_intersect(square)
            if split_result is not None:
                return split_result

    def insert_squares(self, squares):
        """Insert squares list, remove intersect part if need
        """
        squares_for_insert = squares.copy()
        while squares_for_insert:
            current_square = squares_for_insert.pop()
            split_result = self.split_with_first_squares_with_intersect(current_square)
            if split_result is None:
                self.squares.append(current_square)
            else:
                squares_for_insert.extend(split_result)

    def get_square_sum(self):
        square_sum = 0
        for s in self.squares:
            square_sum += s.get_square()
        return square_sum


squares_from_file = []
for row in args.file:
    squares_from_file.append(Square(*[int(n) for n in row.split()]))

not_inserted_squares = NotIntersectSquares()
not_inserted_squares.insert_squares(squares_from_file)
print(not_inserted_squares.get_square_sum())