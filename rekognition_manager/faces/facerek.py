import boto3
from botocore.exceptions import ClientError

class Face():
    def __init__(self, face_id, ext_image_id, confidence, image_url):
        self.face_id = face_id
        self.ext_image_id = ext_image_id
        self.confidence = confidence
        self.image_url = image_url

class FaceRek():
    def __init__(self):
        self.rekognition = boto3.client('rekognition')
        self.s3 = boto3.client('s3')
        self.bucket_name = ''
        self.collection_id = ''

    def create_face_collection(self, collection_id: str):
        response = self.rekognition.create_collection(CollectionId=collection_id)

        if response['StatusCode'] == 200:
            self.collection_id = collection_id
            print(f'Collection {collection_id} successfully created.')
        else:
            print(f'Failed to create collection {collection_id}.')

    def delete_face_collection(self, collection_id: str):
        response = self.rekognition.delete_collection(CollectionId=collection_id)

        if response['StatusCode'] == 200:
            print(f'Collection {collection_id} successfully deleted.')
        else:
            print(f'Failed to delete collection {collection_id}.')

    '''
    Uploads image to S3 storage for usage with AR
    '''
    def upload_image_to_s3(self, file_path: str, image_name: str):
        # self.s3.upload_file(file_path, self.bucket_name, image_name)

        # TODO: Need handling for upload_file responses
        try:
            response = self.s3.upload_file(file_path, self.bucket_name, image_name)
            # if response['StatusCode'] == 200:
            #     print(f'File {file_path} uploaded to {self.bucket_name}/{image_name}.')
            # else:
            #     print(f'Failed to upload file to S3.')

            # return {'bucket_name': self.bucket_name, 'image_name': image_name}
            print(f'File {file_path} uploaded to {self.bucket_name}/{image_name}.')
        except ClientError as e:
            print(f'Could not upload file to S3: {str(e)}')

    '''
    Stores image in S3 then uses image to add face to collection for AR
    '''
    def add_face_to_collection(self, file_path, image_name: str, face_id: str):
        # Upload the image to S3 (file_path is the file-like object)
        try:
            self.s3.upload_fileobj(file_path, self.bucket_name, face_id)
            print(f'File uploaded to S3 as {self.bucket_name}/{face_id}')
        except ClientError as e:
            print(f'Could not upload file to S3: {str(e)}')
            return

        # Index the image as a face in the Rekognition collection
        response = self.rekognition.index_faces(
            CollectionId=self.collection_id,
            Image={'S3Object': {'Bucket': self.bucket_name, 'Name': face_id}},
            ExternalImageId=face_id,
            MaxFaces=1,
            QualityFilter='AUTO'
        )

        print(f'New face with ID {face_id} has been added to the collection {self.collection_id}.')
        return response['FaceRecords'][0]['Face']['FaceId']

    '''
    Lists faces stored in face collection for AR
    '''
    def list_faces_in_collection(self):
        response = self.rekognition.list_faces(CollectionId=self.collection_id)

        # if response['StatusCode'] == 200:
        print('Indexed Faces:')
        if len(response['Faces']) == 0:
            print(f'No faces in collection.')
        for face in response['Faces']:
            print(f'FaceId: {face["FaceId"]}')
            print(f'ExternalImageId: {face["ExternalImageId"]}')
            print(f'Confidence: {face["Confidence"]}\n')
        # else:
        #     print(f'Could not get list of faces.')

    '''
    Lists faces stored in face collection for AR
    '''
    def get_face_collection(self):
        response = self.rekognition.list_faces(CollectionId=self.collection_id)

        faces = []
        # if response['StatusCode'] == 200:
        print('Indexed Faces:')
        if len(response['Faces']) == 0:
            print(f'No faces in collection.')
        for face in response['Faces']:
            img_url = f'https://{self.bucket_name}.s3.amazonaws.com/{face["ExternalImageId"]}'
            new_face = Face(face_id=face["FaceId"], ext_image_id=face["ExternalImageId"], confidence=face["Confidence"], image_url=img_url)
            faces.append(new_face)

        return faces
        # else:
        #     print(f'Could not get list of faces.')

    '''
    Removes index from face collection for AR
    '''
    def delete_faces_from_collection(self, face_ids: list[str]):
        response = self.rekognition.delete_faces(CollectionId=self.collection_id, FaceIds=face_ids)

        print(f'Deleted FaceId(s): {response["DeletedFaces"]}')
        # if response['StatusCode'] == 200:
        #     print(f'Deleted FaceId(s): {response["DeletedFaces"]}')
        # else:
        #     print(f'Could not delete FaceId(s).')

    '''
    Searches for collection faces in image
    '''
    def search_for_faces_in_image(self, file_path: str, image_name: str):
        # Upload image to search in S3
        self.upload_image_to_s3(file_path=file_path, image_name=image_name)

        # Search image
        response = self.rekognition.search_faces_by_image(
            CollectionId=self.collection_id,
            Image={'S3Object': {'Bucket': self.bucket_name, 'Name': image_name}},
            # MaxFaces=5,
            FaceMatchThreshold=90
        )

        face_matches = response['FaceMatches']
        # print(str(response))
        if len(face_matches) >= 1:
            print(f'{len(face_matches)} matches found in image.')
            for match in face_matches:
                print(f'FaceId: {match["Face"]["FaceId"]}')
                print(f'FaceId: {match["Face"]["ExternalImageId"]}')
                print(f'Confidence: {match["Face"]["Confidence"]}\n')
        else:
            print(f'No matches found.')

        # if response['StatusCode'] == 200:
        #     face_matches = response['FaceMatches']
        #     if len(face_matches) >= 1:
        #         print(f'{len()} matches found in image.')
        #         for match in face_matches:
        #             print(f'FaceId: {match["FaceId"]}')
        #             print(f'Confidence: {match["Confidence"]}\n')
        #     else:
        #         print(f'No matches found.')