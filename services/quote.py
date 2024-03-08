import requests
from django.core.cache import cache
from rest_framework.exceptions import ValidationError

from quotes.models import Quote


class QuoteThirdParty:
    """
    Documentation: https://github.com/lukePeavey/quotable?tab=readme-ov-file
    Postman Collection: https://www.postman.com/quotable/workspace/quotable
    """

    @property
    def base_url(self) -> str:
        return "https://api.quotable.io/{request_param}"

    def get_quotes_list(self, limit, term=None, author=None, tags=None):
        url = self.base_url.format(request_param="quotes/random")
        params = {
            'limit': limit,
            'term': term,
            'author': author,
            'tags': tags
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        quotes = response.json()
        for quote in quotes:
            quote_id = quote.pop('_id')
            cached_quote = cache.get(quote_id)
            if cached_quote:
                quote = cached_quote
            else:
                quote, _ = Quote.objects.get_or_create(
                    _id=quote_id,
                    defaults=quote
                )
                cache.set(quote_id, quote)
        return quotes

    def get_quote_detail(self, quote_id):
        url = self.base_url.format(request_param=f'quotes/{quote_id}')
        response = requests.get(url)
        if response.status_code == 404:
            raise ValidationError("Quote not found")
        response.raise_for_status()
        quote_data = response.json()
        quote = Quote.objects.create(
            **quote_data
        )
        return quote
