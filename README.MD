# GitHub PR Review Agent

**GitHub PR Review Agent** is a GitHub Action that leverages the Perplexity API to provide AI-powered pull request reviews. This action simplifies the review process by analyzing the changes and offering insightful feedback.

## Features

- Automates the pull request review process.
- Provides AI-powered feedback using the Perplexity API.
- Supports integration directly into your GitHub workflows.

## Inputs

| Input Name            | Description                     | Required | Example |
|-----------------------|---------------------------------|----------|---------|
| `github_token`        | GitHub token for authentication. | Yes      | `${{ secrets.GITHUB_TOKEN }}` |
| `perplexity_api_key`  | Perplexity API Key for AI interaction. | Yes      | `${{ secrets.PERPLEXITY_API_KEY }}` |

## Outputs

This action does not generate specific outputs but comments directly on the pull request with the AI-generated review.

## Example Workflow

Here’s how to use the **GitHub PR Review Agent** in your GitHub Actions workflow:

```yaml
name: AI PR Review

permissions:
  contents: read
  pull-requests: write
  issues: write

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-pr-review:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: AI PR Review
      uses: sam253narula/ai-pr-reviewer@v2.0.0
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        perplexity_api_key: ${{ secrets.PERPLEXITY_API_KEY }}
