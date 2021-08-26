from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from garden_api_client import GardenAPIClient


class EditPlantScreen(Screen):

    def populate_input_fields(self):
        current_plant = App.get_running_app().current_plant_info
        self.ids.name_edit.text = current_plant[1]
        self.ids.common_name_edit.text = current_plant[2]
        self.ids.category_edit.text = current_plant[3]
        self.ids.location_edit.text = current_plant[4]
        self.ids.year_edit.text = str(current_plant[5])
        self.ids.notes_edit.text = current_plant[6]

    def clear_text_inputs(self):
        self.ids.name_edit.text = ""
        self.ids.common_name_edit.text = ""
        self.ids.category_edit.text = ""
        self.ids.location_edit.text = ""
        self.ids.year_edit.text = ""
        self.ids.notes_edit.text = ""

    def review_updated_plant_info(self):
        layout = GridLayout(cols=1, padding=10)

        new_name = self.ids.name_edit.text
        new_common_name = self.ids.common_name_edit.text
        new_category = self.ids.category_edit.text
        new_location = self.ids.location_edit.text
        new_year = self.ids.year_edit.text
        new_notes = self.ids.notes_edit.text

        if new_name == "" and new_common_name == "" and new_category == "" and new_year == "" and new_notes == "":
            error_message = Label(text="You must enter at least one value.", font_size="20sp")
            edit_info = Button(text="Back", size_hint=(0.1, 0.1))
            layout.add_widget(error_message)
            layout.add_widget(edit_info)
            empty_fields_popup = Popup(title="All Fields Empty", content=layout)
            empty_fields_popup.open()
            edit_info.bind(on_release=empty_fields_popup.dismiss)
        else:
            confirm_info_screen = self.manager.get_screen("confirm_new_info_screen")
            confirm_info_screen.ids.new_info_label.text = f"Name: {new_name}\nCommon Name: {new_common_name}\nCategory: {new_category}\nLocation: {new_location}\nYear Planted: {new_year}\nNotes: {new_notes}"
            confirm_info_screen.ids.confirmed_button.on_release = lambda: self.info_confirmed(new_name, new_common_name, new_category, new_location, new_year, new_notes)
            confirm_info_screen.ids.not_confirmed_button.on_release = self.return_to_edit_screen
            self.manager.current = "confirm_new_info_screen"

    def return_to_edit_screen(self):
        self.manager.current = "edit_plant_screen"

    def info_confirmed(self, name, common_name, category, location, year, notes):
        plant_id = App.get_running_app().current_plant_info[0]
        results = App.get_running_app().loop.run_until_complete(GardenAPIClient.update_plant(plant_id, name, common_name, category, location, year, notes))
        if results:
            updated_results = App.get_running_app().loop.run_until_complete(GardenAPIClient.plant_search(plant_id, name="", common_name="", category="", location="", year="", notes=""))
            for result in updated_results:
                App.get_running_app().current_plant_info = result
            self.clear_text_inputs()
            confirm_screen = self.manager.get_screen("confirmation_screen")
            confirm_screen.ids.success_message.text = "Your update is successful!"
            confirm_screen.ids.back_button.text = "Back"
            confirm_screen.ids.back_button.on_release = lambda: self.go_back()
            self.manager.current = "confirmation_screen"
        else:
            print("Plant did not update.")

    def go_back(self):
        self.manager.current = "full_plant_info_screen"
