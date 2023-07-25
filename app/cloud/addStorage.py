from google.oauth2 import service_account
from google.cloud import storage
from google.api_core.exceptions import NotFound

google_credentials = service_account.Credentials.from_service_account_file("app/cloud/key.json")


def add_cloud(blob_name, additional_content):
  """Appends additional content to the current content of a file in Google Cloud Storage."""
  storage_client = storage.Client(credentials=google_credentials)

  bucket = storage_client.bucket("iam_project1_bucket")

  path_name = "ARCHIVOS" + blob_name
  try:
      blob = bucket.blob(path_name)
      if blob.exists():
          current_content = blob.download_as_text()
          new_content = current_content + additional_content
          blob.upload_from_string(new_content)
          print(f"Additional content added to file {path_name} successfully.")
          return f"Contenido adicional agregado al archivo {path_name} correctamente."
      else:
          print(f"File {path_name} does not exist.")
          return f"El archivo {path_name} no existe."
  except NotFound:
      print(f"File {path_name} does not exist.")
      return f"El archivo {path_name} no existe."


if __name__ == "__main__":
  add_cloud(
    blob_name="/carpeta3/example3.txt",
    additional_content="\nThis is the additional content.",
  )
