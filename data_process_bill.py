import pymongo

def hot_join(hot):
    b = '\n'.join(hot['文章1'])
    c = '\n'.join(hot['文章2'])
    d = '\n'.join(hot['文章3'])
    e = '\n'.join(hot['文章4'])
    f = '\n'.join(hot['文章5'])
    art_join = b + '\n' + '\n' + c + '\n' + '\n' + d + '\n' + '\n' + e + '\n' + '\n' + f
    return art_join
def mongo_bill(database,collection):
    client = pymongo.MongoClient(
        "mongodb+srv://billsyu:freemongodb1@billsyu-database.mooky.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client[database]
    col = db[collection]
    return col.find()