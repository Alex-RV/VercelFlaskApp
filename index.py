from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

@app.route("/test", methods=["POST"])
def test():
    slider_value = request.form["slider"]
    return render_template ("index.html", slider_value=slider_value)

if __name__ == '__main__':
    app.run()