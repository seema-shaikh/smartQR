from marshmallow import Schema, fields, validate

class UserRegisterationSchema(Schema):
    full_name = fields.Str(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=0))
    email = fields.Email(required=True)
    gender = fields.Str(required=True)
    state = fields.Str(required=True)
    phone_number = fields.Int(validate=validate.Range(min=10**9, max=10**10 - 1, error='Phone number must be a 10-digit integer'))
    profile_pic = fields.Str(required=True)
    password = fields.Str(validate=validate.Length(min=8))   

class UserLoginSchema(Schema):

    email = fields.Email(required=True)
    password = fields.Str(validate=validate.Length(min=8))
    
class UpdateProfileSchema(Schema):
    email = fields.Email()
    full_name = fields.Str()
    age = fields.Int(validate=validate.Range(min=0))
    gender = fields.Str()
    state = fields.Str()
    phone_number = fields.Str()
    profile_pic = fields.Str()
    
class DeleteAccountSchema(Schema):

    email = fields.Email(required=True)
    password = fields.Str(validate=validate.Length(min=8)) 
