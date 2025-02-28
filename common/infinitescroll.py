from rest_framework.pagination import PageNumberPagination


class InfiniteScrollPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_queryset(self, request, queryset):
        start_after = request.query_params.get('start_after')
        if start_after:
            queryset = queryset.filter(id__gt=start_after).order_by('id')
        return queryset
