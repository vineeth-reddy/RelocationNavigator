import pandas as pd
import os
from io import BytesIO
from google.cloud import storage
from google.oauth2 import service_account

class GCPUtils:
    def __init__(self):
        self.credentials = self.get_credentials()

    def read_data_from_gcs(self, file, bucket_name):
        print(f"Reading data from GCS.....")
        client = storage.Client.from_service_account_info(self.credentials)
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(file)
        csv_data = blob.download_as_text()
        dataframe = pd.read_csv(BytesIO(csv_data.encode()))
        print(f"Finished reading data from {file} in bucket {bucket_name}")
        return dataframe

    def save_data_to_gcs(self, dataframe, bucket_name, file_path):
        print(f"Writing data to GCS.....")
        client = storage.Client.from_service_account_info(self.credentials)
        csv_data = dataframe.to_csv(index=False)
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(file_path)
        blob.upload_from_string(csv_data, content_type='text/csv')
        print(f"Finished writing data to {file_path} in bucket {bucket_name}.")

    @staticmethod
    def get_credentials():
        creds_info = {
            "type": "service_account",
            "project_id": os.getenv("GOOGLE_PROJECT_ID", "your_project_id"),
            "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID", "your_private_key_id"),
            "private_key": os.getenv("GOOGLE_PRIVATE_KEY", "your_private_key").replace('\\n', '\n'),
            "client_email": os.getenv("GOOGLE_CLIENT_EMAIL", "your_client_email"),
            "client_id": os.getenv("GOOGLE_CLIENT_ID", "your_client_id"),
            "auth_uri": os.getenv("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
            "token_uri": os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
            "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
            "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL", "your_client_x509_cert_url"),
            "universe_domain": os.getenv("GOOGLE_UNIVERSE_DOMAIN", "googleapis.com")
        }
        return creds_info

        