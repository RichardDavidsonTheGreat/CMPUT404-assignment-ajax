#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Davidson, Richard 2021
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request, redirect
import json
app = Flask(__name__)
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    '''Return something coherent here.. perhaps redirect to /static/index.html '''
    #https://www.w3schools.com/python/python_try_except.asp
    try:
        #https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
        return redirect("/static/index.html", code=302) #redirect to /static/index.html
    except:
        #https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask
        #https://stackoverflow.com/questions/12435297/how-do-i-jsonify-a-list-in-flask
        return json.dumps("Error Redirecting"), 500 #500 not 400 because a redirection error would be on the server side


@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    '''update the entities via this interface'''
    #https://www.w3schools.com/python/python_try_except.asp
    try:
        data = flask_post_json() #get the body using the given flask method
        myWorld.set(entity,data) #use the given set function to add an entity to our world
        #https://stackoverflow.com/questions/12435297/how-do-i-jsonify-a-list-in-flask
        data = json.dumps(data) #get the JSON of the data from the request
        #https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask
        return data, 200 #return the data of the request in JSON format with status code 200
    except:
        #https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask
        #https://stackoverflow.com/questions/12435297/how-do-i-jsonify-a-list-in-flask
        return json.dumps("Error Adding entity to world"), 404

@app.route("/world", methods=['POST','GET'])    
def world():
    '''you should probably return the world here'''
    #https://www.w3schools.com/python/python_try_except.asp
    try:
        #https://stackoverflow.com/questions/12435297/how-do-i-jsonify-a-list-in-flask
        requestedWorld = json.dumps(myWorld.world()) #Get what the world variable contains in JSON format
        #https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask
        return requestedWorld, 200 #return the world with status code 200
    except:
        #https://stackoverflow.com/questions/12435297/how-do-i-jsonify-a-list-in-flask
        #https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask
        return json.dumps("Error retreiving world"), 500 #500 not 400 not being able to return the world would be a server side error

@app.route("/entity/<entity>")
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    #https://www.w3schools.com/python/python_try_except.asp
    try:
        #https://stackoverflow.com/questions/12435297/how-do-i-jsonify-a-list-in-flask
        requestedEntity = json.dumps(myWorld.get(entity)) #use the built in get method to get the specific entity and transform it to JSON
        #https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask
        return requestedEntity, 200 #return the entity as JSON with status code 200
    except:
        #https://stackoverflow.com/questions/12435297/how-do-i-jsonify-a-list-in-flask
        #https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask
        return json.dumps("Error retreiving entity"), 404


@app.route("/clear", methods=['POST','GET'])
def clear():
    '''Clear the world out!'''
    #https://www.w3schools.com/python/python_try_except.asp
    try:
        myWorld.clear() #use the provided method to clear the world
        #https://stackoverflow.com/questions/12435297/how-do-i-jsonify-a-list-in-flask
        #https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask
        return json.dumps("World cleared successfully"), 200
    except:
        #https://stackoverflow.com/questions/12435297/how-do-i-jsonify-a-list-in-flask
        #https://stackoverflow.com/questions/7824101/return-http-status-code-201-in-flask
        return json.dumps("World was not cleared successfully"),  500 #500 not 400 not being able to clear the world would be a server side error

if __name__ == "__main__":
    app.run()