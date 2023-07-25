from google.oauth2 import service_account
from google.cloud import storage
from google.api_core.exceptions import NotFound

google_credentials = service_account.Credentials.from_service_account_file("app/cloud/key.json")


def copy_cloud(blob_name, destination_blob_name):
    """Copies a blob from one bucket to another with a new name."""
    storage_client = storage.Client(credentials=google_credentials)

    source_bucket = storage_client.bucket("iam_project1_bucket")
    destination_bucket = storage_client.bucket("iam_project1_bucket")

    path_name = "ARCHIVOS" + blob_name 
    path_destination = "ARCHIVOS" + destination_blob_name
    try:
        if path_name.endswith("/"):
            # CHECK IF THE ORIGIN DIRECTORY EXISTS
            blobs = list(source_bucket.list_blobs(prefix=path_name))
            if not blobs:
                print(f"Directory {path_name} does not exist or does not contain any files.")
                return f"El directorio {path_name} no existe."
            
            # CHECK IF THE DESTINATION DIRECTORY EXISTS
            blobs_destination = list(destination_bucket.list_blobs(prefix=path_destination))
            if not blobs_destination:
                print(f"Directory {path_destination} does not exist.")
                return f"El directorio {path_destination} no existe."
            
            # Check if the blobs of the destination already exist
            for blob in blobs_destination:
                if blob.name[len(path_destination):] in [blob.name[len(path_name):] for blob in blobs]:
                    print(f"File {blob.name[len(path_destination):]} already exists in {path_destination}")
                    return f"El archivo {blob.name[len(path_destination):]} ya existe en {path_destination}"

            for blob in blobs:
                # Copy the blob to the destination
                destination = path_destination + str(blob.name[len(path_name):])
                source_blob = source_bucket.blob(blob.name)
                destination_blob = destination_bucket.blob(destination)
                destination_blob.rewrite(source_blob)

            print("Files copied successfully.")
            return f"Archivos de {path_name} copiados correctamente."
        
        else:
            # CHECK IF THE DESTINATION DIRECTORY EXISTS
            blobs = list(destination_bucket.list_blobs(prefix=path_destination))
            if not blobs:
                print(f"Directory {path_destination} does not exist.")
                return f"El directorio {path_destination} no existe."
            
            # Check if the blobs of the destination already exist
            for blob in blobs:
                if blob.name[len(path_destination):] == blob_name.split("/")[::-1][0]:
                    print(f"File {blob_name.split('/')[::-1][0]} already exists in {path_destination}")
                    return f"El archivo {blob_name.split('/')[::-1][0]} ya existe en {path_destination}"
                

            destination = path_destination + str(path_name.split("/")[::-1][0])
            source_blob = source_bucket.blob(path_name)
            destination_blob = destination_bucket.blob(destination)
            destination_blob.rewrite(source_blob)
            print(
                "Blob {} copied to blob {} ".format(
                    source_blob.name,
                    destination_blob.name,
                )
            )
            return f"Archivo {path_name} copiado correctamente."
    except NotFound:
        print(f"Blob or directory {path_name} does not exist.")
        return f"El archivo o directorio {path_name} no existe."



if __name__ == "__main__":
    copy_cloud(
        blob_name="/carpeta1/",
        destination_blob_name="/carpeta 2/",
    )

