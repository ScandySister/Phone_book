from PhoneBookAPI import PhoneBook

phone_book = PhoneBook()

with open('contacts.txt', 'r', encoding='utf-8') as file:
    for line in file:
        # Разделение строки на значения
        values = line.strip().split(';')
        id = int(values[0])
        name = values[1]
        description = values[2]
        phone_numbers = values[3].split(',')
        phone_book.add_contact(id=id, name=name, discription=description, numbers=phone_numbers)
