from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LoginUser
from django.contrib.auth.hashers import make_password, check_password


class AppLogin(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', "")
        user_pw = request.data.get('user_pw', "")
        user = LoginUser.objects.filter(user_id=user_id).first()

        if user is None:
            return Response(dict(msg="해당 ID의 사용자가 없습니다."))

        if check_password(user_pw, user.user_pw):
            return Response(dict(msg="로그인 성공", user_id=user.user_id))
        else:
            return Response(dict(msg="로그인 실패. 패스워드 불일치"))


class RegistUser(APIView):
    def post(self, request):

        user_id = request.data['user_id']
        # 아이디 공백 체크
        if user_id == '' or None:
            return Response(status=200, data=dict(msg="아이디는 공백이 될 수 없습니다!!"))

        user_pw = request.data['user_pw']
        # 패스워드 공백 체크
        if user_pw == '' or None:
            return Response(status=200, data=dict(msg="비밀번호는 공백이 될 수 없습니다!!"))

        # 이미 존재하는 아이디인지 체크
        if LoginUser.objects.filter(user_id=user_id).exists():
            return Response(status=200, data=dict(msg="이미 존재하는 아이디 입니다."))

        # 암호화 해서 집어넣기
        user = LoginUser.objects.create(user_id=user_id, user_pw=make_password(user_pw))

        return Response(status=200, data=dict(msg="회원가입 성공", user_id=user.user_id))
