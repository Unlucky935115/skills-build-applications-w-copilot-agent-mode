from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

# Sample data for users, teams, activities, leaderboard, workouts
USERS = [
    {"name": "Clark Kent", "email": "superman@dc.com", "team": "DC"},
    {"name": "Bruce Wayne", "email": "batman@dc.com", "team": "DC"},
    {"name": "Diana Prince", "email": "wonderwoman@dc.com", "team": "DC"},
    {"name": "Tony Stark", "email": "ironman@marvel.com", "team": "Marvel"},
    {"name": "Steve Rogers", "email": "captainamerica@marvel.com", "team": "Marvel"},
    {"name": "Natasha Romanoff", "email": "blackwidow@marvel.com", "team": "Marvel"},
]

TEAMS = [
    {"name": "Marvel", "members": ["Tony Stark", "Steve Rogers", "Natasha Romanoff"]},
    {"name": "DC", "members": ["Clark Kent", "Bruce Wayne", "Diana Prince"]},
]

ACTIVITIES = [
    {"user": "Clark Kent", "activity": "Flight", "duration": 60},
    {"user": "Bruce Wayne", "activity": "Martial Arts", "duration": 45},
    {"user": "Tony Stark", "activity": "Weight Lifting", "duration": 30},
]

LEADERBOARD = [
    {"team": "Marvel", "points": 300},
    {"team": "DC", "points": 250},
]

WORKOUTS = [
    {"name": "Super Strength", "description": "Heavy lifting and resistance training."},
    {"name": "Agility Training", "description": "Speed and flexibility drills."},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(host='localhost', port=27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert test data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
