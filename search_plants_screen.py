from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from garden_api_client import GardenAPIClient


class SearchPlantsScreen(Screen):

    def new_search(self):
        self.manager.current = "search_plants_screen"
        self.clear_search_fields()
        App.get_running_app().plant_search_results = []

    def clear_search_fields(self):
        self.ids.name_search.text = ""
        self.ids.common_name_search.text = ""
        self.ids.category_search.text = ""
        self.ids.location_search.text = ""
        self.ids.year_search.text = ""
        self.ids.notes_search.text = ""

    def full_results_info(self, search_result):
        App.get_running_app().current_plant_info = search_result
        self.manager.current = "full_plant_info_screen"
        plant_info_screen = self.manager.get_screen("full_plant_info_screen")
        plant_info_screen.ids.back_to_results.on_release = self.return_to_search_results

    def return_to_search_results(self):
        self.manager.current = "results_screen"

    def error_screen(self):
        layout = GridLayout(cols=1, padding=10)
        error_message = Label(text="That is not a valid search.\nPlease try again.", font_size="20sp")
        dismiss_button = Button(text="Go Back", size_hint=(0.1, 0.1))
        layout.add_widget(error_message)
        layout.add_widget(dismiss_button)
        error_popup = Popup(title="No Results", content=layout)
        error_popup.open()
        dismiss_button.bind(on_release=error_popup.dismiss)

    def recycleview_formatted_data(self):
        results = App.get_running_app().plant_search_results
        records = []
        if not results:
            records.insert(0, {"font_size": "27sp", "text": "No Results in Database."})
            return [x for x in records]
        else:
            for plant in results:
                garden_name = App.get_running_app().garden_name(plant[7])
                record = {"font_size": "20sp", "text": f"{plant[1]}  |  {garden_name}",
                          "input_data": plant, "on_release": lambda _plant=plant: self.full_results_info(_plant)}
                records.append(record)
            return [x for x in records]

    def get_results(self):
        name_input = self.ids.name_search.text
        common_name_input = self.ids.common_name_search.text
        category_input = self.ids.category_search.text
        location_input = self.ids.location_search.text
        year_input = str(self.ids.year_search.text)
        notes_input = self.ids.notes_search.text
        plant_id = ""

        if name_input == "" and common_name_input == "" and category_input == "" and location_input == "No Garden Chosen" and year_input == "" and notes_input == "":
            return self.error_screen()
        else:
            plant_results = App.get_running_app().loop.run_until_complete(GardenAPIClient.plant_search(plant_id, name_input, common_name_input, category_input, location_input, year_input, notes_input))
            App.get_running_app().plant_search_results = plant_results
            rv = self.manager.get_screen("results_screen").ids.plant_results_rv
            rv.data = self.recycleview_formatted_data()
            self.manager.current = "results_screen"
