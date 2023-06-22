import pymysql
from config import host, port, user, password, db_name

class PhoneBook:
    def __init__(self):
        self.__connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor)

    def __str__(self):
        contact_ids = self.get_contact_ids()
        with self.__connection.cursor() as cursor:
            # Формирование заголовка таблицы
            result = "id | name | discription | phone_numbers\n"
            # Формирование строк таблицы для каждого контакта
            for contact_id in contact_ids:
                contact = self.get_contact(contact_id)
                result += f"{contact_id} | {contact['name']} | {contact['discription']} | {', '.join(contact['phone_numbers'])}\n"
        return result


    def close(self):
        '''
        Функция позволяет правильно закрыть базу данных.
        !!!ВАЖНО ВСЕГДА ЗАКРЫВАТЬ БАЗУ ПОСЛЕ ЗАВЕРШЕНИЯ РАБОТЫ С НЕЙ!!!
        '''
        def close(self):
            if not self.__connection.open:
                print('Соединение уже закрыто')
            else:
                self.__connection.close()

    def add_contact(self, id: int, name: str, discription: str, numbers: list[str]):
        '''
        Функция позволяет добавить новый контакт в базу phone_book
            id :int - Идентификатор контакта
            name :str - Имя контакта (до 255 символов)
            discription :str - Описание контакта (до 255 символов)
            numbers :list[str] - Список телефонных номеров (до 12 символов)

        Настройки самой базы данных хранятся в файле 'config.py'
        '''
        if id:
            try:
                with self.__connection.cursor() as cursor:
                    # Добавление контакта в таблицу contact
                    add_contact_query = "INSERT INTO contact (id, name, discription) VALUES (%s, %s, %s)"
                    cursor.execute(add_contact_query, (id, name, discription))

                    # Добавление телефонных номеров в таблицу phone_number
                    add_phone_number_query = "INSERT INTO phone_number (contact_id, number) VALUES (%s, %s)"
                    for phone_number in numbers:
                        cursor.execute(add_phone_number_query, (id, phone_number))
                    self.__connection.commit()
            except Exception as Ex:
                print(f'При создании возникла ошибка: {Ex}')

    def get_contact(self, contact_id: int):
        '''
         функция возвращает информацию о контакте с указанным contact_id :int
        '''
        try:
            with self.__connection.cursor() as cursor:
                # Получение данных контакта из таблицы contact
                get_contact_query = "SELECT name, discription FROM contact WHERE id = %s"
                cursor.execute(get_contact_query, (contact_id,))
                contact = cursor.fetchone()

                # Получение телефонных номеров контакта из таблицы phone_number
                get_phone_numbers_query = "SELECT number FROM phone_number WHERE contact_id = %s"
                cursor.execute(get_phone_numbers_query, (contact_id,))
                phone_numbers = [row['number'] for row in cursor.fetchall()]

                # Формирование результата в виде словаря
                result = {
                    'name': contact['name'],
                    'discription': contact['discription'],
                    'phone_numbers': phone_numbers
                }

                return result
        except Exception as Ex:
            print(f'Возникла ошибка: {Ex}')

    def delete_contact(self, contact_id: int):
        '''
        Функция позволяет удалить контакт и все его номера телефонов из базы данных
            contact_id :int - ID контакта, который нужно удалить
        '''
        try:
            with self.__connection.cursor() as cursor:
                # Удаление телефонных номеров контакта из таблицы phone_number
                delete_phone_numbers_query = "DELETE FROM phone_number WHERE contact_id = %s"
                cursor.execute(delete_phone_numbers_query, (contact_id,))

                # Удаление контакта из таблицы contact
                delete_contact_query = "DELETE FROM contact WHERE id = %s"
                cursor.execute(delete_contact_query, (contact_id,))
                self.__connection.commit()
        except Exception as Ex:
            print(f'Возникла ошибка: {Ex}')

    def update_contact(self, contact_id: int, name: str, discription: str, numbers: list[str]):
        '''
        Функция обновляет информацию о контакте с указанным contact_id
            contact_id :int - ID контакта, который нужно удалить
            name :str - Имя контакта ()до 255 символов)
            discription :str - Описание контакта (до 255 символов)
            numbers : ist[str] - Список телефонных номеров (до 12 символов)

        Настройки самой базы данных хранятся в файле 'config.py'
        '''
        try:
            with self.__connection.cursor() as cursor:
                # Обновление информации о контакте в таблице contact
                update_contact_query = "UPDATE contact SET name = %s, discription = %s WHERE id = %s"
                cursor.execute(update_contact_query, (name, discription, contact_id))

                # Удаление старых телефонных номеров контакта из таблицы phone_number
                delete_phone_numbers_query = "DELETE FROM phone_number WHERE contact_id = %s"
                cursor.execute(delete_phone_numbers_query, (contact_id,))

                # Добавление новых телефонных номеров в таблицу phone_number
                add_phone_number_query = "INSERT INTO phone_number (contact_id, number) VALUES (%s, %s)"
                for phone_number in numbers:
                    cursor.execute(add_phone_number_query, (contact_id, phone_number))
                self.__connection.commit()
        except Exception as Ex:
            print(f'Возникла ошибка: {Ex}')

    def get_contact_ids(self):
        '''
        Функция возвращает список из всех имеющихся в базе id :int
        '''
        try:
            with self.__connection.cursor() as cursor:
                # Получение ID всех контактов из таблицы contact
                get_contact_ids_query = "SELECT id FROM contact"
                cursor.execute(get_contact_ids_query)
                contact_ids = [row['id'] for row in cursor.fetchall()]

                return contact_ids
        except Exception as Ex:
            print(f'Возникла ошибка: {Ex}')


if __name__ == '__main__':
    phone_book = PhoneBook()
    print(phone_book)
    # for id in phone_book.get_contact_ids():
    #     phone_book.delete_contact(id)
    # print(phone_book)
