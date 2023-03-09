#!/usr/local/cs/bin/python3

import os
from pathlib import Path
import zlib
import copy
from collections import deque

def check_directories(dir, query, remove_path):
    # Checks Whether any of the directories are named a certain thing
    directories = [f.path for f in os.scandir(dir) if f.is_dir()]
    for i in directories:
        if i.find(query) != -1:
            return(i.replace(remove_path, ''))
    return 1

def clear_path():
    current_path = os.getcwd()
    while current_path != "/":
        current_path = os.getcwd()
        if os.path.exists(current_path+ "/.git"):
            return
        else:
            if current_path != "/":
                os.chdir(current_path + "/..")
    return

def discover_git_directory():
    # Starting Directory
    clear_path()
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

def get_branch_hashes(branches):
    # Returns the Hash of the Branches Given
    hash_path = discover_git_directory() + "/.git/refs/heads"
    branch_hashes = []
    
    i = 0
    while (i != len(branches)):
        branch = branches[i]
        branch_hashes.append(open(hash_path+"/"+branch, "r").readline().strip())
        i += 1
        
    return branch_hashes

def match_branch_hash(branches, hashes):
    branch_hash_dict = {}
    for i in range(len(branches)):
        branch_hash_dict.setdefault(hashes[i], [])
        branch_hash_dict[hashes[i]].append(branches[i])
    return branch_hash_dict
    
    
class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()
        
    def add_parent(self, parent):
        self.parents.add(parent)
    
    def remove_parent(self, parent):
        self.parents.remove(parent)
    
    def add_child(self, child):
        self.children.add(child)
    
    def remove_child(self, child):
        self.children.remove(child)
        
def construct_commit_graph(branch_hashes):
    # Initial Graph Construction Setup (BFS Method)
    commit_graph = {}
    visited_hashes = set()
    stack = branch_hashes
    
    # Starting the BFS
    while len(stack) != 0:
        curr_hash = stack[-1]
        stack.pop()
        
        # Skip Already Processed Hashes
        if curr_hash in visited_hashes: 
            continue
        
        # Add Current Node to the Graph
        if curr_hash in commit_graph:
            pass
        else:
            commit_graph[curr_hash] = CommitNode(curr_hash)
        
        # Storing Node in Current Variable
        curr_commit_node = commit_graph[curr_hash]
        
        # Decompressing Git Information
        file = open((discover_git_directory() + '/.git/objects/' + curr_hash[:2] + '/' + curr_hash[2:]), "rb")
        decompressed_commit = zlib.decompress(file.read()).decode()
        split_decompressed_commit = decompressed_commit.split()
        
        # Adding the Parent Commits to the Node
        for i in range(0, len(split_decompressed_commit)):
            if  split_decompressed_commit[i] == 'parent':
                curr_commit_node.add_parent(split_decompressed_commit[i+1])
        
        # Adding Parents to be Explored
        for parent in curr_commit_node.parents:
            # Add the Parent to the Commit Graph
            if parent not in commit_graph:
                commit_graph[parent] = CommitNode(parent)
            # Add the Parent to the Visited Hashes
            if parent not in visited_hashes:
                stack.append(parent)

            # Add Sibling Relation from Parent
            commit_graph[parent].children.add(curr_hash)
        
        # Add Hash as Processed
        visited_hashes.add(curr_hash)
            
    return commit_graph

def detect_cycles(res, commit_graph):
    if len(res) < len(commit_graph):
        raise Exception("Cycle Detected")
    return
        
def sort_graph_topologically(commit_graph):
    # Based on Kahn's Algorithm
    duplicate_graph = copy.deepcopy(commit_graph)
    no_children = deque()
    
    # Starting with the Tips of the Graph to (Find Parents)
    for duplicate_commit_hash in duplicate_graph:
        if len(duplicate_graph[duplicate_commit_hash].children) == 0:
            no_children.append(duplicate_commit_hash)
    
    res = []
    
    # Processing the Leaves of the Graph
    while len(no_children) > 0:
        duplicate_commit_hash = no_children.popleft()
        res.append(duplicate_commit_hash)
        
        for parent_hash in list(duplicate_graph[duplicate_commit_hash].parents):
            duplicate_graph[duplicate_commit_hash].remove_parent(parent_hash)
            duplicate_graph[parent_hash].remove_child(duplicate_commit_hash)
            
            if len(duplicate_graph[parent_hash].children) != 0:
                pass
            else:
                no_children.append(parent_hash)
    
    # Checking for Cycles    
    detect_cycles(res, commit_graph)
    return res

    
def topo_order_commits():
    # Finding the .git folder
    git_path = discover_git_directory()
    
    # Navigating to the Branches Folder
    branch_path = git_path + "/.git/refs/heads"
    
    # Finding the Branches
    branches = list_local_branches(branch_path, "")
    
    # Finding the Hashes
    hashes = get_branch_hashes(branches)
    
    # Linking the Hash to the Branches
    branch_matching = match_branch_hash(branches, hashes)
    
    commit_graph = construct_commit_graph(hashes)
    
    topologically_sorted_commits = sort_graph_topologically(commit_graph)
    
if __name__ == '__main__':
    topo_order_commits()