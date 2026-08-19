def read_file(file_name=None):
    # If no name is given, ask on the command line (used by main.py).
    # If a name is given, read that file directly (used by the web app).
    if file_name is None:
        file_name = input("Enter the C++ file name: ")
    with open(file_name, "r") as file:
        content = file.read()
    return content


def read_text(content):
    # Passthrough helper for when the code is already available as text
    # (for example, pasted into the web interface).
    return content
