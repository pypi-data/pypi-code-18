from flask import Flask, render_template

theApp =Flask(__name__)
theApp.config.from_object("config")

from theApp.mod1.controllers import mod1

theApp.register_blueprint(mod1) 
