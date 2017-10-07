
# from django.conf import settings
from django.http.response import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from analytics.models import UserFileHistory
# from loginapp.auth import if_authorized
# from loginapp.models import User
from mediafiles.models import MediaFile
from musikhar.abstractions.views import IgnoreCsrfAPIView
from musikhar.utils import err_logger, CONTENT_TYPE_IMAGE, CONTENT_TYPE_AUDIO


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


def create_file_name(params):
    name = ''
    for i in range(len(params)):
        if i == 0 or i == 1:
            continue
        name += params[i]
        if i != len(params) - 1:
            name += '/'
    return name


def get_content_type(request, params):
    try:
        if params[2] == 'avatars':
            file_format = params[-1].split('.')[-1].lower()
            return CONTENT_TYPE_IMAGE.get(file_format)
        elif params[2] == 'banners':
            file_format = params[-1].split('.')[-1].lower()
            return CONTENT_TYPE_IMAGE.get(file_format)
        elif params[4] == 'songs':
            return CONTENT_TYPE_AUDIO
        elif params[4] == 'covers':
            file_format = params[-1].split('.')[-1].lower()
            return CONTENT_TYPE_IMAGE.get(file_format)
    except Exception as e:
        err_logger.info('[MEDIA_CONTENT_TYPE] {} - {} - {} - {}'.format(timezone.now(),
                                                                        request.user,
                                                                        params,
                                                                        str(e))
                        )
        return None


def get_file(request):
    params = request.path.split('/')
    uri = request.path.replace('uploads', 'my_protected_files')
    name = create_file_name(params)
    file_category = params[2]
    response = HttpResponse()

    content_type = get_content_type(request=request, params=params)
    if not content_type:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

    if file_category == 'avatars':
        response['Content-Type'] = content_type
        response['X-Accel-Redirect'] = uri
        return response

    if file_category == 'banners':
        response['Content-Type'] = content_type
        response['X-Accel-Redirect'] = uri
        return response

    # elif file_category == 'posts':
    #     target_username = params[3]
    #
    #     if target_username == settings.SYSTEM_USER['username']:
    #         UserFileHistory.objects.create(requested_user=request.user,
    #                                        file_path=name)
    #         response['Content-Type'] = content_type
    #         response['X-Accel-Redirect'] = uri
    #         return response
    #     elif request.user.is_authenticated():
    #         if target_username == request.user.username:
    #             UserFileHistory.objects.create(requested_user=request.user,
    #                                            owner_user=request.user,
    #                                            file_path=name)
    #             response['Content-Type'] = content_type
    #             response['X-Accel-Redirect'] = uri
    #             return response
    #         else:
    #             try:
    #                 target_user = User.objects.get(username=target_username)
    #             except User.DoesNotExist:
    #                 response.status_code = status.HTTP_404_NOT_FOUND
    #                 return response
    #
    #             if request.user.is_follower(target_user):
    #                 UserFileHistory.objects.create(requested_user=request.user,
    #                                                owner_user=target_user,
    #                                                file_path=name)
    #                 response['Content-Type'] = content_type
    #                 response['X-Accel-Redirect'] = uri
    #                 return response
    #             else:
    #                 response.status_code = status.HTTP_401_UNAUTHORIZED
    #                 return response
    #     else:
    #         try:
    #             target_user = User.objects.get(username=target_username)
    #         except User.DoesNotExist:
    #             response.status_code = status.HTTP_404_NOT_FOUND
    #             return response
    #
    #         if target_user.is_public:
    #             UserFileHistory.objects.create(owner_user=target_user,
    #                                            file_path=name)
    #             response['Content-Type'] = content_type
    #             response['X-Accel-Redirect'] = uri
    #             return response
    #         else:
    #             response.status_code = status.HTTP_401_UNAUTHORIZED
    #             return response

    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
