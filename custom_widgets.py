from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle

class SearchInput(TextInput):
    def __init__(self, **kwargs):
        super(SearchInput, self).__init__(**kwargs)
        self.background_color = (0,0,0,0)
        self.multiline = False
        self.font_size = 18
        with self.canvas.before:
            Color(rgba=(0, 0, 0, .5))
            self.rect = RoundedRectangle(radius=[15], size=self.size, pos=self.pos)
            Color(rgba=(1,1,1,.7))
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class CustomInput(TextInput):
    def __init__(self, **kwargs):
        super(CustomInput, self).__init__(**kwargs)
        self.foreground_color = (1,1,1,1)
        self.background_color = (.1,.1,.1,1)
        self.cursor_color = (1,1,1,.4)
        self.size_hint_y = None

    def save(self):
        self.readonly = True
        self.background_color = (1,1,1,0)
        self.cursor_color = (1,1,1,0)
        self.foreground_color = (1,1,1,1)

    def edit(self):
        self.readonly = False
        self.foreground_color = (1,1,1,.9)
        self.background_color = (.1,.1,.1,1)
        self.cursor_color = (1,1,1,.4)


class NameInput(CustomInput):
    def __init__(self, **kwargs):
        super(NameInput, self).__init__(**kwargs)
        self.multiline = False
        self.max_length = 10
        self.font_size = 18
        self.height = 35


class DiscriptionInput(CustomInput):
    def __init__(self, **kwargs):
        super(DiscriptionInput, self).__init__(**kwargs)
        self.multiline = True
        self.max_length = 82
        self.font_size = 11
        self.height = 40

    def insert_text(self, substring, from_undo=False):
        if len(self.text) + len(substring) > self.max_length:
            substring = substring[:self.max_length - len(self.text)]
        super(DiscriptionInput, self).insert_text(substring, from_undo=from_undo)


class NumberInput(CustomInput):
    def __init__(self, **kwargs):
        super(NumberInput, self).__init__(**kwargs)
        self.multiline = False
        self.max_length = 12
        self.font_size = 14
        self.height = 30

    def insert_text(self, substring, from_undo=False):
        s = ''.join([char for char in substring if char.isdigit()])
        if len(self.text) + len(s) > self.max_length:
            s = s[:12 - len(self.text)]
        selection = self.selection_text
        if self.selection_from < 2: return
        cursor_pos = self.cursor_index()
        if cursor_pos < 2: return
        return super(NumberInput, self).insert_text(s, from_undo=from_undo)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        cursor_pos = self.cursor_index()
        if cursor_pos <= 2: return
        return super(NumberInput, self).do_backspace(from_undo=from_undo, mode=mode)

    def delete_selection(self, from_undo=False):
        selection = self.selection_text
        if self.selection_from <= 2:
            self.cancel_selection()
            return
        return super(NumberInput, self).delete_selection(from_undo=from_undo)


class ToolBar(AnchorLayout):
    def __init__(self, **kwargs):
        super(ToolBar, self).__init__(**kwargs)
        self.size_hint = [1, .1]
        background = Button(disabled = True,
            background_disabled_normal = 'images/background_texture.png')
        self.add_widget(background)
        tool_bar_box = BoxLayout(orientation = 'horizontal',
            spacing = 5,
            padding = [5,5,5,5])
        self.add_widget(tool_bar_box)

        exit_button = Button(text = '<',
            color = (0,0,0,1),
            on_press=self.to_exit,
            size_hint = [None, None],
            background_normal = 'images/white_button.png',
            size = (50,35))
        tool_bar_box.add_widget(exit_button)

        search_bar = SearchInput(
            size_hint = [5, 1],
            hint_text = 'Поиск...',
            on_text_validate=self.to_search
        )
        tool_bar_box.add_widget(search_bar)

    def to_exit(self, *arg):
        App.get_running_app().stop()

    def to_search(self, arg):
        value = arg.text
        App.get_running_app().search(value = value)


class Contact(AnchorLayout):
    def __init__(self, **kwargs):
        super(Contact, self).__init__(**kwargs)
        background =  Button(disabled = True,
            background_disabled_normal = 'images/background_texture.png')
        self.add_widget(background)
        self.size_hint_y = None
        self.height = 120
        # Основное тело контакта
        self.horizontal_box = BoxLayout(orientation = 'horizontal',
            spacing = 2,
            padding = [5,5,5,5])
        self.add_widget(self.horizontal_box)
        # Изображение контакта
        self.contact_image = Button(disabled = True,
            pos_hint = {'top': 1},
            size_hint = [None,None],
            size = [50,50],
            background_disabled_normal = 'images/new_contact.png')
        self.horizontal_box.add_widget(self.contact_image)
        # Вертикальный слой с TextInput
        self.text_box = BoxLayout(orientation = 'vertical',
            spacing = 2)
        self.horizontal_box.add_widget(self.text_box)
        # Содержимое текстового слоя
        self.name = NameInput(text = '')
        self.discription = DiscriptionInput(text = '')
        self.text_box.add_widget(self.name)
        self.text_box.add_widget(self.discription)
        # Кнопка добавления номера
        self.add_number_button = Button(text = '+',
            on_press = self.add_number,
            size_hint_y = None,
            background_normal = 'images/blue_button.png',
            height = 35)
        self.text_box.add_widget(self.add_number_button)
        # Кнопка редактирования
        self.edit_button = Button(text = '...',
            color = (0,0,0,1),
            pos_hint = {'top': 1},
            size_hint = [None,None],
            size = [35,35],
            background_normal = 'images/white_button.png',
            on_press = self.on_edit_button_press)
        # Кнопка удаления
        self.horizontal_box.add_widget(self.edit_button)
        self.delite_button = Button(text = 'x',
            pos_hint = {'top': 1},
            size_hint = [None,None],
            background_normal = 'images/red_button.png',
            size = [35,35],
            on_press = self.on_delite_button_press)
        # Список номеров
        self.numbers = []

    def hide_edit_buttons(self):
        if self.edit_button in self.horizontal_box.children:
            self.horizontal_box.remove_widget(self.edit_button)
            self.horizontal_box.add_widget(self.delite_button)

    def show_edit_buttons(self):
        if self.delite_button in self.horizontal_box.children:
            self.horizontal_box.remove_widget(self.delite_button)
            self.horizontal_box.add_widget(self.edit_button)

    def hide_delete_buttons(self):
        for number in self.numbers:
            for widget in number.parent.children:
                if isinstance(widget, Button):
                    number.parent.remove_widget(widget)

    def show_delete_buttons(self):
        for number in self.numbers:
            number.parent.add_widget(Button(text = 'x',
                size_hint = (None, None),
                size = (number.height, number.height),
                background_normal = 'images/red_button.png',
                on_press = self.delete_number))

    def add_number(self, *args, number = '+7'):
        number = NumberInput(text = number)
        self.numbers.append(number)
        self.text_box.remove_widget(self.discription)
        self.text_box.remove_widget(self.add_number_button)

        number_box = BoxLayout(orientation = 'horizontal',
            size_hint_y = None,
            height = number.height)
        number_box.add_widget(number)
        self.text_box.add_widget(number_box)

        number_box.add_widget(Button(text = 'x',
            background_normal = 'images/red_button.png',
            size_hint = (None, None),
            size = (number.height, number.height),
            on_press = self.delete_number))

        self.height += number.height + self.text_box.spacing
        self.text_box.add_widget(self.discription)
        self.text_box.add_widget(self.add_number_button)

    def delete_number(self, button):
        number_box = button.parent
        for widget in number_box.children:
            del widget
        number_box.parent.remove_widget(number_box)
        # Удалить номер из базы
        self.height -= button.height + self.text_box.spacing

    def on_delite_button_press(self, *args):
        main_window = App.get_running_app().main_window
        main_window.add_widget(App.get_running_app().delete_confirmation)
        App.get_running_app().delete_confirmation.contact = self

    def on_edit_button_press(self, *args):
        self.show_delete_buttons()
        self.name.edit()
        self.discription.edit()
        list(map(lambda number: number.edit(), self.numbers))
        self.text_box.add_widget(self.add_number_button)

        self.height += self.add_number_button.height + self.text_box.spacing
        App.get_running_app().editing_contact = self
        App.get_running_app().save_add_toggle()


class DeleteConfirmation(AnchorLayout):
    def __init__(self, **kwargs):
        super(DeleteConfirmation, self).__init__(**kwargs)
        self.contact = None
        background =  Button(disabled = True,
            background_disabled_normal = 'images/background_texture.png')
        self.add_widget(background)
        self.size_hint = (.5, .25)
        vertical_box = BoxLayout(orientation = 'vertical',
            size_hint = (.9,.6))
        vertical_box.add_widget(Label(text = 'Удалить контакт?'))
        horizontal_box = BoxLayout(orientation = 'horizontal', spacing = 5)
        cancel_button = Button(text = 'Нет',
            background_normal = 'images/blue_button.png',
            size_hint = (None,None),
            size = (75,50),
            on_press = self.on_cancel_button_pressed)
        del_confirm_button = Button(text = 'Да',
            background_normal = 'images/red_button.png',
            size_hint = (None,None),
            size = (75,50),
            on_press = self.on_del_confirm_button_pressed)
        horizontal_box.add_widget(cancel_button)
        horizontal_box.add_widget(del_confirm_button)
        vertical_box.add_widget(horizontal_box)
        self.add_widget(vertical_box)

    def on_del_confirm_button_pressed(self, button):
        App.get_running_app().delete_contact(self.contact)
        main_window = App.get_running_app().main_window
        main_window.remove_widget(App.get_running_app().delete_confirmation)
        App.get_running_app().delete_confirmation.contact = None

    def on_cancel_button_pressed(self, button):
        main_window = App.get_running_app().main_window
        main_window.remove_widget(App.get_running_app().delete_confirmation)
        App.get_running_app().delete_confirmation.contact = None
