from flask import Flask, render_template

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('WaveGliDA.config')


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


from WaveGliDA.views import views
app.register_blueprint(views)
