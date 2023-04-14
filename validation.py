from marshmallow import Schema,fields,ValidationError,validate

class StudentClass(Schema):
    name = fields.Str(required=True,validate= validate.Length(min=4))
    roll = fields.Int(required=True)
    stranded = fields.Int(required=True)

def validation_method(val):
    try:
        student = StudentClass()
        result = student.loads(val)
        return result
    
    except ValidationError as err:
        return(err.messages)
        
