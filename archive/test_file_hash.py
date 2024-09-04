import hashlib

def calculate_md5(file_path):
    """
    Calculates the MD5 hash of a file.

    Args:
        file_path (str): The file path of the file.

    Returns:
        str: The MD5 hash of the file.
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Usage
print(calculate_md5("/Users/tis/Movies/test.mkv"))