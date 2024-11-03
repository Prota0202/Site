from bson import ObjectId
from .mongodb import get_db
import random
import string


class MongoModel:
    collection_name = 'TestProject'  

    @classmethod
    def get_collection(cls):
        db = get_db()
        return db[cls.collection_name]

    @classmethod
    def insert(cls, data):
        collection = cls.get_collection()
        return collection.insert_one(data).inserted_id

    @classmethod
    def insert_many(cls, data_list):
        collection = cls.get_collection()
        return collection.insert_many(data_list).inserted_ids

    @classmethod
    def find(cls, query={}):
        collection = cls.get_collection()
        documents = collection.find(query)
        result = []
        for doc in documents:
            doc['_id'] = str(doc['_id']) 
            result.append(doc)
        return result

    @classmethod
    def update(cls, query, data):
        collection = cls.get_collection()
        return collection.update_one(query, {'$set': data})

    @classmethod
    def delete(cls, query):
        collection = cls.get_collection()
        return collection.delete_one(query)


class User(MongoModel):
    collection_name = 'users'

    @classmethod
    def create_user(cls, username, password,isAdmin, email):
        data = {
            "email": email, 
            "username": username,
            "password": password,
            "isAdmin": isAdmin,
        }
        return cls.insert(data)

    @classmethod
    def create_multiple_users(cls, count=1000):
        users = []
        for i in range(1, count + 1):
            email= f"user{i}@test.be"
            username = f"user{i}"
            password = f"password{i}"
            isAdmin = False
            users.append({"email": email,"username": username, "password": password, "isAdmin": isAdmin})

        collection = cls.get_collection()
        result = collection.insert_many(users)
        return result.inserted_ids

    @classmethod
    def get_user(cls, user_id):
        query = {"_id": ObjectId(user_id)}
        users = cls.find(query)
        return users[0] if users else None

    @classmethod
    def get_users(cls):
        users = cls.find()
        return users if users else None

    @classmethod
    def update_user(cls, user_id, new_data):
        query = {"_id": ObjectId(user_id)}
        return cls.update(query, new_data)
    
    @classmethod
    def update_pswd(cls, user_email, new_pswd):
        user = cls.get_user_by_email(user_email)
        if user:  
            user_id = user["_id"]
            query = {"_id": ObjectId(user_id)} 
            new_data = {"password": new_pswd}
            cls.update(query, new_data)  
        return None 

    @classmethod
    def delete_user(cls, user_id):
        query = {"_id": ObjectId(user_id)}
        return cls.delete(query)
    

    @classmethod
    def delete_all_users(cls):
        collection = cls.get_collection()
        result = collection.delete_many({})
        return result.deleted_count
    
    @classmethod
    def get_id(cls, username):
        query = {"username": username}  # Requête pour trouver l'utilisateur par nom d'utilisateur
        user = cls.find(query)  # Rechercher l'utilisateur dans la collection
        return user[0]["_id"] if user else None  # Retourne l'_id ou None si l'utilisateur n'existe pas
    

    @classmethod
    def get_user_by_email(cls, email):
        email = email.strip()
        query = {"email": email}
        users = cls.find(query)
        print(f"Query: {query}, Users Found: {users}")
        return users[0] if users else None


class Item(MongoModel):
    collection_name = 'items'

    @classmethod
    def create_item(cls, name, price, promotion=False):
        data = {
            "name": name,
            "price": price,
            "promotion": promotion
        }
        return cls.insert(data)

    @classmethod
    def create_multiple_items(cls, count=100):
        items = []
        for i in range(1, count + 1):
            name = f"item{i}"
            price = i * 10  # Example price calculation
            promotion = (i % 2 == 0)  # Alternate promotion for every other item
            items.append({"name": name, "price": price, "promotion": promotion})

        return cls.insert_many(items)

    @classmethod
    def get_item(cls, item_id):
        query = {"_id": ObjectId(item_id)}
        items = cls.find(query)
        return items[0] if items else None

    @classmethod
    def get_items(cls):
        return cls.find()

    @classmethod
    def update_item(cls, item_id, new_data):
        query = {"_id": ObjectId(item_id)}
        return cls.update(query, new_data)

    @classmethod
    def delete_item(cls, item_id):
        query = {"_id": ObjectId(item_id)}
        return cls.delete(query)
    

    @classmethod
    def get_id(cls, name):
        query = {"name": name}  # Requête pour trouver l'utilisateur par nom d'utilisateur
        user = cls.find(query)  # Rechercher l'utilisateur dans la collection
        return user[0]["_id"] if user else None  # Retourne l'_id ou None si l'utilisateur n'existe pas


class Order(MongoModel):
    collection_name = 'orders'

    @classmethod
    def create_order(cls, orderName, username, itemsids, itemNames):
        data = {
            "orderName": orderName,
            "username": username,
            "itemsids": itemsids,
            "itemNames": itemNames
        }
        return cls.insert(data)

    @classmethod
    def create_multiple_orders(cls, count=100):
        items = []
        for i in range(1, count + 1):
            orderName = f"order{i}"
            username = f"admin"
            itemsids = " "
            itemNames = " " 
            items.append({"orderName": orderName, "username": username, "itemsids": itemsids, "itemNames": itemNames})

        return cls.insert_many(items)

    @classmethod
    def get_order(cls, order_id):
        query = {"_id": ObjectId(order_id)}
        orders = cls.find(query)
        return orders[0] if orders else None

    @classmethod
    def get_orders(cls):
        return cls.find()

    @classmethod
    def update_order(cls, order_id, new_data):
        query = {"_id": ObjectId(order_id)}
        return cls.update(query, new_data)

    @classmethod
    def delete_order(cls, order_id):
        query = {"_id": ObjectId(order_id)}
        return cls.delete(query)


    @classmethod
    def get_id(cls, name):
        query = {"name": name}
        user = cls.find(query)
        return user[0]["_id"] if user else None
