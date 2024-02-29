import os
import shutil

# run the user's program in our generated folders
os.chdir('module/root_folder')


def change_path(cmd):
    if len(cmd) == 2:
        return "Invalid Command"
    try:
        path = cmd.split(" ")[1]
        if path == "..":
            os.chdir('../')
            return os.getcwd().split("\\")[-1]
        else:
            current_working_directory = os.getcwd()
            paths = []

            if path in current_working_directory:
                directories = current_working_directory.split("\\")
                for directory in directories:
                    paths.append(directory)
                    if directory == path:
                        break
                absolute_path = "/".join(paths)
                os.chdir(absolute_path)
                return paths[-1]
            else:
                absolute_path = "./" + path
                os.chdir(absolute_path)
                return absolute_path.split("/")[-1]
    except FileNotFoundError:
        return "Invalid Command"


def list_files(cmd):
    files_list = []
    for file in os.listdir("."):
        if "." not in file:
            files_list.append(file)
    if command == "ls":
        for file in os.listdir("."):
            if "." in file:
                files_list.append(file)
        return "\n".join(files_list)
    elif command == "ls -l":
        for file in os.listdir("."):
            if "." in file:
                files_list.append(file + " " + str(os.stat(file).st_size))
        return "\n".join(files_list)
    elif command == "ls -lh":
        for file in os.listdir("."):
            if "." in file:
                file_size = os.stat(file).st_size
                files_list.append(file + " " + get_readable_size(file_size))
        return "\n".join(files_list)
    else:
        return "Invalid Command"

        
def remove_files(cmd):
    count = 0 
    if len(cmd) == 2:
        print("Specify the file or directory")
    elif cmd.split(' ')[1].startswith('.'):
        files_list = os.listdir('.')
        for file_name in files_list:
           if file_name.endswith(cmd.split(' ')[1]):
                    os.remove(file_name)
                    count = count + 1 
        if count == 0:
                print(f"File extension {cmd.split(' ')[1]} not found in this directory")
    else:
        try:
            path = cmd.split(" ")[1]
            if "." in path:
                os.remove(path)
            else:
                shutil.rmtree(path)
        except FileNotFoundError:
            print("No such file or directory")


def move_file(cmd):
    paths = cmd.split(" ")
    if len(paths) != 3:
        print("Specify the current name of the file or directory and the new location and/or name")
    elif paths[1].startswith('.'):
        count = 0
        files_list_from = os.listdir()
        for file_name_from in files_list_from:
            if file_name_from.endswith(paths[1]):
                count += 1
        if count == 0:
             print(f'File extension {paths[1]} not found in this directory')   
            
        files_list_to = []
        try:
            files_list_to = os.listdir(paths[2])
        except FileNotFoundError:
            print("No such file or directory")
            return  # Return to exit the function early
        files_duplicate = [i for i in files_list_from if i in files_list_to]
        for file_name_from in files_list_from:
            if file_name_from.endswith(paths[1]):
                count += 1  # Simplified count increment
                if file_name_from in files_duplicate:
                    ask = input(f'{file_name_from} already exists in this directory. Replace? (y/n)')
                    if ask == 'y':
                        try:
                            os.remove(os.path.join(paths[2], file_name_from))
                            shutil.move(file_name_from, paths[2])
                        except FileNotFoundError:
                            print("No such file or directory")
                    else:
                        shutil.move(file_name_from, paths[2])
           
    else:
        try:
            if os.path.isfile(paths[2]):
                print("The file or directory already exists")
            else:
                #os.rename(paths[1], paths[2])
                try:
                    shutil.move(paths[1], paths[2])
                except shutil.Error:
                    print("The file or directory already exists")
        except FileNotFoundError:
            print(f"No such file or directory")


def copy_file(cmd):
    count = 0 
    paths = cmd.split(" ")
    if len(paths) == 1:
        print("Specify the file")
    elif len(paths) > 3:
        print('Specify the current name of the file or directory and the new location and/or name')
    elif not os.path.isdir(paths[2]):
        print("No such file or directory")
    elif cmd.split(' ')[1].startswith('.'):
        files_list_from = os.listdir()
        files_list_to = os.listdir(paths[2])
        files_duplicate = [i for i in files_list_from if i in files_list_to]
        for file_name_from in files_list_from:
            if file_name_from.endswith(paths[1]):
                count = count + 1
                if file_name_from in files_duplicate:
                    print(f'{file_name_from} already exists in this directory. Replace?(y/n)')
                    ask = input()
                    if ask == 'y':
                        shutil.copy2(file_name_from, paths[2])

                else:
                    print("file_name_from = ", file_name_from)
                    print("paths[2] = ", paths[2])
                    shutil.copy2(file_name_from, paths[2])
        if count == 0:
            print(f"File extension {paths[1]} not found in this directory")
    else:
        if paths[2] == '..' or paths[2] == '../':
            old_path = os.getcwd() + '/'
            os.chdir('../')
            print(os.getcwd())
            if os.path.isfile(paths[1]):
                print("The file exists")
            else:
                os.chdir(old_path)
                shutil.copy2(paths[1], '../')
        else:
            try:
                shutil.copy2(paths[1], paths[2])
            except shutil.SameFileError:
                print(f'{paths[1]} already exists in this directory')





def make_directory(cmd):
    if len(cmd) == 5:
        print("Specify the name of the directory to be made")
    else:
        try:
            path = cmd.split(" ")[1]
            os.mkdir(path)
        except FileExistsError:
            print("The directory already exists")


def get_readable_size(size):
    if size < 1024:
        return f'{size}B'
    if 1024 <= size < 1024 ** 2:
        return f'{round(size/1024)}KB'
    if 1024 ** 2 <= size < 1024 ** 3:
        return f'{round(size/(1024 ** 2))}MB'
    else:
        return f'{round(size / (1024 ** 3))}GB'


print('Input the command')
command = input()
while command != "quit":
    if command == "pwd":
        print(os.getcwd())
    elif command.startswith("cd"):
        print(change_path(command))
    elif command.startswith("ls"):
        print(list_files(command))
    elif command.startswith("rm"):
        remove_files(command)
    elif command.startswith("mv"):
        move_file(command)
    elif command.startswith("mkdir"):
        make_directory(command)
    elif command.startswith("cp"):
        copy_file(command)
    else:
        print('Invalid Command.')
    command = input()
