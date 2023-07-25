from google.oauth2 import service_account
from google.cloud import storage
from google.api_core.exceptions import NotFound

google_credentials = service_account.Credentials.from_service_account_file("app/cloud/key.json")


def rename_cloud(blob_name, new_name):
    """Renames a file in Google Cloud Storage."""
    storage_client = storage.Client(credentials=google_credentials)

    bucket = storage_client.bucket("iam_project1_bucket")

    path_name = "ARCHIVOS"  + blob_name
    try:
        blob = bucket.blob(path_name)
        if blob.exists():
            # remove the name from the path
            new_ = path_name.split("/")[:-1]
            directory = "/".join(new_)
            # get the blobs of the directory
            blobs = list(bucket.list_blobs(prefix=directory))
            # check if the new name already exists
            for blob in blobs:
                if blob.name[len(directory):] ==  "/" + new_name:
                  print(blob.name[len(directory):], "/" + new_name)
                  print(f"File {new_name} already exists.")
                  return f"El archivo {new_name} ya existe."
                
            # add the new name to the path
            new_.append(new_name)
            # join the path
            new_ = "/".join(new_)
            new_blob = bucket.rename_blob(blob, new_)

            print(f"File {path_name} renamed to {new_}.")
            return f"Archivo {path_name} renombrado a {new_}."
        else:
            print(f"File {path_name} does not exist.")
            return f"El archivo {path_name} no existe."
    except NotFound:
        print(f"File {path_name} does not exist.")
        return f"El archivo {path_name} no existe."


if __name__ == "__main__":
  rename_cloud(
      blob_name="/carpeta 2/exampleSub2(1).txt",
      new_name="alvaro1.txt",
  )
