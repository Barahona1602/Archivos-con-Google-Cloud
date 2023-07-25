from google.oauth2 import service_account
from google.cloud import storage
import os
import json

google_credentials = service_account.Credentials.from_service_account_file("app/cloud/key.json")

def backup_cloud():
    # Backup the bucket
    from_cloud_to_json()
    # Load the JSON data from the backup file
    backup_file = "bucket_backup.json"
    with open(backup_file, "r") as file:
        json_data = json.load(file)
    # Restore the backup
    build_files_directories(json_data,"Archivos")
    return f"Backup de cloud a local completado."


def from_cloud_to_json():
    storage_client = storage.Client(credentials=google_credentials)
    bucket = storage_client.get_bucket("iam_project1_bucket")

    prefix = "ARCHIVOS/"  # Specify the desired directory path

    blob_list = list(bucket.list_blobs())
    
    backup_data = {}

    for blob in blob_list:
        if blob.name.startswith(prefix):
            if not blob.name.endswith("/"):  # Directory
                directory_name = blob.name[len(prefix):].rstrip("/")
                # print("Directory name: " + directory_name)
                directory_path_list = [subdir for subdir in blob.name[len(prefix):].split("/") if subdir]
                # print("Directory path: " + str(directory_path_list))
                for dir in directory_path_list:
                    if dir.endswith(".txt"):
                        # print("File found: " + dir)
                        # Remove from list of directories
                        directory_path_list.remove(dir)

                curr_dict = backup_data
                # print("Current dict: " + str(curr_dict))
                for subdir in directory_path_list:
                    if subdir not in curr_dict:
                        curr_dict[subdir] = {}
                    curr_dict = curr_dict[subdir]
                
                if directory_name == "":
                    continue

                curr_dict["_files"] = curr_dict.get("_files", [])  # Create _files key if not present

                # # # Get files within the directory
                sub_blob_list = list(bucket.list_blobs(prefix=blob.name))
                for sub_blob in sub_blob_list:
                    if sub_blob.name.endswith(".txt"):
                        # print("File found: " + sub_blob.name)
                        file_name = sub_blob.name.split("/")[::-1][0]
                        file_contents = sub_blob.download_as_text()

                        # Check if file with same name already exists in _files
                        existing_file = next((f for f in curr_dict["_files"] if f["file_name"] == file_name), None)
                        if existing_file:
                            # File with same name already exists, update its contents
                            existing_file["file_contents"] = file_contents
                        else:
                            # File does not exist, add it to _files
                            curr_dict["_files"].append({"file_name": file_name, "file_contents": file_contents})

    with open("bucket_backup.json", "w") as file:
        json.dump(backup_data, file, indent=4)

    print(f"Backup completed. Backup data saved to bucket_backup.json")
    


def build_files_directories(json_data, base_path="."):
    for key, value in json_data.items():
        if key == "_files":
            # Create files
            for file_data in value:
                file_name = file_data["file_name"]
                file_contents = file_data["file_contents"]
                file_path = os.path.join(base_path, file_name)
                
                # Check if the file already exists
                if os.path.exists(file_path):
                    # Rename the file
                    file_name, file_extension = os.path.splitext(file_name)
                    renamed_file_name = f"{file_name}(1){file_extension}"
                    renamed_file_path = os.path.join(base_path, renamed_file_name)
                    with open(renamed_file_path, "w") as file:
                        file.write(file_contents)
                    print("Renamed and created file:", renamed_file_path)
                else:
                    # Create the file
                    with open(file_path, "w") as file:
                        file.write(file_contents)
                    print("Created file:", file_path)
        else:
            # Create directory
            directory_path = os.path.join(base_path, key)
            
            # Check if the directory already exists
            if os.path.exists(directory_path):
                # Rename the directory
                renamed_directory_path = f"{directory_path}(1)"
                os.makedirs(renamed_directory_path, exist_ok=True)
                print("Renamed and created directory:", renamed_directory_path)
                # Recursively build files and directories within the renamed subdirectory
                build_files_directories(value, base_path=renamed_directory_path)
            else:
                os.makedirs(directory_path, exist_ok=True)
                print("Created directory:", directory_path)
                # Recursively build files and directories within the subdirectory
                build_files_directories(value, base_path=directory_path)


if __name__ == "__main__":
    result = backup_cloud()
