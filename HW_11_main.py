import re
from HW_11_contact_book import Record, AddressBook

contacts = AddressBook()  

def input_error(funk):
      
    def inner(*args,**kwargs):  

        try:
            return funk(*args,**kwargs)
        except KeyError: 
            return "This name does not exist."
        except IndexError:
            return "Did not receive all information."
        except ValueError:
            return "Did not receive a correct format ('%Y-%m-%d' for date or 3-12 items for number)."
        except:
            return "Option entered incorrectly."

    return inner

@input_error
def add(text):
    phone_number = get_phone(text)
    phone_name = get_name(text)
    if contacts.data.get(phone_name):
        record = contacts[phone_name]
    else:
        record = Record(phone_name)
    record.add(phone_number)
    contacts.add_record(record)
    return "Number added. Something else?"

@input_error
def add_bday(text):
    phone_name = get_name(text)
    birthday = get_birthday(text)

    if  contacts.data.get(phone_name):
        record = contacts[phone_name]
        record.add_birthday(birthday)
        contacts.change_record(record)
    else:
        record = Record(phone_name)
        record.add_birthday(birthday)
        contacts.add_record(record)
    
    return "Birthday added. Something else?"

@input_error
def change(text):
    phone_number = get_phone(text)
    phone_name = get_name(text)
    for name, numbers in contacts.items():
        if name == phone_name:
            old_phone_number = [number.value for number in numbers.phone_numbers]
    record = Record(phone_name)
    record.change(phone_number, old_phone_number)
    contacts.change_record(record)
    result = f"{phone_name}\'s number {old_phone_number} changed to {phone_number}. Something else?"
    return result

@input_error
def days_to_birthday(text):
    name = re.findall(r"[a-z]+", text, flags=re.IGNORECASE)[-1].title()
    days = contacts[name].days_to_birthday()
    if days == None:
        return f"Don't have {name}'s bithday"
    return f"{days} days yet"

@input_error
def delete(text):
    phone_number = get_phone(text)
    phone_name = get_name(text)
    record = contacts[phone_name]
    return record.delete(phone_number)

@input_error
def end(text):
    return "Good bye!"

def get_birthday(text):    
    birthday = re.findall(r"\d{4}-\d{2}-\d{2}", text)[0]
    return birthday
    
def get_name(text):
    phone_name = re.findall(r"[a-z]+", text, flags=re.IGNORECASE)[1].title()
    return phone_name

def get_phone(text):
    phone_number = re.findall(r"\d+", text)[-1]
    return phone_number
  
@input_error
def hello(text):
    return "How can I help you?"

@input_error
def iterator(text):
    n = int(re.findall(r"\d+", text)[-1])
    result = ""
    page = 1
    for item in contacts.iterator(n):
        if item:
            result += f"Page №{page} \n"
        for record in item:
            result += f"{record} \n"
        page += 1
        return result

@input_error
def phone(text):
    phone_name = get_name(text)
    return contacts.find_contact(phone_name)

@input_error
def show_all(text):
    result = ""
    for item in contacts.show_all():
        result += item + "\n"
    return result

def main():

    start = True

    while start:
        access = False
        entered_text = input()
        
        for key in user_command.keys():
            if bool(re.search(key, entered_text, flags=re.IGNORECASE)):
                access = True
                print(user_command[key](entered_text))

                if key in ["exit","good bye","close"]:
                    start = False  
                break
      
        if not access:
            print("Option entered incorrectly...")
               
      
user_command = {
    "add": add, # додає номер телефону
    "birthday": add_bday, # додає дату народження '%Y-%m-%d'
    "change": change,
    "days to bday": days_to_birthday,
    "delete": delete,
    "exit": end,
    "good bye": end,
    "close": end,
    "hello": hello,
    "pages": iterator,
    "phone": phone,
    "show all": show_all,    
}


if __name__ == "__main__":
    main()