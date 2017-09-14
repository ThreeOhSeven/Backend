from flask import Blueprint, session, jsonify, request, render_template, session
import requests
import json

authRoutes = Blueprint('authBp', __name__)

@authRoutes.route("/auth/login", methods = ["POST"])
def checkLogin():
	return False
