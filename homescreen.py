from kivy.uix.screenmanager import Screen
from kivy.app import App
from garden_api_client import GardenAPIClient


class HomePageScreen(Screen):

    def data_for_gardens_list(self):
        garden_data = App.get_running_app().all_gardens
        records = []
        for garden in garden_data:
            if garden[0] == 1 and garden[2] == "hidden":
                continue
            else:
                record = {"font_size": "20sp", "text": f"{garden[1]}",
                          "input_data": garden, "on_press": lambda _garden=garden: self.select_garden(_garden)}
                records.insert(0, record)
        return [x for x in records]

    def select_garden(self, chosen_garden):
        App.get_running_app().current_garden_info = chosen_garden
        self.manager.current = "show_garden_screen"

    def refresh_gardens_recycleview(self):
        self.ids.current_gardens.data = self.data_for_gardens_list()
        self.ids.current_gardens.refresh_from_data()
