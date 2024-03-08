from rest_framework import serializers

from quotes.models import Quote


class QuotesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = (
            "_id",
            "content",
            "author",
            "tags",
            "authorSlug",
            "length",
            "dateAdded",
            "dateModified"
        )


class QuotesDetailSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(max_length=32))

    class Meta:
        model = Quote
        fields = (
            "_id",
            "content",
            "author",
            "tags",
            "authorSlug",
            "length",
            "dateAdded",
            "dateModified"
        )

