from flask import Flask, request, render_template, url_for


app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['POST', 'GET'])
def show_map():
    return render_template('points.html', have_logos=[])


if __name__ == "__main__":
    print(url_for("static", filename="js/homes.js"))
    app.run(port=5000, debug=True)
