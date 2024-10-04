from doctest import debug

from flask import request, jsonify
from flask import Flask

app = Flask(__name__)


@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    extra=request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200

@app.route("/create-user", methods=["POST"])
def create_user():
    data=request.get_json()
    

    return jsonify(data), 201


if __name__ == "__main__":
    app.run(debug=True)

# Get- Request data from a specified source
# Post- Create a resource
# Put- Update a resource
# delete- Delete a resource
