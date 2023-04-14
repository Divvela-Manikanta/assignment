from pymongo import MongoClient
from flask import Flask,jsonify,request
import json
from dataclasses import dataclass
from marshmallow import Schema,fields,ValidationError,validate


app = Flask(__name__)

    
client  = MongoClient('localhost',27017)
db = client.students
collection = db.studentsinfo

class StudentClass(Schema):
    name = fields.Str(required=True,validate= validate.Length(min=4))
    roll = fields.Int(required=True)
    stranded = fields.Int(required=True)

@dataclass
class DataToStore:
    deleteitem : str = None
    
@app.route('/')
def into():
    with app.app_context():
        list1 = '''To view data you to go for /view,
                To insert data you to go for /insert (post method),
                To find data you to go for /find'
                To delete data you to go for /delete'''
        return jsonify(list1)
    
@app.route("/view/") # to view the entire student data 
def student_view():
    x = collection.find()
    document = []
    for val  in x:
        del val['_id']
        document.append(val)
    if len(document) !=0:
        return jsonify(document)
    else:
        return jsonify('Their is no data to view')


@app.route('/insert',methods =['POST']) # to insert the  student data 
def insert():
   
    try:
        val = (request.get_data())
        # val = (val.decode('utf-8'))
        # val = json.loads(val)
        student = StudentClass()

        result = student.loads(val)
        
        dict_insert = { "name":result['name'],
                    "roll":result['roll'],
                    "stranded":result['stranded']
                    }
        dd = collection.insert_one(dict_insert)
        if dd.acknowledged:
            return jsonify("Data is inserted successfully")
        else:
            return jsonify("Data is not inserted successfully")

    except ValidationError as err:
        return(err.messages)
        

@app.route('/find/<int:data>') # to find the sngle student data 
def find(data):
    # projection = {"name":1,"roll":1,"class_stu":1}
    val = collection.find_one({'roll':data},{'_id':0})
    if val != None:
        return jsonify(val)
    else:
        return (f"The student with roll number {data} is not found in data base")

@app.route('/delete',methods =['POST']) # to delete the entire student data 
def delete():
    try:
        val = (request.get_data())
        val = (val.decode('utf-8'))
        val = json.loads(val)
        value  = DataToStore(val['roll'])
        val = collection.find_one({'roll':value.deleteitem})
        if val != None:
            collection.delete_one({'roll':value.deleteitem})
            return jsonify(f"The student info with roll number {value.deleteitem} is deleted from the data base.")
        else:
            return jsonify(f"Unable to datele the student info with roll number {value.deleteitem}.The student might be not available")
    except Exception as ex:
        return jsonify("the entred roll number has to be in string format and data has to be gven in the json 'roll':...")


if __name__ =='__main__':
    app.run(debug=True)
