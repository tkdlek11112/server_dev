from .models import Task
from rest_framework.response import Response
from common.common import TodoView, CommonResponse, SuccessResponse, SuccessResponseWithData, ErrorResponse
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers


logger = logging.getLogger('django')


# Create your views here.
class Test(TodoView):
    def post(self, request):
        print(self.user_id)
        input_value1 = request.data.get('input_value1', None)
        input_value2 = request.data.get('input_value2', None)
        input_value3 = request.data.get('input_value3', None)
        logger.error("INPUT HEADER " + self.user_id)
        logger.error("INPUT BODY input_value1 " + input_value1)
        logger.error("INPUT BODY input_value2 " + input_value2)
        logger.error("INPUT BODY input_value3 " + input_value3)


        output_value1 = input_value1 + "output"
        output_value2 = input_value2 + "output"
        output_value3 = input_value3 + "output"

        data = dict(output_value1=output_value1,
                    output_value2=output_value2,
                    output_value3=output_value3)

        logger.error("OUTPUT BODY output_value1 " + output_value1)
        logger.error("OUTPUT BODY output_value2 " + output_value2)
        logger.error("OUTPUT BODY output_value3 " + output_value3)

        return CommonResponse(0, "success", data)


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['user_id', 'name']


class TaskCreate(TodoView):
    '''
        여기에 주석으로 뭔가 쓰면 swagger에 반영됩니다.
        ---
        # TO-DO를 생성할 때 사용하는 API
            - user_id : 사용자 ID
            - name : To-Do 이름
    '''

    id_field = openapi.Schema(
        'id',
        description='To-Do가 생성되면 자동으로 채번되는 ID값',
        type=openapi.TYPE_STRING
    )

    success_response = openapi.Schema(
        title='response',
        type=openapi.TYPE_OBJECT,
        properties={
            'id': id_field
        }
    )

    @swagger_auto_schema(tags=["TO-DO 생성"],
                         request_body=TodoSerializer,
                         query_serializer=TodoSerializer,
                         responses={
                             200: success_response,
                             403: '인증에러',
                             400: '입력값 유효성 검증 실패',
                             500: '서버에러'
                         })
    def post(self, request):
        # 이전버전 호환을 위해 헤더먼저 검사하고 body로 내려감.
        print('헤더 id', self.user_id,'헤더 version', self.version)
        if self.user_id:
            user_id = self.user_id
        else:
            user_id = request.data.get('user_id', None)
        todo_id = request.data.get('todo_id', None)
        name = request.data.get('name', None)

        # 이전버전 호환을 위해 todo_id가 들어오고 안들어오고로 분기
        if todo_id:
            task = Task.objects.create(id=todo_id, user_id=user_id, name=name)
        else:
            task = Task.objects.create(user_id=user_id, name=name)

        if self.version < '1.1':
            return Response(data=dict(id=task.id))
        else:
            return SuccessResponseWithData(dict(id=task.id))


class TaskSelect(TodoView):
    def post(self, request):
        # 헤더에 id가 있으면 헤더의 id를 사용하고 없으면 body의 id를 사용
        if self.user_id:
            user_id = self.user_id
        else:
            user_id = request.data.get('user_id', None)
        page_number = request.data.get('page_number', None)

        is_last_page = True

        # user_id를 올리는 경우
        if user_id == "":
            tasks = []
        elif user_id:
            tasks = Task.objects.filter(user_id=user_id)
        else:
            tasks = Task.objects.all()

        if len(tasks) > 0:
            if page_number is not None and page_number >= 0:
                # print('총 todo 수 : ', tasks.count())
                if tasks.count() <= 10:
                    pass
                elif tasks.count() <= (1 + page_number) * 10:
                    tasks = tasks[page_number * 10:]
                else:
                    tasks = tasks[page_number * 10: (1 + page_number) * 10]
                    is_last_page = False

            # page_number가 없는경우.. 이전 버전 api이거나 실수로 못올렸거나
            # 그냥 0으로 생각하고 응답줄지 아니면 에러 응답할지 선택해야함.
            else:
                pass

        task_list = []
        for task in tasks:
            task_list.append(dict(id=task.id,
                                  userId=task.user_id,
                                  name=task.name,
                                  done=task.done))

        if self.version < '1.1':
            return Response(dict(
                tasks=task_list,
                is_last_page=is_last_page
            ))
        else:
            return SuccessResponseWithData(dict(
                tasks=task_list,
                is_last_page=is_last_page
            ))


class TaskToggle(TodoView):
    def post(self, request):
        todo_id = request.data.get('todo_id', "")
        task = Task.objects.get(id=todo_id)
        task.done = False if task.done else True
        task.save()

        if self.version < '1.1':
            return Response()
        else:
            return SuccessResponse()


class TaskDelete(TodoView):
    def post(self, request):
        todo_id = request.data.get('todo_id', "")
        task = Task.objects.get(id=todo_id)
        if task:
            task.delete()

        if self.version < '1.1':
            return Response()
        else:
            return SuccessResponse()
