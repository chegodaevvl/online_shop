from django.contrib.postgres.search import SearchVector, SearchQuery, \
    SearchRank, SearchHeadline, TrigramSimilarity, TrigramDistance
from django.db.models import Q, F, Value
from django.db.models.functions import Concat

from django.views.generic import ListView


class SearchResultsList(ListView):

    def get_queryset(self):
        query = self.request.GET.get()
        search_vector = SearchVector(*self.vector,)
        search_query = SearchQuery(query)
        search_headline = SearchHeadline(self.headline_expression,
                                         search_query)

        result = self.model.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).annotate(annotate_expression=self.annotate_expression,
                   headline=search_headline).filter(
            search=search_query).order_by("-rank")

        if not result:
            return self.model.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).annotate(
                similarity=TrigramSimilarity(self.vector[0], query)
                           + TrigramSimilarity(self.vector[1], query),
            ).filter(similarity__gte=0.3).order_by("-similarity")

        return result
