from google.oauth2 import service_account
from google.cloud import storage
from google.api_core.exceptions import NotFound

google_credentials = service_account.Credentials.from_service_account_file("app/cloud/key.json")


def transfer_cloud(blob_name, destination_blob_name):
    """Moves a blob from one bucket to another with a new name, and deletes the source blob."""
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
            
            # Check if the blobs of the destination already exist - add (1) to the name or 
            list_names_exist = []
            for blob in blobs_destination:
                if blob.name[len(path_destination):] in [blob.name[len(path_name):] for blob in blobs]:
                    # append the name to the list
                    list_names_exist.append(blob.name[len(path_destination):])
                    # print(f"File {blob.name[len(destination_blob_name):]} already exists in {destination_blob_name}")

            for blob in blobs:
                if blob.name[len(path_name):] in list_names_exist:
                    # change the name add (1)
                    destination = path_destination + str(blob.name[len(path_name):].replace(".txt", "(1).txt"))
                    source_blob = source_bucket.blob(blob.name)
                    destination_blob = destination_bucket.blob(destination)
                    destination_blob.rewrite(source_blob)   

                # Move the blob to the destination
                destination = path_destination + str(blob.name[len(path_name):])
                source_blob = source_bucket.blob(blob.name)
                destination_blob = destination_bucket.blob(destination)
                destination_blob.rewrite(source_blob)

                # Delete the source blob
                source_blob.delete()

            print("Files moved successfully.")
            return f"Archivos de {path_name} movidos correctamente."
        else:
            # CHECK IF THE DESTINATION DIRECTORY EXISTS
            blobs = list(destination_bucket.list_blobs(prefix=path_destination))
            if not blobs:
                print(f"Directory {path_destination} does not exist.")
                return f"El directorio {path_destination} no existe."
            # Check if the blobs of the destination already exist
            for blob in blobs:
                if blob.name[len(path_destination):] == path_name.split("/")[::-1][0]:
                    # change the name add (1)
                    destination = path_destination + str(path_name.split("/")[::-1][0].replace(".txt", "(1).txt"))
                    source_blob = source_bucket.blob(path_name)
                    destination_blob = destination_bucket.blob(destination)
                    destination_blob.rewrite(source_blob)


            destination = destination_blob_name + str(path_name.split("/")[::-1][0])
            source_blob = source_bucket.blob(path_name)
            destination_blob = destination_bucket.blob(destination)
            destination_blob.rewrite(source_blob)

            # Delete the source blob
            source_blob.delete()

            print(
                "Blob {} moved to blob {} ".format(
                    source_blob.name,
                    destination_blob.name,
                )
            )
            return f"Archivo {source_blob.name} movido a {destination_blob.name} correctamente."
    except NotFound:
        print(f"Blob or directory {path_name} does not exist. Error: {NotFound}")
        return f"El archivo o directorio {path_name} no existe. Error: {NotFound}"


if __name__ == "__main__":
    transfer_cloud(
      blob_name="/carpeta5/",
      destination_blob_name="/carpeta 2/",
    )