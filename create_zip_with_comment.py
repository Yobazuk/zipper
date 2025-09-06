import json
import zipfile

# JSON document to embed in a file comment
json_comment = {
    "name": "example",
    "version": "1",
    "description": "This is a JSON document stored in a file comment."
}

# Encode JSON as bytes
comment_bytes = json.dumps(json_comment, indent=2).encode("utf-8")

# Create the zip file
with zipfile.ZipFile("example.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    # First file (with comment)
    info1 = zipfile.ZipInfo("file_with_comment.txt")
    info1.comment = comment_bytes  # attach JSON as comment
    zf.writestr(info1, "This file has a JSON comment attached.")

    # Second file (no comment)
    zf.writestr("plain_file.txt", "This is just a normal file.")

print("Created example.zip with two files. One file has a JSON comment.")