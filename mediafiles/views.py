import json
# from django.conf import settings
from django.http.response import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from analytics.models import UserFileHistory
# from loginapp.auth import if_authorized
# from loginapp.models import User
from karaoke.models import Post
from loginapp.models import Token
from mediafiles.models import MediaFile
from musikhar.abstractions.views import IgnoreCsrfAPIView
from musikhar.utils import err_logger, CONTENT_TYPE_IMAGE, CONTENT_TYPE_AUDIO, app_logger, CONTENT_TYPE_TEXT


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
        if params[2] == 'avatars' or params[2] == 'default_icons':
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
        elif params[2] == 'async_files':
            return CONTENT_TYPE_TEXT
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
    # name = create_file_name(params)
    file_category = params[2]
    response = HttpResponse()

    content_type = get_content_type(request=request, params=params)
    if not content_type:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

    if file_category == 'async_files':
        if request.user.is_staff or request.user.is_superuser:
            response['Content-Type'] = content_type
            response['X-Accel-Redirect'] = uri
            return response
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return response

    if file_category == 'default_icons':
        response['Content-Type'] = content_type
        response['X-Accel-Redirect'] = uri
        return response

    if file_category == 'avatars':
        response['Content-Type'] = content_type
        response['X-Accel-Redirect'] = uri
        return response

    if file_category == 'banners':
        response['Content-Type'] = content_type
        response['X-Accel-Redirect'] = uri
        return response

    elif file_category == 'posts':
        if params[4] == 'covers':
            response['Content-Type'] = content_type
            response['X-Accel-Redirect'] = uri
            return response
        else:
            parameters = request.GET
            if not parameters:
                response.status_code = status.HTTP_403_FORBIDDEN
                return response
            post_id = parameters.get('post')
            if not post_id:
                response.status_code = status.HTTP_403_FORBIDDEN
                return response
            try:
                post = Post.objects.get(id=int(post_id))
            except Post.DoesNotExist:
                response.status_code = status.HTTP_403_FORBIDDEN
                return response

            if post.user_has_access(user=request.user):
                response['Content-Type'] = content_type
                response['X-Accel-Redirect'] = uri
                return response

    response.status_code = status.HTTP_404_NOT_FOUND
    return response


class Webhook(IgnoreCsrfAPIView):
    def post(self, request):
        try:
            app_logger.info('[WEBHOOK] method: {}, GET: {}'.format(request.method, request.GET))
        except Exception as e:
            app_logger.info('[WEBHOOK] method part, {}'.format(str(e)))

        try:
            app_logger.info('[WEBHOOK] headers {}'.format(request.META))
        except Exception as e:
            app_logger.info('[WEBHOOK] headers part, {}'.format(str(e)))

        try:
            app_logger.info('[WEBHOOK] COOKIES {}'.format(request.COOKIES))
        except Exception as e:
            app_logger.info('[WEBHOOK] COOKIES part, {}'.format(str(e)))

        try:
            app_logger.info('[WEBHOOK] user {}'.format(request.user))
        except Exception as e:
            app_logger.info('[WEBHOOK] user part, {}'.format(str(e)))

        try:
            app_logger.info('[WEBHOOK] body {}'.format(request.body))
        except Exception as e:
            app_logger.info('[WEBHOOK] body part, {}'.format(str(e)))

        return HttpResponse(status=403)
        # return Response({'accept': 'true'})
        data = json.loads(request.body.decode('utf-8'))

        target_file = data.get('resource')
        if not target_file:
            app_logger.info('[WEBHOOK] 403 for target_file  , {}'.format(target_file))
            return HttpResponse(status=403)

        headers = data.get('headers')
        if not headers:
            app_logger.info('[WEBHOOK] 403 for not header')
            return HttpResponse(status=403)

        token = headers.get('Y-Storage-usertoken')
        if not token:
            app_logger.info('[WEBHOOK] 403 for not token')
            return HttpResponse(status=403)

        try:
            user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            app_logger.info('[WEBHOOK] 403 for no user  , token {}'.format(token))
            return HttpResponse(status=403)

        params = target_file.split('/')
        # name = create_file_name(params)
        file_category = params[2]
        response = HttpResponse()
        app_logger.info('[WEBHOOK] UPDATE , file_category {}'.format(file_category))
        content_type = get_content_type(request=request, params=params)
        app_logger.info('[WEBHOOK] UPDATE for content type  , content_type: {}'.format(content_type))
        app_logger.info('[WEBHOOK] UPDATE for params  , params: {}'.format(params))
        if not content_type:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return response

        if file_category == 'avatars':
            return Response({'accept': True})

        if file_category == 'banners':
            return Response({'accept': True})

        elif file_category == 'posts':
            if params[4] == 'covers':
                return Response({'accept': True})
            else:
                parameters = data.get('parameters')
                if not parameters:
                    response.status_code = status.HTTP_403_FORBIDDEN
                    return response
                post_id = parameters.get('post')
                if not post_id:
                    response.status_code = status.HTTP_403_FORBIDDEN
                    return response
                try:
                    post = Post.objects.get(id=int(post_id))
                except Post.DoesNotExist:
                    response.status_code = status.HTTP_403_FORBIDDEN
                    return response

                if post.user_has_access(user=user):
                    return Response({'accept': True})

        response.status_code = status.HTTP_403_FORBIDDEN
        return response

@csrf_exempt
def webhook(request):
    try:
        app_logger.info('[WEBHOOK] method: {}, GET: {}, POST: {}'.format(request.method, request.GET, request.POST))
    except Exception as e:
        app_logger.info('[WEBHOOK] method part, {}'.format(str(e)))

    try:
        app_logger.info('[WEBHOOK] headers {}'.format(request.META))
    except Exception as e:
        app_logger.info('[WEBHOOK] headers part, {}'.format(str(e)))

    try:
        app_logger.info('[WEBHOOK] COOKIES {}'.format(request.COOKIES))
    except Exception as e:
        app_logger.info('[WEBHOOK] COOKIES part, {}'.format(str(e)))

    try:
        app_logger.info('[WEBHOOK] user {}'.format(request.user))
    except Exception as e:
        app_logger.info('[WEBHOOK] user part, {}'.format(str(e)))

    try:
        app_logger.info('[WEBHOOK] body {}'.format(request.body))
    except Exception as e:
        app_logger.info('[WEBHOOK] body part, {}'.format(str(e)))

    data = json.loads(request.body.decode('utf-8'))

    target_file = data.get('resource')
    if not target_file:
        return HttpResponse(status=403)

    headers = data.get('headers')
    if not headers:
        return HttpResponse(status=403)

    token = headers.get('Y-Storage-usertoken')
    if not token:
        return HttpResponse(status=403)

    try:
        user = Token.objects.get(key=token).user
    except Token.DoesNotExist:
        return HttpResponse(status=403)

    params = target_file.split('/')
    # name = create_file_name(params)
    file_category = params[2]
    response = HttpResponse()

    content_type = get_content_type(request=request, params=params)
    if not content_type:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response

    if file_category == 'avatars':
        response.content = json.dumps({'accept': 'true'})
        return response

    if file_category == 'banners':
        response.content = json.dumps({'accept': 'true'})
        return response

    elif file_category == 'posts':
        if params[4] == 'covers':
            response.content = json.dumps({'accept': 'true'})
            return response
        else:
            parameters = data.get('parameters')
            if not parameters:
                response.status_code = status.HTTP_403_FORBIDDEN
                return response
            post_id = parameters.get('post')
            if not post_id:
                response.status_code = status.HTTP_403_FORBIDDEN
                return response
            try:
                post = Post.objects.get(id=int(post_id))
            except Post.DoesNotExist:
                response.status_code = status.HTTP_403_FORBIDDEN
                return response

            if post.user_has_access(user=user):
                response.content = json.dumps({'accept': 'true'})
                return response

    response.status_code = status.HTTP_403_FORBIDDEN
    return response



