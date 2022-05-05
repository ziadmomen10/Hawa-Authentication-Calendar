import re
from rest_framework.response import Response
from rest_framework import status

from .models import User, Period
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import PeriodDateSerializer, RegisterSerilaziers, UserSerializer


# class Register(APIView):
#     """
#     Create user with post request with data

#     """

#     def post(self, request, format=None):

#         serializer = RegisterSerilaziers(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({"Success": "Account Created Succuffuly"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    """
    clear refresh token from JWT and move it to blacklist
    """
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"Logout Success"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response({"Logout Failed"}, status=status.HTTP_400_BAD_REQUEST)

class PeriodView(APIView):
    permission_classes = [IsAuthenticated]
    serialiazer_class = PeriodDateSerializer
    querset = Period.objects.all()

    def get(self, request, format=None):
        serilaizer = self.serialiazer_class(self.querset, many=True)
        return Response(serilaizer.data)


    def post(self, request, format=None):
        try:
            data = request.data
            serilaizer = self.serialiazer_class(data=data, context={"request": request})
            if serilaizer.is_valid():
                serilaizer.save()
                return Response(serilaizer.data)
            return Response({"error": serilaizer.error_messages})
        except Exception as e:
            print("eeeeeeeeeror", e) 



# class UserMe(APIView):
#     permission_classes = [IsAuthenticated]
#     serializar_class = UserSerializer


#     def get(self,request,format=None):
#         user = request.user
#         queryset = User.objects.get(username=user.username)
#         serializer = self.serializar_class(queryset, context={"request": request})
#         return Response({"user": serializer.data})