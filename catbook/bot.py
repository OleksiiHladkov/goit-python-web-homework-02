from catbook.AddressBook import *
from catbook.classes import *
from catbook.exeptions import *
import difflib
from rich.table import Table
from rich import box
import subprocess
import re, os, pickle
from pkg_resources import resource_filename


class Bot:
    def __init__(self):
        self.value = AddressBook()


def get_closest_matches(user_input, commands, n=3, cutoff=0.6):
    user_input_lower = user_input.lower()
    closest_matches = []
    for cmd, kwds in commands.items():
        for kwd in kwds:
            if kwd in user_input_lower:
                closest_matches.append(kwd)
    if not closest_matches:
        user_words = user_input_lower.split()
        for cmd, kwds in commands.items():
            for kwd in kwds:
                for word in user_words:
                    similarity = difflib.SequenceMatcher(None, word, kwd).ratio()
                    if similarity >= 0.5:  # Поріг схожості, можна налаштувати під свої потреби
                        closest_matches.append(kwd)
                        break
    return closest_matches


def closest_matches_suggestion(matches):
    return f"Did you mean one of the following commands: {', '.join(matches)}?"


def unknown_command(text):
    return f"Unknown command: '{text}'. Type 'help' to see the list of available commands."


@input_error
def add_command(*args):
    if not len(args):
        raise ValueNeedEnterError("Name")

    name = None
    phone = ""
    birthday = ""
    email = ""
    adress = ""

    count = 1
    for value in args:
        if count == 1:
            name = Name(value)
        else:
            lower_value = value.lower()

            if "-" in lower_value:
                birthday = Birthday(value)

            elif "@" in value:
                if re.match(r"([a-zA-Z]{1}[a-zA-Z0-9_.]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,})", value):
                    email = Email(value)
                else:
                    raise EmailError(value)
                
            elif value.startswith("+"):
                if re.match(r"\+\d{11,13}", value):
                    phone = Phone(value)
                else:
                    raise PhoneError(value)
                
            elif count == len(args) and not any(symbol in value for symbol in ['-', '/', '@', '+']):
                adress = Adress(value)
            else:
                raise UnknownFieldError(value)

        count += 1

    record = address_book.get(name.value)

    if record:
        if phone:
            record.add_phone(phone)
        if birthday:
            record.change_birthday(birthday)
        if email:
            record.change_email(email)
        if adress:
            record.change_adress(adress)
        return f"Contact {name.value} updated successfully."

    record = Record(name, phone, birthday, email, adress)
    address_book.save_to_file()
    return address_book.add_record(record)
    
    
@input_error
def change_command(*args):
    if not len(args):
        raise ValueNeedEnterError("Name")
    
    if len(args) < 3:
        raise ValueNeedEnterError("Old Phone and New Phone")
    
    name = None
    old_phone = None
    new_phone = None
    birthday = None
    email = None
    adress = None
    
    count = 1
    for value in args:
        if count == 1:
            name = Name(value)
        if count == 2:
            old_phone = Phone(value)
        if count == 3:
            new_phone = Phone(value)
        if count == 4:
            birthday = Birthday(value)
        if count == 5:
            email = Email(value)
        if count == 6:
            adress = Adress(value)
                
        count += 1

    record = address_book.get(name.value)

    if record:
        result = list()
        result.append(record.change_phone(old_phone, new_phone))
        
        if birthday:
            result.append(record.change_birthday(birthday))
        if email:
            result.append(record.change_email(email))
        if adress:
            result.append(record.change_adress(adress))
        return "\n".join(result)
    else:
        raise FindRecordError(name.value)


@input_error
def edit_name_command(*args):
    if len(args) < 2:
        raise ValueNeedEnterError("Old Name and New Name")
    
    old_name = Name(args[0])
    new_name = Name(args[1])
    
    record = address_book.get(old_name.value)

    if record:
        return record.change_name(new_name)
    else:
        raise FindRecordError(new_name)


@input_error
def delete_contact_command(*args):
    if not len(args):
        raise ValueNeedEnterError("Name")
    
    name = Name(args[0])
    
    record = address_book.get(name.value)

    if record:
        return address_book.delete_record(name.value)
    else:
        raise FindRecordError(name)


@input_error
def find_command(*args):
    if not len(args):
        raise ValueNeedEnterError("Search word or other symbols")
    
    search_word = args[0]
    
    records = list()

    for key, record in address_book.data.items():
        if search_word in key or search_word in str(record):
            records.append(record)
    
    if len(records):
        return records
    else:
        return "No contacts find."


def exit_command(*args):
    return "Good bye!"
        

def unknown_command(*args):
    return f"Operation isn't possible. Can't recognized command. Use command 'help' for instructions."


@input_error
def contacts_in_period(period: int) -> str:
    result = address_book.congratulate(int(period))
    if result:
        return "\n".join(str(record) for record in result)
    else:
        return f"No birthdays in {period} days"


def show_all_command(*args):
    if address_book.data:
        records = list()

        for record in address_book.data.values():
            records.append(record)

        return records
    else:
        return "No contacts saved."


def hello_command(*args):
    return "How can I help you?"


@input_error
def change_email_command(*args):
    if not len(args):
        raise ValueNeedEnterError("Name")
    if len(args) < 2:
        raise ValueNeedEnterError("Email")
    
    name = Name(args[0])
    
    record = address_book.get(name.value)

    if record:
        email = Email(args[1])
        return record.change_email(email)
    else:
        raise FindRecordError(name)
    

@input_error
def change_address_command(*args):
    if not len(args):
        raise ValueNeedEnterError("Name")
    if len(args) < 2:
        raise ValueNeedEnterError("Address")
    
    name = Name(args[0])
    
    record = address_book.get(name.value)

    if record:
        address = Adress(args[1])
        return record.change_adress(address)
    else:
        raise FindRecordError(name)


@input_error
def change_birthday_command(*args) -> str:
    if not len(args):
        raise ValueNeedEnterError("Name")
    if len(args) < 2:
        raise ValueNeedEnterError("Birthday")
    
    name = Name(args[0])
    
    record = address_book.get(name.value)

    if record:
        birthday = Birthday(args[1])
        return record.change_adress(birthday)
    else:
        raise FindRecordError(name)


@input_error
def sort_files(path):
    try:
        result = subprocess.run(["python3", "sort.py", path], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e) 


@input_error
def help_command(*data) -> str:
    return "Available commands:\n" \
           "- hello\n" \
           "- add [name] [phone in format +380xxxxxxx] [birthday in format dd-mm-yyyy] [email] [adress]\n" \
           "- change [name] [phone]\n" \
           "- find [name]\n" \
           "- show_all\n" \
           "- edit [name]\n" \
           "- birthday [name] [date in format dd-mm-yyyy]\n" \
           "- period [number of days]\n" \
           "- help \n" \
           "- del [name] \n" \
           "- sort [path] \n" \
           "- bday [name] [new_birthday] for birthday change \n" \
           "- congrats [n] (n = days of period for Birthdays) \n" \
           "- bye, end, exit \n" \
           "- show-notes \n" \
           "- add-notes \n" \
           "- add-tag \n" \
           "- change-tag \n" \
           "- add-text \n" \
           "- change-text \n" \
           "- delete-note \n" \
           "- search-n \n" \
           "- fnt \n" \
           "- >>> space is the reserved argument separator character <<<"
  
    
# команди роботи з нотатками
@input_error
def show_notes(n_str):  # Це показуе або усі або по декілька
    if n_str > 0:
        long = len(notes_book)
        if long <= n_str:
            print("Ваш список нотаток:")
            for i in range(len(notes_book)):
                print(i+1," ",notes_book[i])
        else:
            print_one_page(n_str)    


def print_one_page(n):
    f = 0
    fn = 0
    for i in range(len(notes_book)):
        f = f + 1
        fn = fn + 1
        print(fn, " ", notes_book[i])
        if f == n:
            f = 0
            nn = True
            while nn:
                nn = input(f"Щоб подивитися наступні {n} нотаток натисніть Enter.")
                nn = False
    print("Всі нотаткии показано.\n")

## Загрузка та збереження. Потім можна доробити та  зберігати після кожного редактування    

@input_error
def load_note_book():
    path_note_book = ("save_note_book.bin")
    if os.path.exists(path_note_book):
        with open(resource_filename("catbook", path_note_book),"br") as fbr:
            fbr_list = pickle.load(fbr)
        return fbr_list
    else:
        return None 


@input_error
def save_note_book(list):
    path_note_book = ("save_note_book.bin")
    with open(resource_filename("catbook", path_note_book),"bw") as fwb:
        pickle.dump(list, fwb)
    print("Нотатки збережено.")

notes_book = Notes()
