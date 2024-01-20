from flask import Flask, jsonify, request, render_template
import requests
from dotenv import load_dotenv
import json
import logging
import os
from datetime import datetime

app = Flask(__name__)
load_dotenv()

GITHUB_USER = os.environ.get("GITHUB_USER") or "yuvals41"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
MONGO_UPDATER_HOST = os.getenv('MONGO_UPDATER_HOST') or "mongo-updater"
available_routes = ["/create-repo", "/ready", "/get-repos", "/check-repos-private"]

if not GITHUB_TOKEN:
    logging.error("GitHub token not set. Exiting.")
    os._exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def request_to_endpoint(url: str, headers={},data={},json={}):
    try:
        response = requests.get(url, headers=headers,data=data,json=json, timeout=20)
        response.raise_for_status()
        return response.json(),response.status_code
    except requests.RequestException as e:
        logging.error(f"Error sending request to {url}: {e}")
        return None



def get_repo_names():
    repo_names = {}
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    logging.info("Requesting GitHub repos")
    repos, _ = request_to_endpoint(f"https://api.github.com/users/{GITHUB_USER}/repos", headers)

    if repos is None:
        return jsonify({"error": "Error requesting GitHub API"}), 500


    for i, data in enumerate(repos):
        repo_num = i + 1
        # repo_names.update({f"repo-name{i}": name["name"]})
        repo_names[f"repo-name{repo_num}"] =  data["name"]

    logging.info("created repos json")
    
    mongo_updater_header = {
        "Content-Type": "application/json"
    }
    timestamp = str(datetime.now())
    response_post_id, status = request_to_endpoint(f"http://{MONGO_UPDATER_HOST}/current-git-repo",headers=mongo_updater_header,json={"repo_names": repos,"timestamp": timestamp})
    logging.info(f"mongo updater response: {response_post_id}")

    if status != 200:
        logging.error("failed to send request to db updater")
        return jsonify(f"Internal Error: {response_post_id}"), 500
    
    logging.info(f"successfuly updated in mongo,response: {response_post_id}")

    return jsonify(repo_names),200


def check_private_repos():
    non_private_repos = []

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    logging.info("Checking for private repos")
    repos, _ = request_to_endpoint(f"https://api.github.com/users/{GITHUB_USER}/repos", headers)

    if repos is None:
        return jsonify({"error": "Error requesting GitHub API"}), 500

    if all(repo["private"] for repo in repos):
    
        return jsonify({"message":"all repos are not private"}),500
    
    for repo in repos:
        if repo["private"] == False:
            non_private_repos.append(repo["name"])
        
    return jsonify({"message": f"these are the non private repos: {non_private_repos}"}), 200

def create_git_repo():
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    try:
        user_data = request.get_json()
        logging.info(f"Data received: {user_data}")
    except Exception as e:
        logging.error(f"Missing or invalid data: {e}")
        return jsonify({"error": "Bad request"}), 400

    if not user_data["name"] or not user_data["private"]:
        logging.error("Body does not contain name or private fields")
        return jsonify({"error": "Body must contain name and private fields"}), 400

    try:
        logging.info("Creating repo in GitHub")
        response = requests.post(f"https://api.github.com/user/repos", json=user_data, headers=headers)
        response.raise_for_status()
        return jsonify({"message": "Repository created successfully"}), 201
    
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return None
    except Exception as e:
        logging.error(f"An error occurred while trying to create GitHub repo: {e}")
        return jsonify({"error": "Failed to create repository"}), 500


@app.route('/check-repos-private')
def check_private():
    return check_private_repos()


@app.route('/get-repos')
def get_repos():
    return get_repo_names()


@app.route("/ready")
def ready():
    return jsonify({"status": "healthy"}),200

@app.route("/create-repo",methods=['POST'])
def create_repo():
    return create_git_repo()

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error_html.html",available_routes=available_routes)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)