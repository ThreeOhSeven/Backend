import unittest
import requests
import json
import app
from app.models import User
from app import db

Noah = {"authToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MDg5ODEyMDYsInVzZXIiOiJub2FoaWduYWNpb3NtaXRoQGdtYWlsLmNvbSJ9.o3ePPe8nG-THT51CJ5LFnKhKS76pdqBO8vPSsXlCdSs",
        "id": "16"}
Kyle = {"authToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoia3lsZS5vaGFuaWFuQGdtYWlsLmNvbSIsImV4cCI6MTUwNzI4NzUyN30.tU2hqibehcpdwhpjdG-8swj-uH_PYoOb2Ohd_Bpys_c",
        "id": "20"}
Peter = {"authToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoicGV0ZXJuam9uZXM5NUBnbWFpbC5jb20iLCJleHAiOjE1MDg5MTMzNDh9.sYtvAxjemJMx945gEjRminXuWOU2ayJS1WfMuyKoNqU",
         "id": "21"}

class UserBp_Tests(unittest.TestCase):
    def setUp(self):
        client = app.create_app("development")
        app.config.from_pyfile('config.py')
        client.testing = True
        self.app = client.test_client()

if __name__ == '__main__':
    unittest.main()
