from flask import Flask, request, jsonify,json, Response, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('start.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

if __name__=="__main__":
    app.run(debug = True, port = 5001)

