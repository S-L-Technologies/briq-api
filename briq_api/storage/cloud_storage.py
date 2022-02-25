import os
import json

from .storage import IStorage
# Imports the Google Cloud client library
from google.cloud import storage
from google.cloud.exceptions import NotFound as NotFoundException

import logging
logger = logging.getLogger(__name__)

BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET') or 'test-bucket'

class CloudStorage(IStorage):
    def __init__(self, path="sets/") -> None:
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(BUCKET)
        self.path = path

    def store_json(self, path, data):
        logger.debug("storing JSON at %s", path)
        self.bucket.blob(self.path + path + ".json").upload_from_string(json.dumps(data), content_type='application/json', timeout=10)
        return True

    def load_json(self, path):
        logger.debug("loading JSON from %s", path)
        return json.loads(self.bucket.blob(self.path + path + ".json").download_as_text())

    def has_json(self, path):
        return self.bucket.blob(self.path + path + ".json").exists()

    def list_json(self):
        return [x.name.replace(self.path, "") for x in self.storage_client.list_blobs(self.bucket, prefix=self.path, timeout=5) if ".json" in x.name]

    def iterate_files(self):
        for blob in self.storage_client.list_blobs(self.bucket, prefix=self.path, timeout=5):
            yield blob.name.replace(self.path, "")

    def store_bytes(self, path_including_ext: str, data: bytes):
        logger.debug("Storing data to %s", path_including_ext)
        self.bucket.blob(self.path + path_including_ext).upload_from_string(data, content_type="application/octet-stream", timeout=10)
        return True

    def load_bytes(self, path_including_ext: str):
        logger.debug("Loading data from %s", path_including_ext)
        return self.bucket.blob(self.path + path_including_ext).download_as_bytes()

    def store_image(self, path: str, data: bytes):
        logger.debug("Storing image to %s", path)
        self.bucket.blob(self.path + path + ".png").upload_from_string(data, content_type='image/png', timeout=10)
        return True

    def load_image(self, path: str) -> bytes:
        logger.debug("loading image from %s", path)
        return self.bucket.blob(self.path + path + ".png").download_as_bytes()
