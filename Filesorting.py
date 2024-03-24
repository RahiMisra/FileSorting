import os

def get_file_type(file_path):
    remaining_path, file_extension = os.path.splitext(file_path)
    
    # define file type mappings
    file_type_mapping = {
        '.txt': 'Text File',
        '.pdf': 'PDF Document',
        '.docx': 'Word Document',
        '.xlsx': 'Excel Spreadsheet',
        '.jpg': 'JPEG Image',
        '.png': 'PNG Image',
    }
    
    # find file type mapped to extension
    file_type = file_type_mapping.get(file_extension, 'Unknown File Type')
    return file_type

def main():
    file_path = input("Enter the path to the file: ")
    
    if os.path.exists(file_path):
        file_type = get_file_type(file_path)
        print(f"The file '{file_path}' is of type: {file_type}")
    else:
        print("File not found.")

if __name__ == "__main__":
    main()
