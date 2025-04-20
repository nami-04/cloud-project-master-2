import pika
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv('RABBITMQ_URL')

def uploadQueueClub(studentId):
    print(f"Club queue message would be sent for student: {studentId.decode('utf-8')}")

def uploadQueueEvent(studentId):
    print(f"Event queue message would be sent for student: {studentId.decode('utf-8')}")