from abc import ABC, abstractmethod
from catbook.bot import *
from catbook.AddressBook import *
from rich.console import Console
from catbook.classes import *
from catbook.note_tag import *


# for package install
VERSION = "1.0.0"


COMMANDS = {
    add_command: ("add", "+", "2","adding","append"),
    change_command: ("change", "зміни", "3"),
    exit_command: ("bye", "exit", "end","GoodBye", "0"),
    delete_contact_command:("del","8", "delete"),
    find_command: ("find", "4"),
    show_all_command: ("show-all", "5", "show","showing"),
    hello_command:("hello", "1"),
    edit_name_command: ("edit", "7","rename"),
    change_birthday_command: ("change-bday", "6","change-birthday", "changebday","changebirthday"),
    change_email_command: ("change-email", "9", "change-mail", "changemail", "changeemail"),
    change_address_command: ("change-address", "10","changeaddress"),
    sort_files: ("sort","sorting"),
    contacts_in_period: ("period", "bdays","congrats"),
    help_command: ("help"),
    show_notes: ("show-notes", "n5"),
    make_note: ("make-notes", "add-notes", "+n"),
    bot_add_teg: ("add-tag","+t"),
    bot_change_teg: ("change-tag","=t"),
    bot_add_text_note: ("add-text"),
    bot_change_text_note: ("change-text","=text"),
    delete_note_by_number: ("delete-note","-n"),
    search_notes: ("search-n","search-notes","search-tag","fnt")
        
}


def parser(text: str):
    text_lst = text.split(" ")
    for cmd, kwds in COMMANDS.items():
        kwd = text_lst[0]
        if len(text_lst) and kwd in kwds:
            data = text[len(kwd):].strip().split()
            return cmd, data

    matches = get_closest_matches(text, COMMANDS)
    if matches:
        return closest_matches_suggestion, (matches,)

    return unknown_command, [text]


class ConsoleOutputAbstract(ABC):
    @abstractmethod
    def output(self, some_message, *args) -> str:
        pass


class TextOutput(ConsoleOutputAbstract):
    def output(self, message: str, *args) -> None:
        return print(message)


class TableOutput(ConsoleOutputAbstract):
    def output(self, records: list, *args) -> None:
        table = Table(show_header=True, header_style="bold", box=box.ROUNDED)
        table.add_column("Name")
        table.add_column("Phone number")
        table.add_column("Birthday", style="dim")
        table.add_column("Email")
        table.add_column("Adress")

        for record in records:
            name = str(record.name)
            phone_numbers = ', '.join([str(phone) for phone in record.phones])
            birthday = str(record.birthday) if record.birthday else "N/A"
            email = str(record.email) if record.email else "N/A"
            adress = str(record.adress) if record.adress else "N/A"
            table.add_row(name, phone_numbers, birthday, email, adress)

        console = Console()
        console.print(table)


class ConsoleHandler:
    def __init__(self, command_output: ConsoleOutputAbstract):
        self.__output_processor = command_output
        
    def send_message(self, message) -> None:
        self.__output_processor.output(message)


def main():
    text_output = TextOutput()
    table_output = TableOutput()

    text_handler = ConsoleHandler(text_output)
    table_handler = ConsoleHandler(table_output)
    
    text_handler.send_message('Hello. I am your contact-assistant.\nWhat can I do for you?')
    
    while True:
        user_input = input("enter command--->>> ")

        cmd, data = parser(user_input)

        if cmd == exit_command:
            text_handler.send_message("Goodbye!")
            break

        result = cmd(*data)

        if isinstance(result, str):
            text_handler.send_message(result)
        else:
            table_handler.send_message(result)

 


if __name__ == "__main__":
    main()