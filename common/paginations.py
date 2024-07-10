from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict


class CustomPagination(PageNumberPagination):

    page_query_param = "page"
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_page_number(self, request):
        try:
            page_number = int(request.query_params.get(self.page_query_param, 1))
        except ValueError:
            page_number = 1
        return page_number

    def get_page_size(self, request):
        try:
            page_size = int(request.query_params.get(self.page_size_query_param, self.page_size))
        except ValueError:
            page_size = self.page_size
        return page_size

    def paginate(self, queryset, request):
        page_number = self.get_page_number(request)
        page_size = self.get_page_size(request)
        paginator = Paginator(queryset, page_size)
        paged_queryset = paginator.get_page(page_number)
        self.page = paged_queryset
        return list(paged_queryset)

    @property
    def link_info(self):
        link_info = {
            "current_page": self.page.number,
            "total_pages": self.page.paginator.num_pages,
            "next_link": self.get_next_link(),
            "prev_link": self.get_previous_link(),
            "count": self.page.paginator.count,
        }
        return link_info
