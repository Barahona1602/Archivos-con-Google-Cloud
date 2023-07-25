import sys
from google.oauth2 import service_account
# [START storage_create_bucket]
from google.cloud import storage

google_credentials = service_account.Credentials.from_service_account_file("app/cloud/key.json")


def create_bucket(bucket_name):
    """Creates a new bucket."""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client(credentials=google_credentials)

    bucket = storage_client.create_bucket(bucket_name)

    print(f"Bucket {bucket.name} created")


# [END storage_create_bucket]

if __name__ == "__main__":
    create_bucket(bucket_name="iam_project1_bucket")