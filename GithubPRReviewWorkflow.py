import os
import sys

from dotenv import load_dotenv
from github import Github
from openai import OpenAI
import requests

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# Set up Perplexity API
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")
# Initialize GitHub client
g = Github(GITHUB_TOKEN)

def perplexity_analyze(prompt, model):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

def get_pr_diff(repo_name, pr_number):
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    return pr.get_files()

def analyze_code(file_content, model):
    prompt = f"""
    Analyze the following code for:
    1. Unreachable code
    2. Missing unit tests
    3. Optimization opportunities
    4. Time complexity issues
    5. Best practices violations

    Code:
    {file_content}

    Provide a detailed report on each aspect.
    """
    return perplexity_analyze(prompt, model)

def generate_report(repo_name, pr_number, model):
    files = get_pr_diff(repo_name, pr_number)
    report = []

    for file in files:
        if file.filename.endswith(('.py', '.js', '.java', '.cpp')):  # Add more extensions as needed
            analysis = analyze_code(file.patch, model)
            report.append(f"File: {file.filename}\n{analysis}\n")

    return "\n".join(report)


def code_review_workflow(input_link, model):
    if "pull" in input_link:
        # It's a PR link
        repo_name, pr_number = parse_pr_link(input_link)
    else:
        # It's a repo link, get the latest PR
        repo_name = parse_repo_link(input_link)
        pr_number = get_latest_pr(repo_name)

    report = generate_report(repo_name, pr_number, model)

    # Post the report as a comment on the PR
    post_comment(repo_name, pr_number, report)

    return report

def parse_pr_link(link):
    # Extract repo name and PR number from the link
    parts = link.split('/')
    repo_name = f"{parts[-4]}/{parts[-3]}"
    pr_number = int(parts[-1])
    return repo_name, pr_number


def parse_repo_link(link):
    # Extract repo name from the link
    parts = link.split('/')
    return f"{parts[-2]}/{parts[-1]}"


def get_latest_pr(repo_name):
    repo = g.get_repo(repo_name)
    prs = repo.get_pulls(state='open', sort='created', direction='desc')
    return prs[0].number


def post_comment(repo_name, pr_number, comment):
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(comment)


# Example usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"sys.argv: {sys.argv}")
        repo_or_pr_link = sys.argv[1]
        model = sys.argv[2]
        print(f"model: {model}")
    else:
        repo_or_pr_link = "https://github.com/sam253narula/ExperimentalRepoForAgenticWorkflow/pull/5"
        model = "sonar"

    report = code_review_workflow(repo_or_pr_link, model)
    # print(report)
