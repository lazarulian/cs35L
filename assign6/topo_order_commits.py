#!/usr/local/cs/bin/python3

import os
from pathlib import Path



def check_directories(dir, query, remove_path):
    # Checks Whether any of the directories are named a certain thing
    directories = [f.path for f in os.scandir(dir) if f.is_dir()]
    for i in directories:
        if i.find(query) != -1:
            return(i.replace(remove_path, ''))
    return 1

def discover_git_directory():
    # Starting Directory
    pwd = Path(os.getcwd())
    search_query, remove_query = '/.git', '.git'
    
    # Iterating Through Parent Directories
    while str(pwd) != '/':
        directory_found = check_directories(pwd, search_query, search_query)
        if directory_found != 1:
            return directory_found
        pwd = pwd.parent.absolute()
        
    # Iterating Through Last Parent Directory    
    directory_found = check_directories(pwd, search_query, remove_query)
    if directory_found != 1:
            return directory_found
        
    # Returning None Found
    os.write(2, b"Not inside a Git repository\n")
    return 1

def list_local_branches(branch_directory, slash):
    # Set the Working Directory to the .git/refs/heads/
    os.chdir(branch_directory)
    branch_list = []
    sub_directories=os.listdir()
    
    # Searching whether they are Valid Branches
    for branch_name in sub_directories:
        check_file = branch_directory+"/"+branch_name
        if os.path.isfile(check_file):
            branch_list.append(slash + branch_name)
        else:
            # Use Recursion to test Substring of Branch
           branch_list += list_local_branches(check_file, branch_name +"/")
    
    return branch_list


def main():
    # Finding the .git folder
    git_path = discover_git_directory()
    
    # Navigating to the Branches Folder
    branch_path = git_path + "/.git/refs/heads"
    
    # Finding the Branches
    print(list_local_branches(branch_path, ""))

if __name__ == '__main__':
    main()