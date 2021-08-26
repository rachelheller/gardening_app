from kivy.app import App
from kivy.uix.screenmanager import Screen
from garden_api_client import GardenAPIClient


class ChooseGarden(Screen):
    def garden_recycleview_list_data(self):
        garden_data = App.get_running_app().loop.run_until_complete(GardenAPIClient.get_garden_list())
        records = []
        for garden in garden_data:
            record = {"font_size": "20sp", "text": f"{garden[1]}",
                      "input_data": garden, "on_press": lambda _garden=garden: self.user_chooses_this_garden(_garden)}
            records.append(record)
        return [x for x in records]

    def user_chooses_this_garden(self, chosen_garden):
        previous_screen = App.get_running_app().choose_garden_from_list_previous_screen
        if previous_screen == "search_plants_screen":
            self.manager.get_screen("search_plants_screen").ids.location_search.text = chosen_garden[1]
        elif previous_screen == "edit_plant_screen":
            self.manager.get_screen("edit_plant_screen").ids.location_edit.text = chosen_garden[1]
        elif previous_screen == "add_plant_screen":
            self.manager.get_screen("add_plant_screen").ids.plant_location.text = chosen_garden[1]
        self.manager.current = previous_screen

    def refresh_gardens_list(self):
        self.ids.garden_list_recycleview.data = self.garden_recycleview_list_data()
        self.ids.garden_list_recycleview.refresh_from_data()
