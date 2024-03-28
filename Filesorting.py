import os
import time
from openai import OpenAI
client = OpenAI()

# places folders in directory to an array
def get_folders(directory):
    folders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            folders.append(item)
    return folders

# ai suggests a new folder to put the file into
def suggest_folder(file_name):
    prompt = f"A file named '{file_name}' needs to be classified. Determine the appropriate classification for this file based on the file type. The classifications should be general based on what the file type does. Return only the folder name and nothing else."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": "You are a file classifier that takes in a file and responds with a classification based on the type of file or name. Responses are limited to the name of a folder. You must not provide any other reasoning or information."},
            {"role": "user", "content": prompt}
        ]
    )

    suggested_folder = response.choices[0].message.content

    return suggested_folder

# checks if the new folder is redundant and then makes it if it is not
def check_new_folder(folders, suggested_folder):
    prompt = f"Is the classification '{suggested_folder}' redundant to this list of classifications: {', '.join(folders)}? If it is redundant or is better suited to be a subclass of another class, respond with Drop. If it is not redundant and should not be a subclass of another class, respond with Keep. Return only Keep or Drop and nothing else."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": "You are checking whether or not a new classification should be added to a list of file classifications or if it is redundant. You must provide either Keep or Drop and must not provide any other reasoning or information."},
            {"role": "user", "content": prompt}
        ]
    )

    keep_new_folder = response.choices[0].message.content

    return keep_new_folder

# picks a folder from a list to classify the folder
def pick_folder(file_name, folders):
    prompt = f"A file named '{file_name}' needs to be sorted into one of the following folders: {', '.join(folders)}. Determine the appropriate folder for this file. Return only the folder name."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": "You are a file sorter that takes in a file and a list of folders and responds with the folder that the file should be placed into. Responses are limited to the name of a folder. You must not provide any other reasoning or information."},
            {"role": "user", "content": prompt}
        ]
    )

    selected_folder = response.choices[0].message.content

    return selected_folder

def main():
    # gets the folders on the desktop
    directory = os.path.expanduser("~/Desktop")
    folders = get_folders(directory)
    print("Folders found in the directory:")
    for folder in folders:
        print(folder)

    file_path = input("Enter the path to the file: ")
    # check if the file exists
    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
        # ask to pick a folder from list
        selected_folder = pick_folder(file_name, folders)
        print("selected folder:" +selected_folder)
        # ask for a new folder
        suggested_folder = suggest_folder(file_name)
        print("suggested folder:" +suggested_folder)
        # ask to pick a folder from list including the new one
        folders.append(suggested_folder)
        new_selected_folder = pick_folder(file_name, folders)
        print("new selected folder:" + new_selected_folder)
    
        if selected_folder == new_selected_folder:
            # the selected folder is correct
            chosen_folder = selected_folder
        elif selected_folder == "Miscellanious":
            # the new selected folder is correct
            chosen_folder = new_selected_folder
        else:
            chosen_folder = selected_folder
        print(chosen_folder)

        if chosen_folder == suggested_folder and chosen_folder != selected_folder:
            # check if the new folder should be kept
            keep_new_folder = check_new_folder(folders, suggested_folder)
            print(keep_new_folder)
            if keep_new_folder == "Keep":
                new_folder_path = os.path.join(directory, suggested_folder)
                os.makedirs(new_folder_path)
                print(f"Folder '{suggested_folder}' created on the desktop.")
            else:
                chosen_folder = selected_folder

        folders = get_folders(directory)
        print("Folders found in the directory:")
        for folder in folders:
            print(folder)

    else:
        print("File not found.")

if __name__ == "__main__":
    main()
