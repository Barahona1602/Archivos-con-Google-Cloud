import os
import json
from google.oauth2 import service_account
from google.cloud import storage


google_credentials = service_account.Credentials.from_service_account_file("app/cloud/key.json")

def backup_local():
    # Specify the base directory
    base_directory = "Archivos"

    # Build JSON from local files and directories
    json_data = build_json_from_files(base_path=base_directory)
    # Save JSON data to a file
    backup_file = "local_backup.json"
    with open(backup_file, "w") as file:
        json.dump(json_data, file, indent=4)

    print("JSON backup completed. Backup data saved to", backup_file)

    # upload the files and directories to the cloud storage
    # Specify the JSON file to read
    json_file = "local_backup.json"

    # Specify the bucket name
    bucket_name = "iam_project1_bucket"

    # Specify the prefix (optional)
    prefix = "ARCHIVOS/"

    # Upload the files and directories to the cloud storage
    upload_files_directories(json_file, bucket_name, prefix=prefix)

    return f"Backup de local a cloud completado."


def upload_files_directories(json_file, bucket_name, prefix=""):
    """Uploads files and directories to a specific directory in a bucket based on the JSON data."""
    storage_client = storage.Client(credentials=google_credentials)
    bucket = storage_client.get_bucket(bucket_name)
    
    with open(json_file, "r") as file:
        json_data = json.load(file)
    
    upload_files_directories_recursive(json_data, bucket, prefix)

def upload_files_directories_recursive(data, bucket, prefix=""):
    """Recursively uploads files and directories to a specific directory in a bucket based on the JSON data."""
    if "_files" in data:
        # Upload files
        for file_data in data["_files"]:
            file_name = file_data["file_name"]
            file_contents = file_data["file_contents"]
            blob_name = prefix + file_name + ".txt"
            
            blob = bucket.blob(blob_name)
            blob.upload_from_string(file_contents)
            print("Uploaded file:", blob.name)
    
    # Upload subdirectories
    for key, value in data.items():
        if key != "_files":
            subdirectory_prefix = prefix + key + "/"
            subdirectory_blob = bucket.blob(subdirectory_prefix)
            subdirectory_blob.upload_from_string("")
            print("Uploaded directory:", subdirectory_blob.name)
            # Recursively upload files and subdirectories within the subdirectory
            upload_files_directories_recursive(value, bucket, prefix=subdirectory_prefix)


def build_json_from_files(base_path="."):
    json_data = {}
    
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        
        if os.path.isfile(item_path):
            # File
            file_name, file_extension = os.path.splitext(item)
            file_contents = ""
            
            with open(item_path, "r") as file:
                file_contents = file.read()
            
            if "_files" not in json_data:
                json_data["_files"] = []
            
            json_data["_files"].append({
                "file_name": file_name,
                "file_contents": file_contents
            })
        
        elif os.path.isdir(item_path):
            # Directory
            sub_json = build_json_from_files(item_path)
            json_data[item] = sub_json
    
    return json_data



if __name__ == "__main__":
    result = backup_local()

