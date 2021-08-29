from kivy.uix.screenmanager import Screen
from garden_api_client import GardenAPIClient
from kivy.app import App


class DeleteGardenScreen(Screen):

    def delete_garden_with_plants(self):
        current_garden_id = App.get_running_app().current_garden_info[0]
        all_plants = App.get_running_app().loop.run_until_complete(GardenAPIClient.plant_search(garden_id=current_garden_id))
        for plant in all_plants:
            App.get_running_app().loop.run_until_complete(GardenAPIClient.delete_plant(plant[0]))
        self.garden_deleted()

    def delete_garden_without_plants(self):
        current_garden_id = App.get_running_app().current_garden_info[0]
        all_plants = App.get_running_app().loop.run_until_complete(GardenAPIClient.plant_search(garden_id=current_garden_id))
        for plant in all_plants:
            App.get_running_app().loop.run_until_complete(GardenAPIClient.update_plant(plant_id=plant[0], name=plant[1], common_name=plant[2], category=plant[3], location="no garden", year=plant[5], notes=plant[6], garden_id=1))
        self.garden_deleted()

    def garden_deleted(self):
        current_garden_id = App.get_running_app().current_garden_info[0]
        response = App.get_running_app().loop.run_until_complete(GardenAPIClient.delete_garden(current_garden_id))
        if response:
            App.get_running_app().get_all_gardens()
            screen = self.manager.get_screen("confirmation_screen")
            screen.ids.success_message.text = "Your garden is deleted successfully!"
            screen.ids.back_button.text = "Search Plants"
            screen.ids.back_button.on_press = lambda: self.search_again()
            self.manager.current = "confirmation_screen"
        else:
            print(response)
            print("Not Deleted")

    def search_again(self):
        self.manager.current = "search_plants_screen"