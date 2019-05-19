#Installed packages
from rest_framework import status ,decorators, response, permissions
from knox.auth import TokenAuthentication
#Local packages
from client_auth.serializers import  AccountSerializer


current_format = None


@decorators.api_view(['GET'])
def api_root(request, format=current_format, *args, **kwargs):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    if request.user.is_authenticated:
        data = {'ooh': 'your alive',
                'user': AccountSerializer(request.user).data}
    else:
        data = {'error': 'You saw this. You Killed It'}
    return response.Response(data, status=status.HTTP_200_OK, *args, **kwargs)


