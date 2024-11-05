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
        query = {"username": username}  
        user = cls.find(query) 
        return user[0]["_id"] if user else None  
    

    @classmethod
    def get_user_by_email(cls, email):
        email = email.strip()
        query = {"email": email}
        users = cls.find(query)
        print(f"Query: {query}, Users Found: {users}")
        return users[0] if users else None


class Item(MongoModel):
    collection_name = 'items'
    

    @property
    def item_id(self):
        return self._id
    

    @classmethod
    def create_item(cls, name, price, promotion=False):
        data = {
            "name": name,
            "price": price,
            "promotion": promotion
        }
        return cls.insert(data)

    @classmethod
    def create_multiple_items(cls, count=100000):
        items = []
        for i in range(1, count + 1):
            name = f"item{i}"
            price = random.randint(15, 550)
            promotion = (i % 2 == 0) 
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
    def get_item_by_name(cls, name):
        name = name.strip()
        query = {"name": name}
        items = cls.find(query)
        print(f"Query: {query}, items Found: {items}")
        return items[0] if items else None

    @classmethod
    def update_item(cls, item_id, new_data):
        query = {"_id": ObjectId(item_id)}
        return cls.update(query, new_data)
    
    @classmethod
    def update_item_promo(cls, item_name, new_data):
        print(new_data)
        if(new_data == "False"):
            new_data = True
        else:
            new_data = False


        print(new_data)
        item = cls.get_item_by_name(item_name)
        if item:  
            item_id = item["_id"]
            query = {"_id": ObjectId(item_id)} 
            new_data = {"promotion": new_data}
            cls.update(query, new_data) 
        return None 

    @classmethod
    def delete_item(cls, item_id):
        query = {"_id": ObjectId(item_id)}
        return cls.delete(query)
    
    @classmethod
    def delete_all_item(cls):
        collection = cls.get_collection()
        result = collection.delete_many({})
        return result.deleted_count
    
    
    @classmethod
    def get_id(cls, name):
        query = {"name": name}  
        item = cls.find(query)  
        return item[0]["_id"] if item else None 


class Order(MongoModel):
    collection_name = 'orders'

    @classmethod
    def create_order(cls, orderDate, username, itemsids, price):
        data = {
            "orderDate": orderDate,
            "username": username,
            "itemsids": itemsids,
            "price": price
        }
        return cls.insert(data)

    @classmethod
    def create_multiple_orders(cls, count=100):
        items = []
        for i in range(1, count + 1):
            orderDate = f"order{i}"
            username = f"admin"
            itemsids = " "
            price = " " 
            items.append({"orderName": orderDate, "username": username, "itemsids": itemsids, "price": price})

        return cls.insert_many(items)

    @classmethod
    def get_order(cls, order_id):
        query = {"_id": ObjectId(order_id)}
        orders = cls.find(query)
        return orders[0] if orders else None
    

    @classmethod
    def get_order(cls, username):
        query = {"username": username} 
        orders = cls.find(query)
        return orders if orders else None

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
    
    @classmethod
    def delete_all_orders(cls):
        collection = cls.get_collection()
        result = collection.delete_many({})
        return result.deleted_count
