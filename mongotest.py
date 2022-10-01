from pymongo import MongoClient

MONGO_URI = 'mongodb+srv://pollo23:pollo23@cluster0.2odf0.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(MONGO_URI)

db = client['teststore']
collection = db['products']

collection.insert_one({"name": "keyboard", "price": 300})
