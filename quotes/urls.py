from django.urls import path
from rest_framework.routers import DefaultRouter

from quotes import views

router = DefaultRouter()
router.register(
    "quotes", views.QuotesListViewSet, "quotes-list"
)
urlpatterns = router.urls
urlpatterns += [
    path(
        "quotes/<str:quote_id>",
        views.QuotesDetailViewSet.as_view(
            {"get": "retrieve",
             "patch": "update",
             "post": "create",
             "delete": "destroy"
             }
        ),
        name="quotes",
    ),
]
