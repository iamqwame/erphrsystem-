from rest_framework.test import APITestCase, APIClient
from employees.models import Employee
from rest_framework import status


class BaseAPITestCase(APITestCase):
    """
    Base test case for API tests.
    Provides common setup for all API test cases.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up shared test data. Runs once for the entire test class.
        """
        cls.client = APIClient()

        # Create test employees
        cls.employee1 = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone="1234567890",
            department="IT",
            position="Developer",
            hire_date="2020-01-01",
            salary=60000,
        )
        cls.employee2 = Employee.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="janesmith@example.com",
            phone="9876543210",
            department="HR",
            position="Manager",
            hire_date="2018-05-15",
            salary=80000,
        )

        # Sample payloads for create/update
        cls.valid_employee_data = {
            "first_name": "Alice",
            "last_name": "Brown",
            "email": "alicebrown@example.com",
            "phone": "1231231234",
            "department": "Finance",
            "position": "Analyst",
            "hire_date": "2021-06-01",
            "salary": 55000,
        }
        cls.invalid_employee_data = {
            "first_name": "",
            "email": "invalid-email",
        }


class EmployeeAPITestCase(BaseAPITestCase):
    """
    Unit tests for Employee API endpoints.
    """

    def test_list_employees(self):
        """
        Test listing all employees with pagination.
        """
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["code"], 200)
        self.assertEqual(response.data["data"]["total"], 2)

    def test_create_employee_valid(self):
        """
        Test creating a new employee with valid data.
        """
        response = self.client.post("/api/employees/", self.valid_employee_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["code"], 201)
        self.assertEqual(response.data["data"]["first_name"], "Alice")

    def test_create_employee_invalid(self):
        """
        Test creating a new employee with invalid data.
        """
        response = self.client.post("/api/employees/", self.invalid_employee_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], 400)
        self.assertIn("errors", response.data)

    def test_retrieve_employee(self):
        """
        Test retrieving a single employee by employee_id.
        """
        response = self.client.get(f"/api/employees/{self.employee1.employee_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["code"], 200)
        self.assertEqual(response.data["data"]["email"], "johndoe@example.com")

    def test_update_employee(self):
        """
        Test updating an existing employee by employee_id.
        """
        updated_data = {"first_name": "Johnathan"}
        response = self.client.put(f"/api/employees/{self.employee1.employee_id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["first_name"], "Johnathan")

    def test_delete_employee(self):
        """
        Test deleting an employee by employee_id.
        """
        response = self.client.delete(f"/api/employees/{self.employee1.employee_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.filter(employee_id=self.employee1.employee_id).count(), 0)
