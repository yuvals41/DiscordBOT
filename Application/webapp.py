from flask import Flask, jsonify, request
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
    repo_names = {}
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

    logging.info("created repos json")

    return jsonify(repo_names),200


def check_private_repos():
    non_private_repos = []

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
    
    for repo in repos:
        if repo["private"] == False:
            non_private_repos.append(repo["name"])
        
    return jsonify({"message": f"these are the non private repos: {non_private_repos}"}), 200

def create_git_repo():
    headers = {
        "Accept": "application/vnd.github+json",
        f"Authorization": "Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    try:
        try:
            user_data = request.json
            # return jsonify(f"data received: {data}"), 201
            logging.info(f"data received: {user_data}")
        except Exception as e:
            logging.error(f"Missing data: {e}")
            return jsonify("bad request"), 400
        
        if not user_data["repo_name"] or not user_data["private"]:
            logging.error("Body does not contain repo_name or private fields")
            return jsonify("Body does not contain repo name or specified if repo is private"), 400
        
        logging.info("creating repo in github")
        requests.post(f"https://api.github.com/{GITHUB_USER}/repos",data=user_data,headers=headers) #TODO  need to create new token with read permissions
        # print(response)

    except Exception as e:
        logging.error(f"An error has a occured while trying to create github repo {e}")
        return e, 500





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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)