from rest_framework.views import APIView
from .models import Task
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import render


# Create your views here.
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
        user_id = request.data.get('user_id', "")
        todo_id = request.data.get('todo_id', "")
        name = request.data.get('name', "")
        end_date = request.data.get('end_date', None)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        task = Task.objects.create(id=todo_id, user_id=user_id, name=name, end_date=end_date)

        return Response(dict(msg="To-Do 생성 완료", name=task.name, start_date=task.start_date.strftime('%Y-%m-%d'), end_date=task.end_date))


class TaskSelect(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', "")
        print(user_id)
        tasks = Task.objects.filter()

        task_list = []
        for task in tasks:
            task_list.append(dict(id=task.id,
                                  name=task.name,
                                  done=task.done))

        return Response(dict(tasks=task_list))


class TaskToggle(APIView):
    def post(self, request):
        print(request.data)
        todo_id = request.data.get('todo_id', "")
        #
        task = Task.objects.get(id=todo_id)
        task.done = False if task.done else True
        task.save()
        return Response(status=200)
        # return Response(status=200)


class TaskDelete(APIView):
    def post(self, request):
        todo_id = request.data.get('todo_id', "")
        task = Task.objects.filter(id=todo_id).first()
        task.delete()

        return Response(dict(msg="To-Do 삭제완료"))
