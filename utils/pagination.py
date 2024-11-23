from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class to format the response structure.
    """
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow client to set page size
    max_page_size = 100  # Max page size allowed

    def get_paginated_response(self, data):
        return Response({
            "message": "Data retrieved successfully",
            "code": 200,
            "subCode": "0",
            "errors": None,
            "data": {
                "total": self.page.paginator.count,  # Total items
                "count": len(data),  # Items on the current page
                "next": self.get_next_link(),  # Link to next page
                "previous": self.get_previous_link(),  # Link to previous page
                "results": data  # The actual data
            }
        })
