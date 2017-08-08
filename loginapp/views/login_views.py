from django.http.response import HttpResponse

from loginapp.auth import if_authorized


@if_authorized
def test_view(request):
    print(request.user)
    return HttpResponse(content='OK')



