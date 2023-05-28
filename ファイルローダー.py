import os

def read_files_in_directory(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                contents = file.read()
                print(contents)

# ディレクトリのパスを指定
directory_path = '/path/to/directory'

read_files_in_directory(directory_path)
