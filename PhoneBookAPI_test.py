import unittest
from PhoneBookAPI import Phonebook

class TestPhonebook(unittest.TestCase):
    def setUp(self):
        self.phonebook = Phonebook()

    def test_add_contact(self):
        # Добавление нового контакта
        self.phonebook.add_contact(id=1, name='Test', discription='Test description', numbers=['+1234567890'])
        # Проверка, что контакт добавлен в базу данных
        contact = self.phonebook.get_contact(1)
        self.assertEqual(contact['name'], 'Test')
        self.assertEqual(contact['discription'], 'Test description')
        self.assertEqual(contact['phone_numbers'], ['+1234567890'])

    def test_get_contact(self):
        # Добавление нового контакта
        self.phonebook.add_contact(id=1, name='Test', discription='Test description', numbers=['+1234567890'])
        # Получение информации о контакте
        contact = self.phonebook.get_contact(1)
        # Проверка, что информация о контакте корректна
        self.assertEqual(contact['name'], 'Test')
        self.assertEqual(contact['discription'], 'Test description')
        self.assertEqual(contact['phone_numbers'], ['+1234567890'])

    def test_delete_contact(self):
        # Добавление нового контакта
        self.phonebook.add_contact(id=1, name='Test', discription='Test description', numbers=['+1234567890'])
        # Удаление контакта
        self.phonebook.delete_contact(1)
        # Проверка, что контакт удален из базы данных
        contact_ids = self.phonebook.get_contact_ids()
        self.assertNotIn(1, contact_ids)

    def test_update_contact(self):
        # Добавление нового контакта
        self.phonebook.add_contact(id=1, name='Test', discription='Test description', numbers=['+1234567890'])
        # Обновление информации о контакте
        self.phonebook.update_contact(contact_id=1, name='Updated', discription='Updated description', numbers=['+0987654321'])
        # Получение обновленной информации о контакте
        contact = self.phonebook.get_contact(1)
        # Проверка, что информация о контакте обновлена
        self.assertEqual(contact['name'], 'Updated')
        self.assertEqual(contact['discription'], 'Updated description')
        self.assertEqual(contact['phone_numbers'], ['+0987654321'])

    def test_get_contact_ids(self):
        # Добавление нескольких новых контактов
        self.phonebook.add_contact(id=1, name='Test 1', discription='Test description 1', numbers=['+1234567890'])
        self.phonebook.add_contact(id=2, name='Test 2', discription='Test description 2', numbers=['+0987654321'])
        # Получение списка идентификаторов контактов
        contact_ids = self.phonebook.get_contact_ids()
        # Проверка, что список идентификаторов корректен
        self.assertIn(1, contact_ids)
        self.assertIn(2, contact_ids)

if __name__ == '__main__':
    unittest.main()
