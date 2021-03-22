from rest_framework.views import APIView
from .models import Task
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import render


# Create your views here.
class Test(APIView):
    def post(self, request):
        return Response(status=400)


class Todo(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', "")
        name = request.data.get('name', "")
        end_date = request.data.get('end_date', None)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        Task.objects.create(user_id=user_id, name=name, end_date=end_date)

        tasks = Task.objects.all()
        task_list = []
        for task in tasks:
            task_list.append(dict(name=task.name, start_date=task.start_date, end_date=task.end_date, state=task.state))
        context = dict(task_list=task_list)
        return render(request, 'todo/todo.html', context=context)

    def get(self, request):
        tasks = Task.objects.all()
        task_list = []
        for task in tasks:
            task_list.append(dict(name=task.name, start_date=task.start_date, end_date=task.end_date, state=task.state))
        context=dict(task_list=task_list)
        return render(request, 'todo/todo.html', context=context)


class TaskCreate(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', None)
        todo_id = request.data.get('todo_id', None)
        name = request.data.get('name', None)

        # 이전버전 호환을 위해 todo_id가 들어오고 안들어오고로 분기
        if todo_id:
            task = Task.objects.create(id=todo_id, user_id=user_id, name=name)
        else:
            task = Task.objects.create(user_id=user_id, name=name)

        return Response(data=dict(id=task.id))


class TaskSelect(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', None)
        page_number = request.data.get('page_number', None)

        # print("user_id = ", user_id, ", page_number = ", page_number)
        is_last_page = True

        # user_id를 올리는 경우
        if user_id and not "":
            tasks = Task.objects.filter(user_id=user_id)
        else:
            tasks = Task.objects.all()

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

        return Response(dict(tasks=task_list, is_last_page=is_last_page))


class TaskToggle(APIView):
    def post(self, request):
        todo_id = request.data.get('todo_id', "")
        task = Task.objects.get(id=todo_id)
        task.done = False if task.done else True
        task.save()
        return Response()


class TaskDelete(APIView):
    def post(self, request):
        todo_id = request.data.get('todo_id', "")
        task = Task.objects.get(id=todo_id)
        if task:
            task.delete()

        return Response()
