from pymongo import MongoClient
from student.models import Student
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

firebaseConfig = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "databaseURL": os.getenv('FIREBASE_DATABASE_URL'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID'),
    "measurementId": os.getenv('FIREBASE_MEASUREMENT_ID')
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# MongoDB connection
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongodb_uri)
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
        return True
    except Exception as e:
        print(f"MongoDB insertion failed: {str(e)}")
        return None

def getStudent(id):
    try:
        return conn.find_one({"localId" : id})
    except:
        return None