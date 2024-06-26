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

# picks a parent folder from a list to classify the folder
def select_parent_folder(file_name, folders):
    context = f"You are a file sorter that takes in a file and a list of folders and responds with the folder that the file should be placed into. Responses are limited to the name of a folder. You must not provide any other reasoning or information. Do not include any special characters or symbols."
    prompt = f"A file named '{file_name}' needs to be sorted into one of the following folders: {', '.join(folders)}. Determine the appropriate folder for this file. Return only the folder name."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    selected_parent_folder = response.choices[0].message.content

    return selected_parent_folder

# ai suggests a new folder to put the file into
def suggest_parent_folder(file_name):
    context = "You are a file classifier that takes in a file and responds with a classification based on the type of file or name. Responses are limited to the name of a classification. You must not provide any other reasoning or information. Do not include any special characters or symbols."
    prompt = f"A file named '{file_name}' needs to be classified. Determine the appropriate classification for this file based on the file type. The classifications should be general based on what the file type does. Return only the classification name and nothing else."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    suggested_parent_folder = response.choices[0].message.content

    return suggested_parent_folder

# checks if the new parent folder is redundant or should be a subfolder
def check_new_parent_folder(folders, suggested_parent_folder):
    context = "You are checking whether or not a new classification should be added to a list of file classifications or if it is redundant. You must provide either Keep or Drop and must not provide any other reasoning or information. Do not include any special characters or symbols."
    prompt = f"Is the classification '{suggested_parent_folder}' redundant to this list of classifications: {', '.join(folders)}? If it is redundant or is better suited to be a subclass of another class, respond with Drop. If it is not redundant and should not be a subclass of another class, respond with Keep. Return only Keep or Drop and nothing else."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    keep_new_folder = response.choices[0].message.content

    return keep_new_folder

# picks a subfolder from a list to classify the folder
def select_sub_folder(file_name, parent_folder, folders):
    context = "You are a file sorter that takes in a file and a list of folders and responds with the folder that the file should be placed into. Responses are limited to the name of a folder. You must not provide any other reasoning or information. Do not include any special characters or symbols."
    prompt = f"A file named '{file_name}' is to be placed inside a folder named '{parent_folder}'. The file needs to be sorted into one of the following subfolders: {', '.join(folders)} inside '{parent_folder}'. Determine the appropriate subfolder for this file. Return only the folder name."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    selected_sub_folder = response.choices[0].message.content

    return selected_sub_folder

# ai suggests a new subfolder to put the file into
def suggest_sub_folder(file_name, parent_folder):
    context = "You are a file classifier that takes in a file and responds with a classification based on the type of file or name. Responses are limited to the name of a classification. You must not provide any other reasoning or information. Do not include any special characters or symbols."
    prompt = f"A file named '{file_name}' is classified as '{parent_folder}'. There must be another classification done to further sort this file. Determine the appropriate subclassification for this file based on the file type. The classifications should be general and based on what the file type does. Return only the classification name and nothing else."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    suggested_sub_folder = response.choices[0].message.content

    return suggested_sub_folder

# selects between two subfolders
def select_between_two_sub_folders(file_name, parent_folder, selected_folder, suggested_folder):
    context = "You are a file classifier that takes in a file that is already classified and tries to classify it further. Responses are limited to the name of a subclassification. You must not provide any other reasoning or information. Do not include any special characters or symbols."
    prompt = f"A file named '{file_name}' is classified as '{parent_folder}'. There must be another classification done to further sort this file. Determine the appropriate subclassification for this file between the two choices, '{selected_folder}' and '{suggested_folder}'. The subclassification should be general and based on what the file type does. Return only the classification name and nothing else."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    suggested_sub_folder = response.choices[0].message.content

    return suggested_sub_folder

# checks if the new folder is redundant and then makes it if it is not
def check_new_sub_folder(parent_folder, subfolders, suggested_sub_folder):
    context = "You are checking whether or not a new subclassification should be added to a list of file subclassifications or if it is redundant. You must provide either Keep or Drop and must not provide any other reasoning or information. Do not include any special characters or symbols."
    prompt = f"Inside the classification '{parent_folder}', is the subclassification '{suggested_sub_folder}' redundant to this list of subclassifications: {', '.join(subfolders)}? If it is redundant in any way, respond with Drop. If it is not redundant in any way, respond with Keep. Return only Keep or Drop and nothing else."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": prompt}
        ]
    )

    keep_new_folder = response.choices[0].message.content

    return keep_new_folder

# moves the file into a path
def move_file(file_path, folder_path):
    # ensure the new subfolder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_name = os.path.basename(file_path)
    new_file_path = os.path.join(folder_path, file_name)
    os.rename(file_path, new_file_path)

    return new_file_path

def sort_file(file_path, folders):
    # gets the desktop directory
    directory = os.path.expanduser("~/Desktop")
    folders = get_folders(directory)

    # appends miscellaneous to folders to always have an option
    folders.append("Miscellaneous")
    # print the folders to check what is there
    print("Folders found in the directory:")
    for folder in folders:
        print(folder)

    # check if the file exists
    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)

        # ask the ai to pick a folder from list
        selected_parent_folder = select_parent_folder(file_name, folders)
        print("selected parent folder:" +selected_parent_folder)

        # ask the ai to suggest a new folder
        suggested_parent_folder = suggest_parent_folder(file_name)
        print("suggested parent folder:" + suggested_parent_folder)

        # ask the ai to pick a folder from list including the new one
        new_folders = folders
        new_folders.append(suggested_parent_folder)
        new_selected_parent_folder = select_parent_folder(file_name, new_folders)
        print("new selected parent folder:" + new_selected_parent_folder)
    
        # checks to make sure the best option chosen by the ai is chosen
        # the original selected folder is correct
        if selected_parent_folder == new_selected_parent_folder:
            chosen_parent_folder = selected_parent_folder

        # the last selected folder is correct
        elif selected_parent_folder == "Miscellaneous" and not new_selected_parent_folder == "Miscellaneous":
            chosen_parent_folder = new_selected_parent_folder

        # the suggested folder is correct because the rest are marked miscellaneous
        elif selected_parent_folder == "Miscellaneous" and new_selected_parent_folder == "Miscellaneous" and not suggested_parent_folder == "Miscellaneous":
            chosen_parent_folder = suggested_parent_folder
        
        # if they are all miscellaneous then it will be marked miscellaneous
        else:
            chosen_parent_folder = selected_parent_folder
        print("chosen parent folder:" + chosen_parent_folder)

        # check to see if a new folder would need to be made
        if chosen_parent_folder == suggested_parent_folder and not chosen_parent_folder == selected_parent_folder:
            # ask the ai if the new folder should be kept
            keep_new_folder = check_new_parent_folder(folders, suggested_parent_folder)
            print(keep_new_folder)
            if keep_new_folder == "Keep":
                # if folder should be kept make new folder in directory
                new_folder_path = os.path.join(directory, suggested_parent_folder)
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)
                    print(f"Folder '{suggested_parent_folder}' created on the desktop.")    
            else:
                # folder should not be kept so we switch to the other selection
                chosen_parent_folder = selected_parent_folder
        print("real chosen parent folder:" + chosen_parent_folder)

        # make sure the new parent folder path is made and the folder is created
        new_folder_path = os.path.join(directory, chosen_parent_folder)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            print(f"Folder '{chosen_parent_folder}' created on the desktop.")  

        # print the folders to check what is there
        folders = get_folders(directory)
        print("Folders found in the directory:")
        for folder in folders:
            print(folder)

        # get the subfolders from the chosen patent folder
        subfolders = get_folders(new_folder_path)
        # appends miscellaneous to folders to always have an option
        subfolders.append("Miscellaneous")
        # print the folders to check what is there
        print("Folders found in the parent folder:")
        for folder in subfolders:
            print(folder)

        # ask the ai to pick a subfolder from list
        selected_sub_folder = select_sub_folder(file_name, chosen_parent_folder, subfolders)
        print("selected sub folder:" + selected_sub_folder)

        # ask the ai to create a new folder
        suggested_sub_folder = suggest_sub_folder(file_name, chosen_parent_folder)
        print("suggested sub folder:" + suggested_sub_folder)

        # ask the ai to pick a folder from list including the new one
        subfolders.append(suggested_sub_folder)
        select_between_sub_folder = select_between_two_sub_folders(file_name, chosen_parent_folder, selected_sub_folder, suggested_sub_folder)
        print("chosen sub folder:" + select_between_sub_folder)

        # checks to make sure the best option chosen by the ai is chosen
        # the new selected subfolder is correct
        if not select_between_sub_folder == "Miscellaneous":
            chosen_sub_folder = select_between_sub_folder

        # the original selected subfolder is correct
        elif select_between_sub_folder == "Miscellaneous" and not selected_sub_folder == "Miscellaneous":
            chosen_sub_folder = selected_sub_folder
        
        # the suggested subfolder is correct
        elif selected_sub_folder == "Miscellaneous" and select_between_sub_folder == "Miscellaneous" and not suggested_sub_folder == "Miscellaneous":
            chosen_sub_folder = suggested_sub_folder

        # the subfolder is miscellaneous
        else:
            chosen_sub_folder = select_between_sub_folder
        print("real chosen sub folder:" + chosen_sub_folder)

        # check if the new folder needs to be made
        if chosen_sub_folder == suggested_sub_folder and not chosen_sub_folder == selected_sub_folder:
            # ask the ai if making this subfolder is beneficial
            keep_new_folder = check_new_sub_folder(chosen_parent_folder, subfolders, suggested_sub_folder)
            print(keep_new_folder)
            if keep_new_folder == "Keep":
                # if we keep the subfolder we create it
                new_sub_folder_path = os.path.join(new_folder_path, suggested_sub_folder)
                if not os.path.exists(new_sub_folder_path):
                    os.makedirs(new_sub_folder_path)
                    print(f"Folder '{suggested_sub_folder}' created in '{chosen_parent_folder}'.")
            else:
                # subfolder should not be kept so we switch to the other selection
                chosen_sub_folder = selected_sub_folder
        
        # make sure the subfolder path exists and the folder has been created
        new_sub_folder_path = os.path.join(new_folder_path, chosen_sub_folder)
        if not os.path.exists(new_sub_folder_path):
            os.makedirs(new_sub_folder_path)
            print(f"Folder '{chosen_sub_folder}' created in '{chosen_sub_folder}'.")  

        # move the file and get the file path
        new_file_path = move_file(file_path, new_sub_folder_path)
        print(f"File '{file_name}' moved to folder '{chosen_sub_folder}'")

        #return the new file path
        return new_file_path

    else:
        print("File not found.")
        return file_path
