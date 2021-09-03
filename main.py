import asyncio

from kivy.config import Config

Config.set("graphics", "resizable", True)

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from search_plants_screen import SearchPlantsScreen
from add_plants_screen import AddPlantsScreen
from add_garden_screen import AddGardenScreen
from edit_plant_screen import EditPlantScreen
from homescreen import HomePageScreen
from view_garden import ViewGarden
from full_plant_info import FullPlantInfoScreen
from edit_garden_screen import UpdateGarden
from choose_garden import ChooseGarden
from delete_garden import DeleteGardenScreen
from garden_api_client import GardenAPIClient

Builder.load_file("design.kv")

Window.clearcolor = (0, 0.6, 0.1, 1.0)


class HomeScreen(HomePageScreen):
    pass


class Search(SearchPlantsScreen):
    pass


class ChooseGardenFromList(ChooseGarden):
    pass


class FullPlantInfo(FullPlantInfoScreen):
    pass


class ResultsScreen(Screen):

    def refresh_recycleview(self):
        screen = self.manager.get_screen("search_plants_screen")
        self.ids.plant_results_rv.data = screen.recycleview_formatted_data()
        self.ids.plant_results_rv.refresh_from_data()


class AddPlant(AddPlantsScreen):
    pass


class EditPlant(EditPlantScreen):
    pass


class EditGarden(UpdateGarden):
    pass


class AddGarden(AddGardenScreen):
    pass


class DeleteGarden(DeleteGardenScreen):
    pass

class ConfirmNewInfo(Screen):
    pass


class AddImageScreen(Screen):
    pass


class DatabaseConfirmationScreen(Screen):
    pass


class ShowGarden(ViewGarden):
    pass


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.plant_search_results = []
        self.current_plant_info = []
        self.current_garden_info = []
        self.new_plant_info = []
        self.previous_screen = ""
        self.choose_garden_from_list_previous_screen = ""
        self.loop = asyncio.get_event_loop()
        self.all_gardens = []
        self.get_all_gardens()

    def record_previous_screen(self, screen_name):
        if screen_name == "full_plant_info_screen":
            self.choose_garden_from_list_previous_screen = screen_name
        else:
            self.choose_garden_from_list_previous_screen = screen_name
            self.previous_screen = screen_name

    def get_all_gardens(self):
        self.all_gardens = self.loop.run_until_complete(GardenAPIClient.get_garden_list())

    def garden_name(self, garden_id):
        for garden in self.all_gardens:
            if garden_id == garden[0]:
                return garden[1]

    def build(self):
        self.title = "My Gardens App"
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
