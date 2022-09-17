# принцип подстановки Liskov
# Если у Вас есть API, который принимает какой-то базовый класс,
# Вы должны иметь возмоность передать туда любой базовый класс
# и все должно работать


class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def area(self):
        return self._width * self._height

    def __str__(self):
        return f'Width: {self.width}, height: {self.height}'

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value


def use_it(rc: Rectangle):
    w = rc.width
    rc.height = 10
    expected = int(w * 10)
    print(f'Expected an area of {expected}, got {rc.area}')


rc = Rectangle(2, 3)

use_it(rc)

# Нарушаем принцип


class Square(Rectangle):
    def __init__(self, size):
        super().__init__(size, size)

    @Rectangle.width.setter
    def width(self, value):
        self._width = self._height = value

    @Rectangle.height.setter
    def height(self, value):
        self._width = self._height = value


sq = Square(5)

use_it(sq)

#  основная проблема в rc.height = 10 и в использовании сеттеров так как она изменяет и ширину в квадрате
