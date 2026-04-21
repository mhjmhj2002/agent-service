import os
import requests
import base64

BASE_URL = "https://api.github.com"


def get_headers():
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise Exception("GITHUB_TOKEN não definido no ambiente")

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }


def get_owner():
    owner = os.getenv("GITHUB_OWNER")

    if not owner:
        raise Exception("GITHUB_OWNER não definido no ambiente")

    return owner


def create_branch(repo, branch_name, base="main"):
    headers = get_headers()
    owner = get_owner()

    ref_url = f"{BASE_URL}/repos/{owner}/{repo}/git/ref/heads/{base}"
    ref_response = requests.get(ref_url, headers=headers)
    ref_response.raise_for_status()

    sha = ref_response.json()["object"]["sha"]

    create_url = f"{BASE_URL}/repos/{owner}/{repo}/git/refs"

    response = requests.post(
        create_url,
        headers=headers,
        json={
            "ref": f"refs/heads/{branch_name}",
            "sha": sha
        }
    )

    response.raise_for_status()
    return response.json()


def create_file(repo, path, content, message, branch):
    headers = get_headers()
    owner = get_owner()

    url = f"{BASE_URL}/repos/{owner}/{repo}/contents/{path}"

    encoded = base64.b64encode(content.encode()).decode()

    response = requests.put(
        url,
        headers=headers,
        json={
            "message": message,
            "content": encoded,
            "branch": branch
        }
    )

    response.raise_for_status()
    return response.json()


def create_pull_request(repo, title, body, head, base="main"):
    headers = get_headers()
    owner = get_owner()

    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"

    response = requests.post(
        url,
        headers=headers,
        json={
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }
    )

    response.raise_for_status()
    return response.json()


def get_open_pull_requests(repo):
    headers = get_headers()
    owner = get_owner()

    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls?state=open"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching PRs: {response.text}")

    return response.json()