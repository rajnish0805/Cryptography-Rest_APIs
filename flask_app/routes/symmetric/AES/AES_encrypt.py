from email import header
from re import M
from flask import request
from flask_restful import Resource, reqparse
import json
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from main import app

class Aes_encrypt_class(Resource):
    
    def get(self):
        key_state = False
        app.logger.info("In encryption class")
        
        try:
            #Arguments collection
            data=request.files.get("data")
            key = request.files.get("key")
            head=request.form.get("header")
            
            #Checking args
            if data == None or data=="" or data==" ":
                return {"message":"Encryption can be done only if data is provide."}, 201
            else:
                data=data.read()
                print(type(data))
                app.logger.info("Data loaded")

            if key == None or key=="" or key==" ":
                key=get_random_bytes(16)
                key_state=True
            else:
                key=key.read()
            
            cipher = AES.new(key, AES.MODE_CCM)

            if head == None or head=="" or head==" ":
                head = b"header"
            else:
                head=head

            app.logger.info("Args checked")

            cipher.update(head)
            ciphertext, tag = cipher.encrypt_and_digest(data)       ##Encryption done

            app.logger.info("Encrypted data")

            #Binding result in json
            json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
            json_v = [ b64encode(x).decode('utf-8') for x in (cipher.nonce, head, ciphertext, tag)]
            result = dict(zip(json_k, json_v))

            app.logger.info("Result generated")

            #Returning key only when if it is not passed in args
            if key_state:
                return {'message':'Encryption successfull',
                        'result':result,
                        'key_generated':str(key)},200
            else:
                return {'message':'Encryption successfull',
                        'result':result},200

        
        except Exception as e:
            print("Something went wrong ", e)
            app.logger.error(f"Error occured - {e}")
            return {"error":"Internal server error"}, 500
            


