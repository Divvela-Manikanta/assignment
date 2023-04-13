from pymongo import MongoClient
from flask import Flask,jsonify,request
import json

app = Flask(__name__)
client  = MongoClient('localhost',27017)
db = client.students
collection = db.studentsinfo

@app.route('/')
def into():
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
        val = (val.decode('utf-8'))
        val = json.loads(val)
        dict_insert = { "Name":val['Name'],
                        "Roll":val['Roll'],
                        "class":val['class']
                        }
        dd = collection.insert_one(dict_insert)
        if dd.acknowledged:
            return jsonify("Data is inserted successfully")
        else:
            return jsonify("Data is not inserted successfully")
    
    except Exception as ex:
        return jsonify('The format of data that you are inserted mightbe wrong')

@app.route('/find/<data>') # to find the sngle student data 
def find(data):
    val = collection.find_one({'Roll':data})
    if val != None:
        del val['_id']
        return jsonify(val)
    else:
        return jsonify(f"The student with roll number {data} is not found in data base")

@app.route('/delete',methods =['POST']) # to delete the entire student data 
def delete():
    try:
        val = (request.get_data())
        val = (val.decode('utf-8'))
        val = json.loads(val)
        val = collection.find_one({'Roll':val['Roll']})
        if val != None:
            collection.delete_one({'Roll':val['Roll']})
            return jsonify(f"The student info with roll number {val['Roll']} is deleted from the data base.")
        else:
            return jsonify(f"Unable to datele the student info with roll number {val['Roll']}.The student might be not available")
    except Exception as ex:
        return jsonify("the entred roll number has to be in string format and data has to be gven in the json 'Roll':...")


if __name__ =='__main__':
    app.run(debug=True)