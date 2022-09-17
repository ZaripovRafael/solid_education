# Принцип разделения интерфейсов

# суть в том что не нужно добавлять слишком много методов в интерфейс


class Mashine:

    def print(self, document):
        raise NotImplementedError

    def fax(self, document):
        raise NotImplementedError

    def scan(self, document):
        raise NotImplementedError


class MultiFuncPrinter(Mashine):
    """Такое количество методов нормально для МФУ"""
    def print(self, document):
        # ok
        pass

    def fax(self, document):
        # ok
        pass

    def scan(self, document):
        # ok
        pass


class OldPrinter(Mashine):
    """Для старых принтеров все эти методы не нужны"""
    def print(self, document):
        # ok
        pass

    def fax(self, document):
        pass

    def scan(self, document):
        pass

# Выход - разбить все на отдельные интерфейсы


class Printer:

    @abstractmethod
    def print(self, document):
        pass


class Scanner:

    @abstractmethod
    def scan(self, document):
        pass


class Fax:

    @abstractmethod
    def fax(self, document):
        pass


class MyPrinter(Printer):
    def print(self, document):
        print(document)


class Photocopier(Printer, Scanner):
    def print(self, document):
        pass

    def scan(self, document):
        pass


class MultiscanerDevice(Printer, Scanner):

    def __init__(self, printer: Printer, scanner: Scanner):
        self.scanner = scanner
        self.printer = printer

    @abstractmethod
    def print(self, document):
        self.printer.print(document)

    @abstractmethod
    def scan(self, document):
        self.scanner.scan(document)
