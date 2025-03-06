from rest_framework.pagination import PageNumberPagination


class InfiniteScrollPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    key = 'key'
    order = 'ASC'

    def get_queryset(self, request, queryset):
        if self.key not in request.query_params:
            return queryset
        key: int = request.query_params[self.key]
        order = self.order
        if order.lower() == 'asc':
            return queryset.filter(id__gt=key)
        return queryset.filter(id__lt=key)
