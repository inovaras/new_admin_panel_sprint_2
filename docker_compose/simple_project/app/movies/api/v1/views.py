from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.views.generic.list import BaseListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ...models import FilmWork, Genre, Person


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        return FilmWork.objects.prefetch_related('genres', 'persons').values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type'
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg('persons__full_name', filter=Q(personfilmwork__role='actor'), distinct=True),
            directors=ArrayAgg('persons__full_name', filter=Q(personfilmwork__role='director'), distinct=True),
            writers=ArrayAgg('persons__full_name', filter=Q(personfilmwork__role='writer'), distinct=True),
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, **response_kwargs)


class BaseDetailView(View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 10  # Количество объектов на странице

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)

        page = self.request.GET.get('page')
        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            movies = paginator.page(1)
        except EmptyPage:
            movies = paginator.page(paginator.num_pages)

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': movies.previous_page_number() if movies.has_previous() else None,
            'next': movies.next_page_number() if movies.has_next() else None,
            'results': list(movies),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        movie_id = kwargs.get('pk')
        movie = self.get_queryset().filter(id=movie_id).first()
        return movie if movie else {}
