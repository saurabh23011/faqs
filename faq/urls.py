from django.urls import path
from .views import FAQListView, QueryView

urlpatterns = [
    path('faqs/',FAQListView.as_view(),name='faq-list'),
    path('query/',QueryView.as_view(),name='query')
]
