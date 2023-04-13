from pymongo import MongoClient
from flask import Flask,jsonify,request


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
    return list1
    
@app.route("/view") # to view the entire student data 
def student_view():
    x = collection.find()
    document = []
    for val  in x:
        del val['_id']
        document.append(val)
    if len(document) !=0:
        return jsonify(document)
    else:
        return 'Their is no data to view'


@app.route('/insert',methods =['POST']) # to insert the  student data 
def insert():
    try:
        val = (request.get_data())
        val = val.decode('utf-8')
        val = val.split(',')
        dict_insert = { "Name":val[0],
                        "Roll":val[1],
                        "class":val[2]
                        }
        dd = collection.insert_one(dict_insert)
        if dd.acknowledged:
            return "Data is inserted successfully"
        else:
            return "Data is not inserted successfully"
    
    except Exception as ex:
        return 'The format of data that you are inserted mightbe wrong'

@app.route('/find',methods =['GET']) # to find the sngle student data 
def find():
    data = (request.get_data())
    data = data.decode('utf-8')
    val = collection.find_one({'Roll':data})
    if val != None:
        del val['_id']
        return jsonify(val)
    else:
        return f"The student with roll number {data} is not found in data base"

@app.route('/delete') # to delete the entire student data 
def delete():
    roll = (request.get_data())
    roll = roll.decode('utf-8')
    val = collection.find_one({'Roll':roll})
    if val != None:
        collection.delete_one({'Roll':roll})
        return f"The student info with roll number {roll} is deleted from the data base."
    else:
        return f"Unable to datele the student info with roll number {roll}.The student might be not available"


if __name__ =='__main__':
    app.run(debug=True)