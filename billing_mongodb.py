import pymongo
client = pymongo.MongoClient(
        "mongodb+srv://billsyu:freemongodb1@billsyu-database.mooky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

def count(database, col_name, count_type):
    db = client[database]
    col = db[col_name]
    a = col.find_one({'type':'billing'})
    temp_list = list()
    for i in a[count_type]:
        temp_list.append(i)
    return temp_list

def update(database, col_name, p_count, n_count):
    db = client[database]
    col = db[col_name]
    col.drop()
    a = {'type':'billing','posi':p_count,'nega':n_count}
    col.insert_one(a)