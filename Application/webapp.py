from flask import Flask, jsonify
import requests
from dotenv import load_dotenv
import json
import logging
import os

app = Flask(__name__)
load_dotenv()

GITHUB_USER = os.environ.get("GITHUB_USER") or "yuvals41"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if not GITHUB_TOKEN:
    logging.error("GitHub token not set. Exiting.")
    os._exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def request_github_api(url: str, headers: dict):
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return None



def get_repo_names():
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    logging.info("Requesting GitHub repos")
    repos = request_github_api(f"https://api.github.com/users/{GITHUB_USER}/repos", headers)

    if repos is None:
        return jsonify({"error": "Error requesting GitHub API"}), 500


    for i, data in enumerate(repos):
        repo_num = i + 1
        # repo_names.update({f"repo-name{i}": name["name"]})
        repo_names[f"repo-name{repo_num}"] =  data["name"]
    repo_names = json.dumps(repo_names)

    logging.info("created repos json")

    return repo_names,200


def check_private_repos():
    non_private_repos = dict()

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }

    logging.info("Checking for private repos")
    repos = request_github_api(f"https://api.github.com/users/{GITHUB_USER}/repos", headers)

    if repos is None:
        return jsonify({"error": "Error requesting GitHub API"}), 500

    if all(repo["private"] for repo in repos):
    
        return jsonify({"message":"all repos are not private"}),500
    
    for i, repo in enumerate(repos):
        repo_num = i + 1
        if repo["private"] == False:
            non_private_repos[f"repo{repo_num}"] = repo["name"]
        
    return jsonify({"message": f"these are the non private repos: {non_private_repos}"}), 200



@app.route('/check-repos-private')
def check_private():
    return check_private_repos()


@app.route('/get-repos')
def get_repos():
    return get_repo_names()


@app.route("/ready")
def ready():
    return jsonify({"status": "healthy"}),200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)