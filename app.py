from mongodb_connection import mongo
from validation import validation_method
from flask import Flask,jsonify,request

import json

app = Flask(__name__)

 
@app.get('/')
def into():
    with app.app_context():
        list1 = '''To view data you to go for /view,
                To insert data you to go for /insert (post method),
                To find data you to go for /find'
                To delete data you to go for /delete'''
        return jsonify(list1)
    
@app.route("/view") # to view the entire student data 
def student_view():
    document = mongo.view()
    if len(document) !=0:
        return jsonify(document)
    else:
        return jsonify({"Message": "Their is no data to view.",
                        "Status":"200",
                         "Success": True})


@app.route('/insert',methods =['POST']) # to insert the  student data 
def insert():
    val = (request.get_data())
    out = validation_method(val)
    msg = mongo(out)
    return jsonify(msg.insert())
        

@app.route('/find/<int:data>') # to find the sngle student data 
def find(data):
    msg = mongo(data=data)
    return jsonify(msg.find())

@app.route('/delete',methods =['POST']) # to delete the entire student data 
def delete():
        val = (request.get_data())
        val = (val.decode('utf-8'))
        val = json.loads(val)
        msg = mongo(val=val)
        return jsonify(msg.delete())
    
if __name__ =='__main__':
    app.run(debug=True, port=5555)



