from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
import subprocess

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=['GET', 'POST'])
# CORS(app)

@app.route('/solvePuzzle', methods=['GET', 'POST'])
@cross_origin()
def solve_puzzle():
    #Get parameters
    params = request.get_json()
    initialState = params.get('initial-state')
    if (initialState):
        print("Received:",initialState)
    else:
        print("No parameters received")
    print("type:",type(initialState))
    
    #call function
    process = subprocess.Popen(['python3', '../python/DijkstrasAlgorithm/main.py'], stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    #send response
    print(output)
    response = jsonify({'solution':"hello"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    
    return response

@app.route("/")
def hello():
    return "hello"
    

if __name__ == "__main__":
    app.run()