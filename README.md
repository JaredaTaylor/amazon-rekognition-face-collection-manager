# amazon-rekognition-face-collection-manager
Simple python based web UI for managing a face collection in Amazon Rekognition
EXAMPLE ONLY, NOT FOR USE IN PRODUCTION

## Requirements
- Python3
- Django
- Boto3

## Execution
1. Update rekognition bucket name and face collection IDs in views.py
   ```
   rekognition.bucket_name = 'someS3Bucket'
   rekognition.collection_id = 'someFaceCollection'
   ```
2. from repository directory
   ```
   python manage.py migrate
   python manage.py runserver
   ```
3. Navigate to `http://127.0.0.1:8000/faces/`
