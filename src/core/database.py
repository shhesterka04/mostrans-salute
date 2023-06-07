from pymongo import MongoClient


class Route:
    def __init__(self, short_route_name, long_route_name, link):
        self.short_route_name = short_route_name
        self.long_route_name = long_route_name
        self.link = link

    def to_dict(self):
        return {
            "short_route_name": self.short_route_name,
            "long_route_name": self.long_route_name,
            "link": self.link,
        }


password = "WEkW2B7IjCphpBs0"
client = MongoClient(f"mongodb+srv://mostrans:{password}@cluster0.a62xwlu.mongodb.net/?retryWrites=true&w=majority")
db = client['mostrans']
routes = db['routes']
