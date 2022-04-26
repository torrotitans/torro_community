import datetime
from google.cloud import storage
import googleapiclient.discovery
import google
from google.oauth2 import service_account
import base64
import json
def create_key(service_account_email):
    """Creates a key for a service account."""
    try:
        credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])

        service = googleapiclient.discovery.build(
            'iam', 'v1', credentials=credentials)

        key = service.projects().serviceAccounts().keys().create(
            name='projects/-/serviceAccounts/' + service_account_email, body={}
            ).execute()

        # print('Created key: ' + key['name'])
        key_name = key['name']
        private_key_data = key['privateKeyData']
        private_key_decode = base64.b64decode(private_key_data).decode("utf-8")
        private_key_json = json.loads(private_key_decode, strict=False)
        # # print('Created key: ',  key)
    except:
        key_name = None
        private_key_json = {}
    return key_name, private_key_json
def delete_key(full_key_name):
    """Deletes a service account key."""

    credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])

    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)

    service.projects().serviceAccounts().keys().delete(
        name=full_key_name).execute()

    # print('Deleted key: ' + full_key_name)
def generate_download_signed_url_v4(bucket_name, blob_name, sa_name):
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'
    key_name, private_key_json = create_key(sa_name)
    if key_name is None:
        return ''
    credentials = service_account.Credentials.from_service_account_info(
        private_key_json, scopes=['https://www.googleapis.com/auth/cloud-platform'])
    storage_client = storage.Client(credentials=credentials)
    delete_key(key_name)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=30),
        # Allow GET requests using this URL.
        method="GET",
    )

    # print("Generated GET signed URL:")
    # print(url)
    # print("You can use this URL with any user agent, for example:")
    # print("curl '{}'".format(url))
    return url

