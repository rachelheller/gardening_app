from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from garden_api_client import GardenAPIClient


class UpdateGarden(Screen):

    def populate_current_info(self):
        current_garden = App.get_running_app().current_garden_info
        self.ids.garden_name_edit.text = current_garden[1]
        self.ids.garden_notes_edit.text = current_garden[2]

    def complete_garden_update(self, new_name, new_notes):
        garden_id = App.get_running_app().current_garden_info[0]
        response = App.get_running_app().loop.run_until_complete(GardenAPIClient.update_garden(garden_id, new_name, new_notes))
        if response:
            new_garden_info = App.get_running_app().loop.run_until_complete(GardenAPIClient.get_garden(garden_id))
            for garden in new_garden_info:
                App.get_running_app().current_garden_info = garden
            self.manager.get_screen("show_garden_screen").populate_info()
            self.manager.current = "show_garden_screen"
        else:
            print("Not updated")

    def review_updated_garden_info(self):
        layout = GridLayout(cols=1, padding=10)
        new_name = self.ids.garden_name_edit.text
        new_notes = self.ids.garden_notes_edit.text

        if new_name == "" and new_notes == "":
            error_message = Label(text="You must enter at least one value", font_size="20sp")
            edit_info = Button(text="Back", size_hint=(0.1, 0.1))
            layout.add_widget(error_message)
            layout.add_widget(edit_info)
            empty_fields_popup = Popup(title="All Fields Empty", content=layout)
            empty_fields_popup.open()
            edit_info.bind(on_release=empty_fields_popup.dismiss)
        else:
            confirm_info_screen = self.manager.get_screen("confirm_new_info_screen")
            confirm_info_screen.ids.new_info_label.text = f"Name: {new_name}\nNotes: {new_notes}"
            confirm_info_screen.ids.confirmed_button.on_release = lambda: self.complete_garden_update(new_name, new_notes)
            self.manager.current = "confirm_new_info_screen"
