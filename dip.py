from abc import abstractmethod
from enum import Enum

# Принцип инверсии зависимостей
# Высокоуровневые классы не должны зависеть от низкоуровневых классов
# Они должны зависеть от абстракций


class Relationship(Enum):
    PARENT = 0
    CHILD = 1
    SIBLING = 2


class Person:
    def __init__(self, name):
        self.name = name


class RelationshipBrowser:
    @abstractmethod
    def find_all_children_of(self, name):
        pass


class Relationships(RelationshipBrowser):  # low-level

    relations = []  # клиент зависит от типа хранения

    def add_parent_and_child(self, parent: Person, child: Person):
        self.relations.append((parent, Relationship.PARENT, child))
        self.relations.append((child, Relationship.PARENT, parent))

    def find_all_children_of(self, name):
        for r in self.relations:
            if r[0].name == name and r[1] == Relationship.PARENT:
                yield r[2].name


class Research:  # high-level
    def __init__(self, browser: RelationshipBrowser):
        for p in browser.find_all_children_of("John"):
            print(f'John has a child called {p}')


parent = Person("John")
child1 = Person("Chris")
child2 = Person("Matt")

relationships = Relationships()

relationships.add_parent_and_child(parent, child1)
relationships.add_parent_and_child(parent, child2)

Research(relationships)
