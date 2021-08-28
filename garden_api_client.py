import json
import aiohttp
import os

HOST_URL = os.environ.get("HOST_URL")


class GardenAPIClient:

    @staticmethod
    async def get_garden_list():
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{HOST_URL}/gardens") as response:
                if response.status == 200:
                    raw = await response.text()
                    data = [tuple(item.values()) for item in json.loads(raw)]
                    return data
                else:
                    return None

    @staticmethod
    async def create_garden(name, notes):
        dictionary = {"name": name,
                      "notes": notes}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{HOST_URL}/gardens/create", data=dictionary) as response:
                if response.status == 200:
                    return True
                else:
                    print(response.status)
                    return False

    @staticmethod
    async def add_plant(name, common_name, category, location, year, notes, garden_id):
        dictionary = {"name": name,
                      "common_name": common_name,
                      "category": category,
                      "location": location, # how do I make this connected with the foreignkey
                      "year": year,
                      "notes": notes,
                      "garden_id": garden_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{HOST_URL}/plants/create", data=dictionary) as response:
                if response.status == 200:
                    return True
                else:
                    print(response.status)
                    return False

    @staticmethod
    async def update_garden(garden_id, name, notes):
        dictionary = {"name": name,
                      "notes": notes}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{HOST_URL}/gardens/update/{garden_id}", data=dictionary) as response:
                if response.status == 200:
                    return True
                else:
                    return False

    @staticmethod
    async def search_gardens(garden_id="", garden_name=""):
        dictionary = {}
        if garden_id != "":
            dictionary["id"] = garden_id
        if garden_name != "":
            dictionary["name"] = garden_name
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{HOST_URL}/gardens/search", data=dictionary) as response:
                if response.status == 200:
                    raw = await response.text()
                    data = [tuple(item.values()) for item in json.loads(raw)]
                    return data
                else:
                    return False

    @staticmethod
    async def delete_garden(garden_id):
        dictionary = {"id": garden_id}
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{HOST_URL}/gardens/delete/{garden_id}", data=dictionary) as response:
                if response.status == 200:
                    return True
                else:
                    return False

    @staticmethod
    async def plant_search(plant_id="", name="", common_name="", category="", location="", year="", notes="", garden_id=""):
        plant_dictionary = {"plant_id": plant_id,
                            "name": name,
                            "common_name": common_name,
                            "category": category,
                            "location": location,
                            "year": year,
                            "notes": notes,
                            "garden_id": garden_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{HOST_URL}/plants/search", data=plant_dictionary) as response:
                if response.status == 200:
                    raw = await response.text()
                    data = [tuple(item) for item in json.loads(raw)]
                    return data
                else:
                    return False

    @staticmethod
    async def update_plant(plant_id, name, common_name, category, location, year, notes, garden_id):
        plant_dictionary = {"name": name,
                            "common_name": common_name,
                            "category": category,
                            "location": location,
                            "year": year,
                            "notes": notes,
                            "garden_id": garden_id}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{HOST_URL}/plants/update/{plant_id}", data=plant_dictionary) as response:
                if response.status == 200:
                    return True
                else:
                    return False

    @staticmethod
    async def delete_plant(plant_id):
        dictionary = {"id": plant_id}
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{HOST_URL}/plants/delete/{plant_id}", data=dictionary) as response:
                if response.status == 200:
                    return True
                else:
                    return False
