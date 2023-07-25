from google.oauth2 import service_account
from google.cloud import storage

google_credentials = service_account.Credentials.from_service_account_file("app/cloud/key.json")

def create_cloud(file_data, destination_blob_name, name):
  """Uploads file data to the bucket."""
  storage_client = storage.Client(credentials=google_credentials)
  bucket = storage_client.bucket("iam_project1_bucket")
  path_name = "ARCHIVOS" + destination_blob_name + name
  blob = bucket.blob(path_name)

  # CHECK IF THE FILE ALREADY EXISTS
  if blob.exists():
    print(f"File {path_name} already exists.")
    return f"El archivo {path_name} ya existe."

  blob.upload_from_string(file_data)

  print(f"File data uploaded to {path_name}.")
  return f"Archivo {path_name} subido correctamente."


if __name__ == "__main__":
  file_data = '''This is the content of the text file.
  It can have multiple lines and contain any text data.
  '''

  create_cloud(
      file_data=file_data,
      destination_blob_name="/",
      name ="root.txt",
  )
#  create_cloud(bucket_name="iam_project1_bucket", file_data=body, destination_blob_name=f"ARCHIVOS{path[:-1]}{name}")

