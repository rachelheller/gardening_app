from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from garden_api_client import GardenAPIClient


class AddGardenScreen(Screen):

    def new_garden_popup(self):
        name = self.ids.garden_name.text
        notes = self.ids.garden_notes.text
        if name == "" and notes == "":
            self.error_message("You must enter at least one value.")
        elif name == "":
            self.error_message("The garden must have a name.")
        else:
            new_info_confirm_screen = self.manager.get_screen("confirm_new_info_screen")
            new_info_confirm_screen.ids.new_info_label.text = f"Is this information correct?\nName: {name}\nNotes: {notes}"
            new_info_confirm_screen.ids.confirmed_button.on_press = lambda: self.info_confirmed(name, notes)
            self.manager.current = "confirm_new_info_screen"

    def error_message(self, message):
        layout = GridLayout(cols=1, padding=10)
        error_message = Label(text=message, font_size="20sp")
        edit_info = Button(text="Back", size_hint=(0.1, 0.1))
        layout.add_widget(error_message)
        layout.add_widget(edit_info)
        empty_fields_popup = Popup(title="There Is A Problem.", content=layout)
        empty_fields_popup.open()
        edit_info.bind(on_press=empty_fields_popup.dismiss)

    def info_confirmed(self, name, notes):
        response = App.get_running_app().loop.run_until_complete(GardenAPIClient.create_garden(name, notes))
        if response:
            self.clear_text_input_fields()
            screen = self.manager.get_screen("confirmation_screen")
            screen.ids.success_message.text = "Your garden is successfully added!"
            screen.ids.back_button.text = "Add Garden"
            screen.ids.back_button.on_press = lambda: self.go_back()
            self.manager.current = "confirmation_screen"
        else:
            print("Not added to database.")

    def go_back(self):
        self.manager.current = "add_garden_screen"

    def clear_text_input_fields(self):
        self.ids.garden_name.text = ""
        self.ids.garden_notes.text = ""
