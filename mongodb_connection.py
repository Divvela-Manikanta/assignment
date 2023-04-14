from pymongo import MongoClient
from data_class import DataToStore,Student


client  = MongoClient('localhost',27017)
db = client.students
collection = db.studentsinfo

class mongo:
    def __init__(self,result=None,data =None,val=None):
        self.result = result
        self.data = data
        self.val=val

    
    @staticmethod
    def view():
        x = collection.find({'_id':0})
        document = []
        for val  in x:
            document.append(val)
        return document
    
    def insert(self):
        dict_insert = { "name":self.result['name'],
                    "roll":self.result['roll'],
                    "stranded":self.result['stranded']
                    }
        dd = collection.insert_one(dict_insert,{'_id':None})
        if dd.acknowledged:
            return ({"Meassage":"Data is inserted successfully",
                      "Success": True,
                      "Status":200})
        else:
            return ({"Meassage":"Data is not inserted successfully",
                      "Success": False,
                      "Status":500})
    
    def find(self):
        val = collection.find_one({'roll':(self.data)},{'_id':0})
        if val != None:
              return (val)
        else:
            return ({"Mesage":f"The student with roll number {self.data} is not found in data base.",
                     "Success":True,
                     "Status":200})
        
    def delete(self):
        value  = DataToStore(self.val['roll'])
        val = collection.find_one({'roll':value.deleteitem})
        if val != None:
            collection.delete_one({'roll':value.deleteitem})
            return ({"Mesage":f"The student info with roll number {value.deleteitem} is deleted from the data base.",
                     "Success":True,
                     "Status":200})
        else:
            return ({"Mesage":f"Unable to datele the student info with roll number {value.deleteitem}.The student might be not available",
                     "Success":True,
                     "Status":200})
        

