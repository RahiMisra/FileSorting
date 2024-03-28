import os
import time
from openai import OpenAI
client = OpenAI()

def file_sorter(file_name, folders):
    prompt = f"A file named '{file_name}' needs to be classified. Determine the appropriate classification for this file based on the file type. The classifications should be general based on what the file type does. Return only the folder name and nothing else."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": "You are a file classifier that takes in a file and responds with a classification based on the type of file or name. Responses are limited to the name of a folder. You must not provide any other reasoning or information."},
            {"role": "user", "content": prompt}
        ]
    )

    folder_response = response.choices[0].message.content

    return folder_response

# places folders in directory to an array
def get_folders(directory):
    folders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folders.append(item)
    return folders

def main():
    # gets the folders on the desktop
    directory = os.path.expanduser("~/Desktop")
    folders = get_folders(directory)

    print("Folders found in the directory:")
    for folder in folders:
        print(folder)

    file_path = input("Enter the path to the file: ")
    
    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        folder_response = file_sorter(file_name, folders)
        print(folder_response)
    else:
        print("File not found.")

if __name__ == "__main__":
    main()
