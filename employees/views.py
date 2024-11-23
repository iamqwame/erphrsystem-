from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from .models import Employee
from .serializers import EmployeeSerializer
from utils.pagination import CustomPagination
from utils.response_formatter import custom_response
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

class EmployeeListCreateAPIView(ListCreateAPIView):
    """
    Handles listing and creating employees with pagination.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = custom_response(
                message="Employee created successfully",
                code=201,
                data=serializer.data
            )
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(custom_response(
            message="Employee creation failed",
            code=400,
            errors=serializer.errors
        ), status=status.HTTP_400_BAD_REQUEST)

class EmployeeRetrieveUpdateDeleteAPIView(APIView):
    """
    Handles retrieving, updating, and deleting an employee by ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve Employee",
        operation_description="Retrieve details of a specific employee by ID.",
        responses={200: EmployeeSerializer, 404: "Employee not found"},
    )
    def get(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee)
            response_data = custom_response(
                message="Employee retrieved successfully",
                code=200,
                data=serializer.data,
            )
            return Response(response_data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            response_data = custom_response(
                message="Employee not found",
                code=404,
                errors={"detail": "Employee does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Update Employee",
        operation_description="Update details of a specific employee by ID.",
        request_body=EmployeeSerializer,
        responses={200: EmployeeSerializer, 404: "Employee not found"},
    )
    def put(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = custom_response(
                    message="Employee updated successfully",
                    code=200,
                    data=serializer.data,
                )
                return Response(response_data, status=status.HTTP_200_OK)
            response_data = custom_response(
                message="Employee update failed",
                code=400,
                errors=serializer.errors,
            )
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            response_data = custom_response(
                message="Employee not found",
                code=404,
                errors={"detail": "Employee does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="Delete Employee",
        operation_description="Delete a specific employee by ID.",
        responses={204: "No content", 404: "Employee not found"},
    )
    def delete(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()
            response_data = custom_response(
                message="Employee deleted successfully",
                code=204,
                data=None,
            )
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            response_data = custom_response(
                message="Employee not found",
                code=404,
                errors={"detail": "Employee does not exist"},
            )
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
