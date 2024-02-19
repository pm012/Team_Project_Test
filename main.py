"""Module providing a function """
import pickle
from collections import UserDict
from datetime import datetime
from class_file import AddressBook,Record

def decorator(func):
    """Decorator"""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return "Enter the correct command"
        except ValueError:
            return "Enter correct command"
        except IndexError:
            return "Enter the correct command, name and phone number"
        except NameError as e:
            return f"{e}"
        except FileNotFoundError:
            global book
            book = AddressBook()
            with open('Data.bin', 'wb') as file:
                pickle.dump(book, file)
                return "Create Data"
        except Exception as e:
            return f"{e}"
    return wrapper

@decorator
def start():
    """Load data"""
    with open('Data.bin', 'rb') as file:
        global book
        book = pickle.load(file)
    return "Bot start"

def save():
    """Save data"""
    global book
    with open('Data.bin', 'wb') as file:
        pickle.dump(book, file)

def command_hello():
    """Function Hello"""
    return "How can I help you?"

def command_add_record(name,phone):
    """Adding a contact to the Address Book"""
    new_record = Record(name)
    new_record.add_phone(phone)
    book.add_record(new_record)
    return "Contact added successfully"

def command_find_record(value):
    """Find a contact in the Address Book"""
    for i in book.iterator(value):
        print(i)
    #return book.iterator(value)

def command_delete_record(name):
    """Deleting a contact in the Address Book"""
    if book.find(name):
        book.delete(name)
        return f"Contact {name} deleted"

def command_update_phone(name,phone):
    """Adding a phone number"""
    if book.find(name):
        new_phone = book.find(name)
        new_phone.add_phone(phone)
        return new_phone

def command_remove_phone(name, phone):
    """Deleting a phone number"""
    if book.find(name):
        record = book.find(name)
        record.remove_phone(phone)
        return record

def command_edit_phone(name,phone_one,phone_two):
    """Changing the phone number"""
    if book.find(name):
        record = book.find(name)
        record.edit_phone(phone_one,phone_two)
        return record

def command_show_all():
    """Function show all phone number"""
    for contact in book.values():
        print(f'{contact}')

def command_add_note(name,note):
    """Function add note"""
    if book.find(name):
        record = book.find(name)
        record.add_note(note)
        return "Note added successfully"

def command_delete_note(name):
    """Function delete note"""
    record = book.find(name)
    if record:
        record.delete_note()
        return "Note delete"

def command_edit_note(name,note):
    """Function edit note"""
    record = book.find(name)
    if record:
        record.edit_note(note)
        return "Note edit"

def command_find_note(value):
    """Function find note"""
    for i in book.find_note(value):
        print(i)

def command_good_bye():
    """Function close bot"""
    global ACTIVE_BOT
    ACTIVE_BOT = False
    return "Good Bye!"

def get_command(command):
    """Function command bot"""
    return command_list[command]

def command_add_address(name, address):
    """Adding a address"""
    if book.find(name):
        new_address = book.find(name)
        new_address.add_address(address)
        return "Address added successfully"

def command_add_email(name, email):
    """Adding a email"""
    if book.find(name):
        new_email = book.find(name)
        new_email.add_email(email)
        return "Email added successfully"

def command_add_birthday(name, birthday):
    """Adding a birthday"""
    if book.find(name):
        new_birthday = book.find(name)
        new_birthday.add_birthday(birthday)
        return "Birthday added successfully"

command_list = {
        "hello": command_hello,
        "add": command_add_record,
        "find": command_find_record,
        "delete": command_delete_record,

        "update" : command_update_phone,
        "remove": command_remove_phone,
        "edit": command_edit_phone,

        "show all": command_show_all,
        "good bye": command_good_bye,
        "close": command_good_bye,
        "exit": command_good_bye,

        "add-address": command_add_address,
        "add-email": command_add_email,
        "add-birthday": command_add_birthday,

        "write": command_add_note,
        "delete-note": command_delete_note,
        "edit-note": command_edit_note,
        "find-note": command_find_note,
    }

ACTIVE_BOT = False
book = None

@decorator
def command_parser(user_input):
    """Сommand parser"""
    if user_input in ["show all", "hello", "good bye", "close", "exit"]:
        return get_command(user_input)()
    else:
        user_input = user_input.split()
        if user_input[0] in ["phone", "delete", "find", "delete-note", "find-note",]:
            return get_command(user_input[0])(user_input[1])
        elif user_input[0] in ["remove", "update", "add", "add-email", "add-birthday"]:
            return get_command(user_input[0])(user_input[1],(user_input[2]))
        elif user_input[0] in ["write","add-address", "edit-note"]:
            return get_command(user_input[0])(user_input[1],(user_input[2:]))
        elif user_input[0] in ["edit"]:
            return get_command(user_input[0])(user_input[1],(user_input[2]),(user_input[3]))
        else:
            raise ValueError()

def main():
    """Bot"""
    print(start())
    global ACTIVE_BOT
    ACTIVE_BOT = True
    while ACTIVE_BOT:
        user_input = input("Enter the command: ").lower().strip()
        print(command_parser(user_input))
        save()

main()
#The file ends
