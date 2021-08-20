from rest_framework import pagination
from rest_framework.response import Response


class GenericPagination(pagination.PageNumberPagination):
    # django_paginator_class = RODjangoPaginator

    def get_paginated_response(self, data):
        pagination_data = {
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
        }
        pagination_data.update(data)
        return Response(pagination_data)
