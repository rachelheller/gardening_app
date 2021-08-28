from kivy.uix.screenmanager import Screen
from kivy.app import App
from garden_api_client import GardenAPIClient
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

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

    def delete_garden_check(self):
        if self.this_garden_name == "no garden":
            layout = GridLayout(cols=1, padding=10)
            message = Label(text='"no garden" cannot be deleted.\nWould you like to hide it\nfrom the Home screen?')
            cancel_button = Button(text="Cancel", size_hint=(0.1, 0.1))
            no_garden_hidden = Button(text="Hide 'No Garden'", size_hint=(0.1, 0.1))
            layout.add_widget(message)
            layout.add_widget(cancel_button)
            layout.add_widget(no_garden_hidden)
            no_garden_popup = Popup(title="Deleting No Garden", content=layout)
            no_garden_popup.open()
            cancel_button.bind(on_release=no_garden_popup.dismiss)
            no_garden_hidden.bind(on_release=lambda x: self.hide_no_garden(no_garden_popup))
        else:
            self.manager.current = "delete_garden_screen"

    def hide_no_garden(self, popup):
        App.get_running_app().loop.run_until_complete(GardenAPIClient.update_garden(garden_id=1, name="no garden", notes="hidden"))
        popup.dismiss()