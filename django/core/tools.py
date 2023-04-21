import os
from django.db import connection


""" Drop test database"""
def drop_test_db():
    test_db = 'test_' + os.environ.get('POSTGRES_DB')
    cursor = connection.cursor()         
    cursor.execute(f'DROP DATABASE IF EXISTS {test_db}')
    cursor.close() 