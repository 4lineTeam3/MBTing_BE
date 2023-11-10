from imaplib import _Authenticator
from django.shortcuts import render, get_object_or_404
import jwt
from rest_framework.views import APIView

from config.settings import SECRET_KEY
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

MBTIDic = {
    'ENTP': ['INFJ', 'INTJ'],
    'ENFP': ['INTJ', 'INFJ'],
    'ESTP': ['ISFJ', 'ISTJ'],
    'ENTJ': ['INTP', 'INFP'],
    'ESTJ': ['ISFP', 'ISTP'],
    'ESFP': ['ISTJ', 'ISFJ'],
    'ENFJ': ['INFP', 'ISFP'],
    'ESFJ': ['ISTP', 'INTP'],
    'INTP': ['ESTJ', 'ENTJ'],
    'INFP': ['ENFJ', 'ENTJ'],
    'ISTP': ['ESFJ', 'ESTJ'],
    'INTJ': ['ENFP', 'ENTP'],
    'ISTJ': ['ESFP', 'ESTP'],
    'ISFP': ['ESFJ', 'ENFJ'],
    'INFJ': ['ENFP', 'ENTP'],
    'ISFJ': ['ESTP', 'ESFP']
}


# Create your views here.
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token) #JWT token
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AuthAPIView(APIView):
    # 유저 정보 확인
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES.get('access')
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def post(self, request):
        # 유저 인증
        email2  = request.data.get("email")
        user = authenticate(
            email=request.data.get("email"), 
            password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            user = get_object_or_404(User, email=email2)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            res.set_cookie('user_id', user.id, httponly=True)

            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("user_id")
        return response
    

#테스트용 viewset
# jwt 토근 인증 확인용 뷰셋
# Header - Authorization : Bearer <발급받은토큰>
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 본인의 MBTI와 연관된 2개의 MBTI User 보내기
class RelationMBTI(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user_id = request.COOKIES.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user_mbti = user.mbti
        related_mbti = MBTIDic.get(user_mbti, [])  # user_mbti에 대한 관련 MBTI 가져오기
        print(related_mbti)
        # 관련 MBTI를 반환할 수 있도록 필요에 맞게 처리
        return Response({'related_mbti': related_mbti})

# 10개의 질문이 끝나고, 결과 MBTI 넣기 
class ResultMBTI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def patch(self, request, *args, **kwargs):
    #     return super().patch(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        user_id = request.COOKIES.get('user_id')
        user = get_object_or_404(User, pk=user_id) #id=user_id pk값으로 변경
        ################################ 프론트 값에 따라 수정 필요################################
        #mbti = request.GET['mbti']
        mbti = "ENTJ"
        user.mbti = mbti
        print(user.mbti)
        user.save()
        return Response(status=status.HTTP_200_OK)

# class ResultMBTI(APIView):
#     def put(self, request):
#         user_id = request.COOKIES['user_id']
#         user = get_object_or_404(User, id=user_id)
#         mbti = request.GET['mbti']
#         user.mbti = mbti
#         print(user.mbti)
#         print(mbti)

#         return Response(status=status.HTTP_200_OK)

class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer

    def patch(self, request, *args, **kwargs):
        user_id = request.COOKIES.get('user_id')
        user = get_object_or_404(User, id=user_id)
        kakao = request.data.get('kakao')

        if kakao:
            user.kakao = kakao
            user.save()

        return self.partial_update(request, *args, **kwargs)
