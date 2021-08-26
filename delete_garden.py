from kivy.uix.screenmanager import Screen
from garden_api_client import GardenAPIClient
from kivy.app import App


class DeleteGardenScreen(Screen):

    def delete_garden_with_plants(self):
        garden_id = App.get_running_app().current_garden_info[0]
        all_plants = App.get_running_app().loop.run_until_complete(GardenAPIClient.plant_search())
        # identify plants in the current garden
        # delete plants
        # delete gardens

    def delete_garden_without_plants(self):
        pass  # identify plants in current garden
        # create new garden called "no garden"
        # change all plant location to "no garden"
        # delete the garden

    def garden_deleted(self):
        response = App.get_running_app().loop.run_until_complete(GardenAPIClient.delete_garden(self.this_garden_id))
        if response:
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