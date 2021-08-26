from kivy.uix.screenmanager import Screen
from kivy.app import App
from garden_api_client import GardenAPIClient

class ViewGarden(Screen):

    def __init__(self, **kwargs):
        super(ViewGarden, self).__init__(**kwargs)
        self.this_garden_name = ""
        self.this_garden_notes = ""
        self.this_garden_id = ""

    def populate_info(self):
        garden_info = App.get_running_app().current_garden_info
        self.this_garden_id = garden_info[0]
        self.this_garden_name = garden_info[1]
        self.this_garden_notes = garden_info[2]
        self.ids.current_garden_name.text = f"[u]{(garden_info[1]).title()}[/u]"
        self.ids.notes_for_this_garden.text = f"{garden_info[2]}"

        results = App.get_running_app().loop.run_until_complete(GardenAPIClient.plant_search(location=self.this_garden_name))
        if results:
            records = []
            for plant in results:
                each_plant = {"font_size": "22sp", "text": f"{plant[1]}  |  {plant[2]}",
                              "input_data": plant, "on_press": lambda _plant=plant: self.full_plant_info(_plant)}
                records.append(each_plant)
            self.ids.plants_list.data = [x for x in records]
            self.ids.plants_list.refresh_from_data()

    def full_plant_info(self, plant):
        App.get_running_app().current_plant_info = plant
        self.manager.current = "full_plant_info_screen"
        plant_info_screen = self.manager.get_screen("full_plant_info_screen")
        plant_info_screen.ids.back_to_results.on_press = self.back_to_view_garden

    def back_to_view_garden(self):
        self.manager.current = "show_garden_screen"