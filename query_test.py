import pymongo

myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

for i in mycol.find({ 'keyword': { '$regex': '友通' } }):
    print(i['title'])