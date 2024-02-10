import requests
import base64
import tkinter as tk
from tkinter import filedialog

# Function to encode credentials
def encode_credentials(username, password):
    return base64.b64encode(f'{username}:{password}'.encode()).decode('utf-8')

# Function to send files to Flask OCR app
def send_to_flask_ocr(file_paths, search_string, flask_url):
    files = {f'file{i}': open(file_path, 'rb') for i, file_path in enumerate(file_paths, 1)}
    response = requests.post(flask_url, files=files, data={'search_string': search_string})
    # Closing files
    for file in files.values():
        file.close()
    return response.text

# Function to create a post in WordPress
def create_wordpress_post(title, content, wordpress_url, username, password):
    headers = {'Authorization': 'Basic ' + encode_credentials(username, password)}
    post_data = {'title': title, 'content': content, 'status': 'publish'}
    response = requests.post(f'{wordpress_url}/posts', headers=headers, json=post_data)
    return response

# GUI for file selection
def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(title='Select files')
    return list(file_paths)

# Select files using the file dialog
file_paths = select_files()
search_string = input("Enter the search string: ")

# URL of your Flask OCR app
flask_ocr_url = "http://your-flask-app-url/upload"

# WordPress credentials
username = "rqk7tn"
password = "AUqy JPcp usNL a14M h28m yCf0"
wordpress_url = "https://wealif.com/wp-json/wp/v2"

# Sending files to Flask OCR app
ocr_results = send_to_flask_ocr(file_paths, search_string, flask_ocr_url)

# Creating a post in WordPress with OCR results
wp_response = create_wordpress_post("OCR Results", ocr_results, wordpress_url, username, password)
print(wp_response)
