from datetime import datetime, date
import re
from catbook.exeptions import *
from collections import UserDict, UserList
from catbook.note_tag import Name_teg, Note, Teg, Notes


class Field:
    def __init__(self, value: str) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return self.value


class Name(Field):
    def __init__(self, first_name, last_name=None) -> None:
        if last_name:
            self.value = f"{first_name} {last_name}"
        else:
            self.value = first_name
    

class Phone(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value:str):
        if self.is_correct_phone(value):
            self.__value = value
        else:
            raise PhoneError(value)
        
    def is_correct_phone(self, value) -> bool:
        pattern = re.compile(r"\+\d{11,13}")
        result = re.fullmatch(pattern, value)
        
        return True if result else False


class Birthday(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value:str):
        if re.fullmatch(r"\d{1,2}-\d{1,2}-\d{4}", value):
            self.__value = datetime.strptime(value, "%d-%m-%Y")
        elif re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", value):
            self.__value = datetime.strptime(value, "%d.%m.%Y")
        elif re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}", value):
            self.__value = datetime.strptime(value, "%d/%m/%Y")
        else:
            raise BirthdayError(value)
        
    def is_empty_date(self) -> bool:
        return self.__value == datetime(1, 1, 1)
    
    def __str__(self):
        return self.__value.strftime("%d-%m-%Y") if not self.is_empty_date() else ""


class Email(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value:str):
        if self.is_correct_email(value):
            self.__value = value.lower()
        else:
            raise EmailError(value)
        
    def is_correct_email(self, value) -> bool:
        pattern = re.compile(r"([a-zA-Z]{1}[a-zA-Z0-9_.]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,})")
        result = re.fullmatch(pattern, value)
        
        return True if result else False
    

class Adress(Field):
    def __init__(self, value):
         self.value = value


class Field:
    def __init__(self, value):
         self.value = value
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return str(self)

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None, adress: Adress = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday
        self.email = email
        self.adress = adress


    def change_birthday(self, new_birthday: Birthday):
        self.birthday = new_birthday
        # address_book.save_to_file()
        return f"Birthday changed to {new_birthday} for contact {self.name}"

    def change_email(self, new_email:Email):
        self.email = new_email
        # address_book.save_to_file()
        return f"Email changed to {new_email} for contact {self.name}"
    
    def change_adress(self, new_adress:Adress):
        self.adress = new_adress
        # address_book.save_to_file()
        return f"Address changed to {new_adress} for contact {self.name}"
    
    def add_phone(self, phone: Phone):
        if str(phone) not in [str(p) for p in self.phones]:
            self.phones.append(phone)
            # address_book.save_to_file()
            return f"Succesfully added phone '{phone}' to name '{self.name}'"
        else:
            return f"Phone '{phone}' is already in record '{self}'"

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        phones_list = [str(p) for p in self.phones]

        if str(old_phone) not in phones_list:
            return f"There is no phone '{old_phone}' in record '{self}'"
        if str(new_phone) in phones_list:
            return f"Phone '{new_phone}' is already in record '{self}'"
        
        index = phones_list.index(old_phone.value)
        self.phones[index] = new_phone
        # address_book.save_to_file()
        return f"Succesfully changed phone '{old_phone}' to '{new_phone}'"


    def change_name(self, new_name: Name):
        old_name = self.name
        self.name = new_name
        # address_book.save_to_file()
        return f"Name changed to {new_name} for old contact {old_name}"

        
    def __str__(self) -> str:
        result = ""
        if self.name:
            result = result + str(self.name)
        if len(self.phones):
            result = result + ", " + ",".join([str(p) for p in self.phones])
        if self.birthday:
            result = result + ", " + str(self.birthday)
        if self.email:
            result = result + ", " + str(self.email)
        if self.adress:
            result = result + ", " + str(self.adress)

        return result
