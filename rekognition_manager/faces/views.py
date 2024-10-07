from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadImageForm
from .facerek import FaceRek

# Initialize FaceRek object with collection and bucket settings
rekognition = FaceRek()
rekognition.bucket_name = ''
rekognition.collection_id = ''

def list_faces(request):
    # List all faces in the collection
    faces = rekognition.get_face_collection()
    return render(request, 'faces/list_faces.html', {'faces': faces})

def add_face(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Retrieve the image and face_id from the form
            image = request.FILES['image']
            face_id = request.POST['face_id']
            image_name = image.name

            # Pass the image directly to the add_face_to_collection function
            rekognition.add_face_to_collection(file_path=image, image_name=image_name, face_id=face_id)
            
            return redirect('list_faces')
    else:
        form = UploadImageForm()

    return render(request, 'faces/add_face.html', {'form': form})

def delete_face(request, face_id, user_id):
    # Delete the face from the collection
    rekognition.delete_faces_from_collection([face_id], user_id)
    return redirect('list_faces')
