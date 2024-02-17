import base64
import requests


class Github:
    ''' function for creation and updation of images '''

    def __init__(self, username :str, token :str, repo_name :str):
        ''' usefull variables '''
        self.USERNAME = username
        self.TOKEN = token
        self.REPO_NAME = repo_name
        self.IMAGE_DIR = "./image_output"

    def update_image_in_github(self,image_path, path_in_repo):
        ''' upload/update images'''

        # Read the image file as binary data
        with open(image_path, "rb") as file:
            image_data = file.read()

        # Encode the image data as base64
        encoded_image = base64.b64encode(image_data).decode()

        # Get the existing file content
        url = f"https://api.github.com/repos/{self.USERNAME}/{self.REPO_NAME}/contents/{path_in_repo}"
        headers = {
            "Authorization": f"token {self.TOKEN}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to get existing file content. Error:", response.text)

        existing_content = response.json()
        sha = existing_content.get('sha')

        # Extract the SHA hash from the response


        # Delete the existing file
        delete_url = f"https://api.github.com/repos/{self.USERNAME}/{self.REPO_NAME}/contents/{path_in_repo}"
        delete_payload = {
            "message": "Delete image",
            "sha": sha
        }
        delete_response = requests.delete(delete_url, headers=headers, json=delete_payload)
        if delete_response.status_code != 200:
            print("Failed to delete existing image. Error:", delete_response.text)

        # Upload the new file
        upload_url = f"https://api.github.com/repos/{self.USERNAME}/{self.REPO_NAME}/contents/{path_in_repo}"
        upload_payload = {
            "message": "Upload image",
            "content": encoded_image
        }
        upload_response = requests.put(upload_url, headers=headers, json=upload_payload)
        print(upload_response)
        print(upload_response.status_code)
        if upload_response.status_code == 201:
            print("Image updated successfully.")
        else:
            print("Failed to update image. Error:", upload_response.text)

