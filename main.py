from kivy.app import App
from kivy.config import Config
Config.set("graphics","width",360)
Config.set("graphics","height",640)
Config.set("graphics","resizable","0")

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView

from PhoneBookAPI import PhoneBook
from custom_widgets import SearchInput, Contact, ToolBar, DeleteConfirmation


class phone_bookApp(App):
    def build(self):
        self.main_window = AnchorLayout()
        self.main_window.add_widget(Image(source = 'images/background.jpg'))
        self.gui_box = BoxLayout(orientation = 'vertical')
        tool_bar = ToolBar()

        self.phone_book = PhoneBook()
        screen_manager = ScrollView(do_scroll_x = False)
        self.contact_list = BoxLayout(orientation='vertical',
            spacing = 5,
            size_hint_y=None)
        self.contact_list.bind(minimum_height=self.contact_list.setter('height'))
        screen_manager.add_widget(self.contact_list)

        self.contacts = {}

        self.add_contact_button = Button(text = 'Создать новый контакт',
            color = (0,0,0,1),
            size_hint = [1,.15],
            background_normal = 'images/blue_button.png',
            on_press = self.add_contact
            )

        self.save_contact_button = Button(text = 'Сохранить',
            size_hint = [1,.15],
            background_normal = 'images/green_button.png',
            on_press = self.on_save_button_pressed
            )
        self.editing_contact = None

        self.delete_confirmation = DeleteConfirmation()

        self.gui_box.add_widget(tool_bar)
        self.gui_box.add_widget(screen_manager)
        self.gui_box.add_widget(self.add_contact_button)

        self.main_window.add_widget(self.gui_box)

        self.load_contacts()
        return self.main_window

    def on_stop(self):
        self.phone_book.close()

    def search(self, value :str):
        contacts_by_num = []
        for key, contact in self.contacts.items():
            numbers = self.phone_book.get_contact(key)['phone_numbers']
            for number in numbers:
                if value in number:
                    contacts_by_num.append(key)
        contacts_by_name = []
        for key, contact in self.contacts.items():
            if value.lower() in contact.name.text.lower():
                contacts_by_name.append(key)

        result = list(set(contacts_by_num + contacts_by_name))
        self.update_contact_list(contacts = result)

    def update_contact_list(self, contacts):
        self.contact_list.clear_widgets()
        for id in contacts:
            self.contact_list.add_widget(self.contacts[id])

    def load_contacts(self):
        contact_ids = self.phone_book.get_contact_ids()
        loaded_contacts = {id: self.phone_book.get_contact(id) for id in contact_ids}
        for loaded_id in loaded_contacts:
            self.add_contact(id = loaded_id, contact = loaded_contacts[loaded_id])

    def save_add_toggle(self):
        if self.add_contact_button in self.gui_box.children:
            self.gui_box.remove_widget(self.add_contact_button)
            self.gui_box.add_widget(self.save_contact_button)
            for id in self.contacts:
                self.contacts[id].hide_edit_buttons()
        elif self.save_contact_button in self.gui_box.children:
            self.gui_box.remove_widget(self.save_contact_button)
            self.gui_box.add_widget(self.add_contact_button)
            for id in self.contacts:
                self.contacts[id].show_edit_buttons()

    def add_contact(self, *args, id = None, contact = None):
        if not id:
            is_new_contact  = True
            contact_ids = self.phone_book.get_contact_ids()
            if len(contact_ids) > 0:  id = contact_ids[-1]+1
            else: id = 1
            contact = {'name':'','discription':'','phone_numbers': ['+7']}
        else: is_new_contact  = False

        self.contacts[id] = Contact()
        self.contacts[id].name.text = contact['name']
        self.contacts[id].discription.text = contact['discription']
        self.contact_list.add_widget(self.contacts[id])
        self.editing_contact = self.contacts[id]
        for current_number in contact['phone_numbers']:
            self.contacts[id].add_number(number = current_number)
        if not is_new_contact :
            self.save_contact(id = id)
        self.save_add_toggle()

    def on_save_button_pressed(self, *args):
            self.save_contact()

    def save_contact(self, *args, id = None):
        contact = self.editing_contact
        name = contact.name.text
        discription = contact.discription.text
        numbers = [number.text for number in contact.numbers]

        if not id:
            for key, value in self.contacts.items():
                if value == contact:
                    id = key
            if id in self.phone_book.get_contact_ids():
                self.phone_book.update_contact(contact_id = id,
                    name = name,
                    discription = discription,
                    numbers = numbers)
            else:
                self.phone_book.add_contact(id = id,
                    name = name,
                    discription = discription,
                    numbers = numbers)

        contact.name.save()
        contact.discription.save()
        list(map(lambda number: number.save(), contact.numbers))

        contact.height-=contact.add_number_button.height+contact.text_box.spacing
        contact.text_box.remove_widget(contact.add_number_button)
        contact.hide_delete_buttons()
        self.save_add_toggle()
        self.editing_contact = None

    def delete_contact(self, contact):
        id = next(key for key, value in self.contacts.items() if value == contact)
        self.phone_book.delete_contact(id)
        self.contact_list.remove_widget(self.contacts[id])
        del self.contacts[id]


if __name__ == '__main__':
    phone_bookApp().run()
