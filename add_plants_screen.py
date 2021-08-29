from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from garden_api_client import GardenAPIClient


class AddPlantsScreen(Screen):

    def add_plant_confirmation(self):

        name = self.ids.plant_name.text.lower()
        common_name = self.ids.plant_common_name.text.lower()
        category = self.ids.plant_category.text.lower()
        location = self.ids.plant_location.text.lower()
        year = self.ids.year_planted.text
        notes = self.ids.notes.text.lower()

        try:
            int(year)
        except ValueError:
            self.error_message("The year must be in the yyyy format.\nExample: 2004")

        if name == "" and common_name == "" and category == "" and location == "" and year == "" and notes == "":
            self.error_message("You must enter at least one value.")
        elif name == "":
            self.error_message("The plant must have a name.")
        elif len(year) != 4:
            self.error_message("The year must be in the yyyy format.\nExample: 2004")
        else:
            self.manager.current = "confirm_new_info_screen"
            confirm_info_screen = self.manager.get_screen("confirm_new_info_screen")
            confirm_info_screen.ids.new_info_label.text = f"Name: {name}\nCommon Name: {common_name}\nCategory: {category}\nLocation: {location}\nYear Planted: {year}\nNotes: {notes} "
            confirm_info_screen.ids.confirmed_button.on_press = lambda: self.add_confirmed_information(name, common_name, category, location, year, notes)
            confirm_info_screen.ids.not_confirmed_button.on_press = self.back_to_add_plant_screen

    def error_message(self, message):
        layout = GridLayout(cols=1, padding=10)
        error_message = Label(text=message, font_size="20sp")
        edit_info = Button(text="Back", size_hint=(0.1, 0.1))
        layout.add_widget(error_message)
        layout.add_widget(edit_info)
        empty_fields_popup = Popup(title="There Is A Problem.", content=layout)
        empty_fields_popup.open()
        edit_info.bind(on_press=empty_fields_popup.dismiss)

    def back_to_add_plant_screen(self):
        self.manager.current = "add_plant_screen"

    def add_confirmed_information(self, name, common_name, category, location, year, notes):
        if location == "":
            location = "no garden"
            id_garden = 1
        else:
            for garden in App.get_running_app().all_gardens:
                if garden[1] == location:
                    id_garden = garden[0]
        response = App.get_running_app().loop.run_until_complete(GardenAPIClient.add_plant(name, common_name, category, location, year, notes, id_garden))
        if response:
            screen = self.manager.get_screen("confirmation_screen")
            screen.ids.success_message.text = "Your plant is added successfully!"
            screen.ids.back_button.text = "Add Another Plant"
            screen.ids.back_button.on_release = self.to_add_plant_screen
            self.manager.current = "confirmation_screen"
            self.clear_text_inputs()
        else:
            print("Did not add plant.")

    def to_add_plant_screen(self):
        self.manager.current = "add_plant_screen"

    def clear_text_inputs(self):
        self.ids.plant_name.text = ""
        self.ids.plant_common_name.text = ""
        self.ids.plant_category.text = ""
        self.ids.plant_location.text = "Choose a Garden"
        self.ids.year_planted.text = ""
        self.ids.notes.text = ""

