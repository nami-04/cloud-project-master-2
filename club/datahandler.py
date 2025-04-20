from pymongo import MongoClient
from club.models import Club
from admintask.models import subscription
from student.models import Student
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
import uuid
import firebase_admin
from firebase_admin import auth, credentials
import traceback
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongodb_uri)
db = client.get_database("CloudProject")
conn = db.Clubs

# Initialize Firebase Admin SDK
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL')
})

firebase_admin.initialize_app(cred)

def createClub(ClubData):
    password = str(uuid.uuid4())
    try:        
        print("Going to google")
        user = auth.create_user(
            email=ClubData['clubEmail'],
            password=password,
            email_verified=False
        )
        print("user created")
        auth.generate_email_verification_link(ClubData['clubEmail'])
    except:
        traceback.print_exc()
        print("Google Failed")
        return None
    
    try:
        ClubData['clubId'] = user.uid
        conn.insert_one(ClubData)  
        club = Club(clubId=ClubData['clubId'])
        club.save()
        my_group = Group.objects.get(name='Clubgrp')
        user = User(username = ClubData['clubId'] ,first_name=ClubData['clubName'], email = ClubData['clubEmail'],is_superuser=False)
        user.set_password("deZE%KYzH5jVBbHN")
        user.save()
        my_group.user_set.add(user)
        return password
    except Exception as e:
        print(f"Error creating club: {str(e)}")
        return None

def deleteClub(id):
    try:    
        auth.delete_user(id)
        conn.delete_one({"clubId" : id})
        evedata.deleteEventforClub(id)
        User.objects.filter(username=id).delete()
        Club.objects.filter(clubId=id).delete()
        try:
            subscription.objects.all().filter(clubId=id).delete()
        except:
            traceback.print_exc()
            print("No subscription")
    except:
        traceback.print_exc()
        return None
    return True


def getAllClub():
    try:
        return conn.find({})
    except:
        traceback.print_exc()
        return None

def getClub(id):
    try:
        return conn.find_one({"clubId" : id})
    except:
        traceback.print_exc()
        return None

def getSubscribedClubforStudent(studentId):
    clubs = []
    try:
        clubIds = subscription.objects.all().filter(studentId = studentId)
        for x in clubIds:
            clubs.append(getClub(x.clubId))
    except:
        traceback.print_exc()
        print("error in subscribed club")
    return clubs

def removeStudentSubscription(studentId , clubId):
    subscription.objects.all().filter(studentId=studentId , clubId=clubId).delete()


def addStudentSubscription(studentId , clubId):
    subs = subscription(studentId=studentId, clubId= clubId)
    subs.save()

def updateClub(id , updatedData):
    try:  
        query = {"clubId" : id}
        update = {"$set": updatedData}
        conn.update_one(query , update)
    except:
        return None
    return True