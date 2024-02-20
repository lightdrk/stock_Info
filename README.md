## Overview

This project is designed to [brief description of the project].

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3 installed on your local machine.
- Access to the internet.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone <repository_url>
    ```

2. Navigate to the project directory:

    ```bash
    cd <project_directory>
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Getting Credentials

To use this project, you will need to obtain credentials for the following services:

- **GitHub**: You need a GitHub account and a personal access token with appropriate permissions.

    1. Go to [GitHub](https://github.com/) and sign in or create a new account.
    2. Once logged in, navigate to your **Settings**.
    3. In the left sidebar, click on **Developer settings** and then **Personal access tokens**.
    4. Generate a new token with the necessary permissions (typically, repo access is needed).
    5. Copy the generated token.

- **Google Sheets**: You need credentials for Google Sheets API.

    1. Go to [Google Developers Console](https://console.developers.google.com/).
    2. Create a new project (if you haven't already).
    3. Enable the Google Sheets API for your project.
    4. Create credentials for a service account.
    5. Download the JSON file containing your credentials.

## Setting Up Credentials

Once you have obtained the necessary credentials, follow these steps:

1. Create a directory named `creds` in the project root if not seen/avilable .
2. ```bash
   python main.py --new

## Usage

To run the project, execute the main script:

```bash
python main.py
