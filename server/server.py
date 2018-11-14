from flask import Flask, render_template, g
import sqlite3

# set templates folder here
app = Flask(__name__, template_folder='templates')

DB = './config.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv	# ?

@app.teardown_appcontext
def close_connection(e):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/config")
def config():
    config = query_db("SELECT * FROM configs WHERE id = ?", [1], one=True)
    if config is None:
        msg = "Config not found"
        raise msg	# ??
    else:
        msg =  "<p>Config: name: %s, config: %s</p>\n" % (config["name"], config["config"])

    config_id = 1
    query = (
        "SELECT c.id AS config_id, c.name AS config_name," 
        " l.id AS light_id, l.name AS light_name, l.url AS light_url"
        " FROM configs c, lights l"
        " WHERE c.id = ?"   # cart prod??
    )
    lights = query_db(query, [config_id])
    msg += '<table><tr><th>id</th><th>name</th><th>url</th><tr>'
    for light in lights:
        msg += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (light['light_id'], light['light_name'], light['light_url'])
    msg += '</table>\n'

    html = "<html><head><title>Route: &#47;config</title></head><body>%s</body></html>" % msg
    return html

@app.route("/status")
def status():
    return render_template('status.html')

if __name__ == '__main__':
    app.run(debug=True)

# cruft

# msg += "Python version: " + sys.version	# Python version: 3.6.5 [...]

# from urllib import request
# import sys

    # reference query fields with names
    # def make_dicts(cursor, row):
    #     return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))
    # db.row_factory = make_dicts	# allows e.g. table_name["field_name"]
    # or:
    # db.row_factory = sqlite3.Row	# also allows table_name["field_name"]
        # uses Row objects rather than dicts to return the results of queries. These are `namedtuple`s, 
        # so we can access them either by index or by key

    # cur = get_db().cursor()