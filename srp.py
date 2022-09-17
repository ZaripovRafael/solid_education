# single responsabyliti principe
# принцип единственной ответственности
# Каждый класс берет на себя единственную ответственность


class Journal:
    """Хранение и удаление записей - основная обязанность журнала"""

    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.count += 1
        self.entries.append(f'{self.count}: {text}')

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return '\n'.join(self.entries)

    # # нарушаем принцип добавляя ему обязанности сохранять себя
    # def save_file(self, file_name):
    #     with open(file_name, 'w') as f:
    #         f.write(str(self))
    #
    # # и загружать что-то
    # def load(self, file_name):
    #     pass


class PersistenceManager:
    """Функцию сохранения лучше возложить на отдельный класс"""
    @staticmethod
    def save_to_file(journal: Journal, file_name: str):
        with open(file_name, 'w') as f:
            f.write(str(journal))


j = Journal()

j.add_entry("Сегодня я опоздал на автобус")
j.add_entry("Нашел самый вкусный кофе в городе")


file = "./journal.txt"

PersistenceManager.save_to_file(j, file)

print(f'Journal entries:\n{j}')
