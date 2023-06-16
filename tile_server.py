import sqlite3
import flask
import io 

app = flask.Flask(__name__)

@app.route('/tiles/<int:z>/<int:x>/<int:y>.png')
def serve_tile(z, x, y):
    conn = sqlite3.connect('./world.mbtiles')
    c = conn.cursor()

    c.execute('SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?',
              (z, x, y))

    result = c.fetchone()
    if result:
        return flask.send_file(io.BytesIO(result[0]), mimetype='image/png')
    else:
        flask.abort(404)

    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
