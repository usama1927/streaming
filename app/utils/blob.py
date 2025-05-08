import os
import uuid
from azure.storage.blob import BlobServiceClient

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER)

def upload_to_blob(file_stream, original_filename: str) -> str:
    ext = original_filename.split(".")[-1]
    blob_name = f"{uuid.uuid4()}.{ext}"
    blob_client = container_client.get_blob_client(blob=blob_name)
    blob_client.upload_blob(file_stream, overwrite=True)

    # Public blob URL
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_STORAGE_CONTAINER}/{blob_name}"
