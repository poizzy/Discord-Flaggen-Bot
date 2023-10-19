import json
import random

file = open("countries.json", encoding="utf8")
data = json.load(file)



class country_gen:
    def __init__(self):
        print("Hallo")
        self.generate()

    def generate(self):
        countryid = random.randint(1, 250)
        for i in data:
            if i["id"] == f"{countryid}":
                self.country = i["code2l"]
                self.country_name = i["name"]
                print(self.country, self.country_name)