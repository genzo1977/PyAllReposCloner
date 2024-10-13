import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os
import subprocess

# Function to browse for a local directory
def browse_directory():
    folder_selected = filedialog.askdirectory()
    local_dir_entry.delete(0, tk.END)
    local_dir_entry.insert(0, folder_selected)

# Function to download all public repos without confirmation dialogs
def download_repos():
    github_url = github_entry.get().strip()
    local_dir = local_dir_entry.get().strip()

    if not github_url or not local_dir:
        messagebox.showerror("Error", "Both GitHub URL and Local Directory are required!")
        return
    
    if not os.path.isdir(local_dir):
        messagebox.showerror("Error", "Invalid directory selected.")
        return

    username = github_url.split('/')[-1]  # Extract username from the URL

    # GitHub API to get public repos
    api_url = f"https://api.github.com/users/{username}/repos"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for failed requests
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch repos: {e}")
        return

    repos = response.json()

    if not repos:
        messagebox.showinfo("No Repos", "No public repositories found.")
        return

    logArea.insert(tk.END, f"Found {len(repos)} repositories for user {username}\n")
    
    for repo in repos:
        repo_name = repo['name']
        clone_url = repo['clone_url']
        repo_local_path = os.path.join(local_dir, repo_name)
        
        # Run git clone command
        if not os.path.exists(repo_local_path):
            logArea.insert(tk.END, f"Cloning {repo_name}...\n")
            subprocess.run(['git', 'clone', clone_url, repo_local_path], check=True)
        else:
            logArea.insert(tk.END, f"{repo_name} already exists in {local_dir}\n")
    
    logArea.insert(tk.END, "All repositories downloaded.\n")

# Create the main window
root = tk.Tk()
root.title("PyAllReposCloner")

# GitHub Account URL Label and Entry
github_label = tk.Label(root, text="GitHub Account URL:")
github_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

github_entry = tk.Entry(root, width=50)
github_entry.grid(row=0, column=1, padx=10, pady=10)

# Local Directory Label and Entry
local_dir_label = tk.Label(root, text="Local Directory Path:")
local_dir_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

local_dir_entry = tk.Entry(root, width=50)
local_dir_entry.grid(row=1, column=1, padx=10, pady=10)

# Browse Button
browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=1, column=2, padx=10, pady=10)

# Log Area
logArea = tk.Text(root, height=10, width=60)
logArea.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Download Button
download_button = tk.Button(root, text="Download Repos", command=download_repos)
download_button.grid(row=3, column=0, columnspan=3, pady=20)

root.mainloop()
