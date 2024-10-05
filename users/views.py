import csv
import os.path

import pandas as pd
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .Producer import UserProducer
from .models import User
from .serializers import UserSerializer

from django.http import JsonResponse


# 获取所有用户
@api_view(['GET'])
def get_users(request):
    # 1.添加查询条件，sort
    # users = (User.objects.all()
    #          .filter(salary__gt=request.data['salary'])).order_by('name')

    # 2. native query
    users = User.objects.raw('SELECT * FROM users WHERE email LIKE %s', ['%@outlook.com'])

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# 获取单个用户
@api_view(['GET'])
def get_user(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        # return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "User not found"}, status=status.HTTP_200_OK)

    serializer = UserSerializer(user)
    return Response(serializer.data)


# 创建用户
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 更新用户
@api_view(['PUT'])
def update_user(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 删除用户
@api_view(['DELETE'])
def delete_user(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# 下載csv
@api_view(['GET'])
def export_users_csv(request):
    # 增加異常處理

    # 创建 HTTP 响应，设置为 CSV 文件
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    # 创建 CSV writer
    csvWrite = csv.writer(response)

    # 写入 CSV 的头部
    csvWrite.writerow(['ID', 'Name', 'Email', 'Salary'])

    # 查询数据库中的所有用户

    users = User.objects.all().values_list('id', 'name', 'email', 'salary')

    for user in users:
        csvWrite.writerow(user)

    return response


@api_view(['POST'])
def upload_csv_to_db(request):
    # 定义 CSV 文件的路径
    csv_file_path = os.path.join(os.path.dirname(__file__), request.data['path'])

    try:
        # 使用 pandas 读取 CSV 文件
        data = pd.read_csv(csv_file_path)

        # 遍历每一行，并插入到数据库
        for index, row in data.iterrows():
            # 假设 CSV 文件中有 'name', 'email', 'salary' 列
            User.objects.create(
                name=row['Name'],
                email=row['Email'],
                salary=row['Salary']
            )

        return JsonResponse({'status': 'success', 'message': 'CSV data uploaded successfully!'})

    except FileNotFoundError:
        return JsonResponse({'status': 'error', 'message': 'CSV file not found!'}, status=404)

    except Exception as e:
        # 打印异常信息到控制台
        print(f"Error: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


# 更新用户信息并发送消息到 Kafka。
@api_view(['POST'])
def update_user_kafka(request):
    try:
        userId = request.data.get('id')
        user = User.objects.get(id=userId)
        user.name = request.data.get('name', user.name)
        user.email = request.data.get('email', user.email)
        user.salary = request.data.get('salary', user.salary)
        user.save()

        # 发送更新消息到 Kafka
        producer = UserProducer()
        producer.send_user_update({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'salary': user.salary
        })

        return JsonResponse({'status': 'success'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
