from typing import List

"""
Для того чтобы не нарушать принцип "открытости для расширения закрытости для модификации"

Классы должны быть открыты для расширения, но закрыты для модификации.

Есть к примеру продукты. У них есть тип, размер, цвет.

К примеру приходит менеджер и говорит что нужно их сортировать по размеру

Плохая идея делать это через добавления метода к классу продукта
Хорошая - сделать это через класс фильтрации по размеру (расширение)

Существую корпоративные шаблоны проектирования. Один из таких шаблонов Спецификация
"""
# Плохой пример


class Product:

    def __init__(self, name: str, color: str, size: str):
        self.name = name
        self.color = color
        self.size = size


# Изначально по требованиям должна быть фильтрация по цвету
class ProductFilter:

    def filter_by_color(self, products: List[Product], color: str):
        for product in products:
            if product.color == color:
                yield product

    # а потом менеджер попросил добавить фильтр по размеру
    def filter_by_size(self, products: List[Product], size: str):
        for product in products:
            if product.size == size:
                yield product

    # Этой модификацией мы нарушили принцип открытости закрытости.
    # Кроме этого такой подход не масштабируется и приводит к взрывному росту сложности.
    # Если потребуется фильтр по цвету, размеру, цвету и размеру, то комбинаций будет 2!,
    # Если добавится третий параметр, то 3!

# Specification


class Specification:
    """
    Определяет ли один элемент конкретному критерию
    У него только один метод без конкретной реализации
    """
    def is_satisfied(self, item):
        ...

    def __and__(self, other):
        """Для перегрузки оператора &"""
        return AndSpecification(self, other)


class Filter:
    """
    Так же базовый класс
    Идея в том чтобы расширять базовые классы, а не модифицировать
    """
    def filter(self, items: List[Product], spec: Specification):
        ...


class ColorSpecification(Specification):

    def __init__(self, color: str):
        self.color = color

    def is_satisfied(self, item: Product):
        return item.color == self.color


class SizeSpecification(Specification):

    def __init__(self, size: str):
        self.size = size

    def is_satisfied(self, item: Product):
        return item.size == self.size


class AndSpecification(Specification):
    """Класс для комбинаций фильтров"""

    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        """Обойдя все элементы применяет к ней функцию проверки элемента спецификации"""
        return all(map(lambda spec: spec.is_satisfied(item), self.args))


class BetterFilter(Filter):

    def filter(self, items, spec: Specification):
        for item in items:
            if spec.is_satisfied(item):
                yield item


if __name__ == '__main__':
    apple = Product('Apple', 'green', 'small')
    tree = Product('Tree', 'green', 'large')
    house = Product('House', 'yellow', 'large')

    products = [apple, tree, house]

    pf = ProductFilter()
    print('Green products(old):')

    for product in pf.filter_by_color(products, "green"):
        print(f' - {product.name} is {product.color}')

    bf = BetterFilter()

    print('\nGreen products (new):')
    green = ColorSpecification('green')

    for product in bf.filter(products, green):
        print(f' - {product.name} is {product.color}')

    print('\nLarge products:')
    large = SizeSpecification('large')

    for product in bf.filter(products, large):
        print(f' - {product.name} is {product.size}')

    print('\nLarge yellow items:')

    # large_yellow = AndSpecification(large, ColorSpecification('yellow'))
    large_yellow = large & ColorSpecification('yellow')  # Вариант с перегрузкой оператора & (изменили подход)

    for product in bf.filter(products, large_yellow):
        print(f' - {product.name} is {product.size} and {product.color}')

# Таким образом соблюдение принципа открытости закрытости позволяет не изменять код, который протестирован
# и запущен в продакшн
