import re

def sanitize_username(name):
    # Remove non-alphanumeric characters and underscores
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    
    # Convert to lowercase
    name = name.lower()
    
    # Limit the username to a maximum of 64 characters
    name = name[:64]
    
    return name
