from google.oauth2 import service_account
from google.cloud import storage
from google.api_core.exceptions import NotFound

google_credentials = service_account.Credentials.from_service_account_file("app/cloud/key.json")


def modify_cloud(blob_name, new_content):
    """Modifies the content of a file in Google Cloud Storage."""
    storage_client = storage.Client(credentials=google_credentials)

    bucket = storage_client.bucket("iam_project1_bucket")

    path_name = "ARCHIVOS" + blob_name
    try:
        blob = bucket.blob(path_name)
        if blob.exists():
            blob.upload_from_string(new_content)
            print(f"Content of file {path_name} modified successfully.")
            return f"Contenido del archivo {path_name} modificado correctamente."
        else:
            print(f"File {path_name} does not exist.")
            return f"El archivo {path_name} no existe."
    except NotFound:
        print(f"File or Directory {path_name} does not exist.")
        return f"El archivo o directorio {path_name} no existe."



if __name__ == "__main__":
    modify_cloud(
        blob_name="ARCHIVOS/carpeta3/example.txt",
        new_content="This is the modified content of the file.",
    )
