from rest_framework.response import Response

def custom_response(message, code, data=None, sub_code="0", errors=None):
    """
    Utility to format API responses consistently.
    """
    return {
        "message": message,
        "code": code,
        "data": data,
        "subCode": sub_code,
        "errors": errors,
    }

def get_paginated_response(self, data):
    return Response(custom_response(
        message="Paginated data retrieved successfully",
        code=200,
        data={
            "total": self.page.paginator.count,
            "count": len(data),
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        }
    ))
