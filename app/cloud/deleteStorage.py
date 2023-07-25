import sys
from google.oauth2 import service_account
from google.cloud import storage

google_credentials = service_account.Credentials.from_service_account_file("app/cloud/key.json")


def delete_cloud(blob_name,name):
  """Deletes a blob or directory from the bucket."""
  storage_client = storage.Client(credentials=google_credentials)
  bucket = storage_client.bucket("iam_project1_bucket")
  
  if name == "not coming":
    name = ""

  set_blob_name = "ARCHIVOS" + blob_name + name

  blob = bucket.blob(set_blob_name)

  if set_blob_name.endswith("/"):
      # Directory deletion
      blobs = list(bucket.list_blobs(prefix=set_blob_name))  # Convert the iterator to a list

      if not blobs:
          print(f"Directory {set_blob_name} does not exist.")
          return f"El directorio {set_blob_name} no existe."

      for blob in blobs:
          blob.delete()
      print(f"Directory {set_blob_name} deleted.")
      return f"Directorio {set_blob_name} eliminado."
  else:
      # Single blob deletion
      if not blob.exists():
          print(f"Blob {set_blob_name} does not exist.")
          return f"El archivo {set_blob_name} no existe."

      blob.delete()
      print(f"Blob {set_blob_name} deleted.")
      return f"Archivo {set_blob_name} eliminado."



if __name__ == "__main__":
  delete_cloud(blob_name="/carpeta3/", name="not coming") # delete the directory
  delete_cloud(blob_name="/carpeta 2/", name="prueba 2.txt") # delete the file
