from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from loginapp.auth import if_authorized
from loginapp.models import User
from mediafiles.models import MediaFile
from musikhar.abstractions.views import IgnoreCsrfAPIView


# .media_type: multipart/form-data
class UploadMediaFile(IgnoreCsrfAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, type, format=None):
        if MediaFile.type_is_valid(type=type):
            try:
                my_file = request.FILES["file"]
                media_file = MediaFile.objects.create(user=request.user,
                                                      type=type)
                media_file.file = my_file
                media_file.save()
                return Response(status=status.HTTP_201_CREATED, data={'upload_id': media_file.id})
            except:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)


@if_authorized
def get_file(request):
    params = request.path.split('/')
    uri = request.path.replace('uploads', 'my_protected_files')
    file_category = params[2]
    response = HttpResponse()

    if file_category == 'avatars':
        response['X-Accel-Redirect'] = uri
        return response

    elif file_category == 'posts':
        target_username = params[3]

        if target_username == settings.SYSTEM_USER['username']:
            response['X-Accel-Redirect'] = uri
            return response
        elif target_username == request.user.username:
            response['X-Accel-Redirect'] = uri
            return response
        else:
            try:
                target_user = User.objects.get(username=target_username)
            except User.DoesNotExist:
                response.status_code = status.HTTP_404_NOT_FOUND
                return response

            if request.user.is_follower(target_user):
                response['X-Accel-Redirect'] = uri
                return response
            else:
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return response
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response

    # print(params)
    # print(request.path)
    # print(request.path_info)
    # print(request.get_full_path())
    # return HttpResponse(status=status.HTTP_200_OK)
