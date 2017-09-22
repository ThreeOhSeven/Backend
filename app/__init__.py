from flask import Flask, jsonify, request, session, abort, render_template
from flask_cors import CORS
from .authBp import authRoutes

app = Flask(__name__)
app.secret_key = "EeL8b9UvQgrianpI3vDp2Zy3c13NmcGzGb0tb2w2"
CORS(app)

app.register_blueprint(authRoutes)
