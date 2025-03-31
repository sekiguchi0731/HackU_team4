import json

def load_data():
    with open('restaurants.json', 'r', encoding='utf-8') as f:
        return json.load(f)
d={
      "id": 6,
      "name": "居酒屋むらさき",
      "genre": "居酒屋",
      "area": "新宿",
      "seats_available": 5,
      "phone": "03-1111-3333",
      "description": "和風個室でゆったりくつろげる居酒屋です。"
    },
with open('restaurants.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2)