from django.core.cache import cache
from django_filters import rest_framework
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from quotes.filters import QuotesListFilter
from quotes.models import Quote
from quotes.serializers import QuotesListSerializer, QuotesDetailSerializer
from services.quote import QuoteThirdParty


class QuotesListViewSet(
    ListModelMixin, viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = QuotesListSerializer
    model_cls = Quote
    filter_backends = (rest_framework.DjangoFilterBackend, SearchFilter)
    queryset = Quote.objects.all()
    filterset_class = QuotesListFilter

    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        limit = int(query_params.get('limit', 1))
        term = query_params.get('term')
        author = query_params.get('author')
        tags = query_params.get('tags')
        sort = query_params.get('sort')

        quotes = self.filter_queryset(self.get_queryset())
        if sort == 'random':
            quotes = quotes.order_by('?')
        if sort == 'newest':
            quotes = quotes.order_by('-created_at')
        elif sort == 'oldest':
            quotes = quotes.order_by('created_at')
        quotes_count = quotes.count()
        if quotes_count < limit:
            third_party_quotes = QuoteThirdParty().get_quotes_list(limit - quotes_count, term, author, tags)
            quotes = list(quotes) + third_party_quotes
        serializer = self.get_serializer(quotes[:limit], many=True)
        return Response(serializer.data)


class QuotesDetailViewSet(
    GenericViewSet,
):
    serializer_class = QuotesDetailSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            self.permission_classes = [IsAdminUser]
        if self.request.method in ["POST", "PATCH"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_object(self):
        quote_id = self.kwargs.get("quote_id")
        return cache.get(quote_id)

    def retrieve(self, request, *args, **kwargs):
        quote_id = self.kwargs.get("quote_id")
        cached_obj = self.get_object()
        if cached_obj:
            serializer = QuotesListSerializer(cached_obj)
            return Response(serializer.data)
        try:
            quote = Quote.objects.get(_id=quote_id)
        except Quote.DoesNotExist:
            quote = QuoteThirdParty().get_quote_detail(quote_id)
        cache.set(quote_id, quote)
        serializer = QuotesListSerializer(quote)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        quote_id = self.kwargs.get("quote_id")
        quote = Quote.objects.filter(_id=quote_id)
        if quote.exists():
            return Response({"quote with this quote_id  already exists."}, status=status.HTTP_400_BAD_REQUEST)
        request.data.update({"_id": quote_id})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.set(quote_id, serializer.save())
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        quote_id = self.kwargs.get("quote_id")
        quote = get_object_or_404(Quote, _id=quote_id)
        quote.delete()
        cache.delete(quote_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        quote_id = self.kwargs.get("quote_id")
        try:
            quote = Quote.objects.get(_id=quote_id)
        except Quote.DoesNotExist:
            return Response({'error': 'Quote not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(quote, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        quote = serializer.save()
        cache.set(quote_id, quote)
        return Response(serializer.data)
