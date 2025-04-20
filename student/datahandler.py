from pymongo import MongoClient
from student.models import Student
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import pyrebase
firebaseConfig = {
    "apiKey": "AIzaSyDUEVU5icElBw_PR6xQ5XEXsy56vOL0H3g",
    "authDomain": "cloud-project-1-27e81.firebaseapp.com",
    "databaseURL": "https://cloudproject-bcd7008-default-rtdb.firebaseio.com",
    "projectId": "cloud-project-1-27e81",
    "storageBucket": "cloud-project-1-27e81.appspot.com",
    "messagingSenderId": "850810687393",
    "appId": "1:850810687393:web:c3c448975108610c3345e0",
    "measurementId": "G-Z40ZLL0MMJ"
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

client = MongoClient("")
db = client.get_database("CloudProject")
conn = db.Student

def createStudent(studentData,password):
    try:
        guser = auth.create_user_with_email_and_password(studentData['studentEmail'], password)
        auth.send_email_verification(guser['idToken'])
    except:
        print("google failed")
        return None
    
    try:
        user = User(username=guser['localId'],email=studentData['studentEmail'] ,first_name=studentData['studentName'],is_superuser=False)
        user.set_password("deZE%KYzH5jVBbHN")
        user.save()
        my_group = Group.objects.get(name='Studentgrp')
        my_group.user_set.add(user)
    except:
        print("Local User Failed")
        return None
    
    try:
        stu = Student(studentId = guser['localId'])
        stu.save()
    except:
        print("Student Model failed")
        return None
    
    try:
        studentData['localId'] = guser['localId']
        conn.insert_one(studentData)   
    except:
        print("mongo failed")
        return None
    return True

def getStudent(id):
    try:
        return conn.find_one({"localId" : id})
    except:
        return None