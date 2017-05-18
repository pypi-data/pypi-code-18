from flask import render_template


from papimem.web import webapp, db


@webapp.route("/")
def requests_collection():
    return render_template('index.html', items=db.get_all())
