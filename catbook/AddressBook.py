from collections import UserDict
from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime, date, timedelta
import re
import pickle
from catbook.classes import *
from pkg_resources import resource_filename

# Клас AddressBook, який наслідується від UserDict, 
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        self.save_to_file()  # зберегти після додавання
        return f"Contact {record} added successfully"


    def delete_record(self, name: str):
        if name in self.data:
            del self.data[name]
            self.save_to_file()  # зберегти після видалення
            return f"Contact with name '{name}' deleted successfully"
        return f"No contact with name '{name}' in the address book"


    def save_to_file(self):
        with open(resource_filename("catbook","adress.bin"), "wb") as file:
            pickle.dump(self.data, file)


    def load_from_file(self):
        try:
            with open(resource_filename("catbook","adress.bin"), "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            # якщо файл відсутній, створити
            self.data = {}


    def congratulate(self, period: int):
        current_date = datetime.now().date()

        results = []
        for record in self.data.values():
            if record.birthday:
                birthdate = record.birthday.value #.date()
                next_birthday = datetime(current_date.year, birthdate.month, birthdate.day).date()

                if next_birthday < current_date:
                    next_birthday = datetime(current_date.year + 1, birthdate.month, birthdate.day).date()

                days_to_bd = (next_birthday - current_date).days
                if 0 <= days_to_bd <= period:
                    results.append(f"{record.name} {next_birthday.strftime('%d.%m')}")

        return results


    # метод iterator, який повертає генератор за записами. Пагінація    
    def __iter__(self, n=5):
        keys = list(self.data.keys())
        for i in range(0, len(keys), n):
            chunk = {key: self.data[key] for key in keys[i:i + n]}
            yield chunk
    

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())

# завантажує записи під час ініціалізації
    def __init__(self):
        super().__init__()
        self.load_from_file()



address_book = AddressBook()    

