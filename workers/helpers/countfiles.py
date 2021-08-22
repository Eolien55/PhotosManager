import os

def countfiles(root):
    result = 0
    for _, _, files in os.walk(root):
        result += len(files)
    
    return result