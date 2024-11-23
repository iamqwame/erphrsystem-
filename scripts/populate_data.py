import os
import random
import django
from faker import Faker
import sys

# Set up Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '..')) 
sys.path.append(src_dir) 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') 
django.setup()

from employees.models import Employee  # Import the Employee model

# Initialize Faker for generating random data
fake = Faker()

def clear_data():
    """
    Clear old data from the Employee table.
    """
    print("Clearing old data...")
    Employee.objects.all().delete()
    print("Old data cleared successfully.")


def populate_employees(n=10):
    """
    Populate the Employee table with sample data.
    """
    print(f"Creating {n} employees...")
    for _ in range(n):
        Employee.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            phone=fake.phone_number(),
            department=fake.job(),
            position=fake.job(),
            hire_date=fake.date_between(start_date="-10y", end_date="today"),
            salary=random.randint(30000, 120000),
        )
    print(f"{n} employees created successfully.")


if __name__ == "__main__":
    clear_data()  # Clear old data first
    populate_employees(100)  # Populate 100 employees
    print("Sample employee data added successfully.")
