from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Allow clients to override page size with ?page_size=."""

    page_size_query_param = 'page_size'
    max_page_size = 200
