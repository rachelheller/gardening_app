from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from garden_api_client import GardenAPIClient


class FullPlantInfoScreen(Screen):

    def populate_plant_info(self):
        current_plant = App.get_running_app().current_plant_info
        garden_name = App.get_running_app().garden_name(current_plant[7])
        self.ids.full_info_name.text = current_plant[1].title()
        self.ids.full_info_common_name.text = f"[i]Common Name:[/i]  {current_plant[2].title()}"
        self.ids.full_info_category.text = f"[i]Category:[/i]  {current_plant[3].title()}"
        self.ids.full_info_location.text = f"[i]Garden:[/i]  {garden_name.title()}"
        self.ids.full_info_year.text = f"[i]Year Planted:[/i]  {current_plant[5]}"
        self.ids.full_info_notes.text = f"[i]Notes:[/i]  {current_plant[6]}"

    def delete_plant_popup(self):
        current_plant = App.get_running_app().current_plant_info
        layout = GridLayout(cols=1, padding=10, spacing=(0, 5))
        deletion_message = Label(text=f"Are you sure you want to delete:\n{current_plant[1]}?\nThis action cannot be undone.", font_size="20sp")
        delete_button = Button(text="Delete", size_hint=(0.2, 0.2))
        cancel_button = Button(text="Cancel", size_hint=(0.2, 0.2))
        layout.add_widget(deletion_message)
        layout.add_widget(cancel_button)
        layout.add_widget(delete_button)
        delete_popup = Popup(title="Delete Plant Confirmation", content=layout)
        delete_popup.open()
        delete_button.bind(on_release=lambda x: self.complete_deletion(delete_popup))
        cancel_button.bind(on_release=delete_popup.dismiss)

    def complete_deletion(self, popup_name):
        plant_id = App.get_running_app().current_plant_info[0]
        response = App.get_running_app().loop.run_until_complete(GardenAPIClient.delete_plant(plant_id))
        if response:
            screen = self.manager.get_screen("confirmation_screen")
            screen.ids.success_message.text = "Your plant is deleted successfully!"
            screen.ids.back_button.text = "Back"
            screen.ids.back_button.on_release = lambda: self.back()
            self.manager.current = "confirmation_screen"
            popup_name.dismiss()
        else:
            print("Plant not deleted.")

    def back(self):
        previous_screen = App.get_running_app().previous_screen
        if previous_screen == "show_garden_screen":
            self.manager.current = previous_screen
        else:
            self.manager.get_screen("search_plants_screen").get_results()
