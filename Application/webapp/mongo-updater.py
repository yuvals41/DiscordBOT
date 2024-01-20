from pymongo import MongoClient
from flask import Flask, request, jsonify
import logging, os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_HOST = os.environ.get("DB_HOST") or "localhost"
DB_USER = os.environ.get("DB_USER") or ""
DB_PASSWORD = os.environ.get("DB_PASSWORD") or ""
DIRECT_CONNECTION = os.environ.get("DIRECT_CONNECTION") or False

if DIRECT_CONNECTION == "true":
    DIRECT_CONNECTION = True
    
if not DB_PASSWORD or not DB_USER:
    auth = ""
else:
    auth = f"{DB_USER}:{DB_PASSWORD}@"


client = MongoClient(f"mongodb://{auth}{DB_HOST}",27017,directConnection=DIRECT_CONNECTION)
db = client["yuval"]

def update_repos():
    try:
        data = request.get_json()
        logging.info("Request data received")
    except Exception as e:
        logging.error(f"Missing or invalid data: {e}")
        return jsonify({"error": "Bad request"}), 400
    
    if not data["repo_names"] or not data["timestamp"]:
        logging.error("Body does not contain repo_names or timestamp")
        return jsonify({"error": "Body must contain repo_names and timestamp"}), 400
    
    doc = {
        "repo_names": data["repo_names"],
        "timestamp": data["timestamp"]
    }

    if "githubRepos" not in db.list_collection_names():
        db.create_collection("githubRepos")
        logging.info("Created githubRepos collection")

    collection = db.get_collection("githubRepos")

    logging.info("updating collection")
    post_id = collection.insert_one(doc).inserted_id

    return jsonify({"post_id": str(post_id)}), 200


@app.route("/current-git-repo")
def update_current_repos():
    return update_repos()

@app.route("/ready")
def ready():
    return jsonify({"status": "healthy"}),200


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)