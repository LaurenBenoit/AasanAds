import core.views as coreviews
from django.conf.urls import url

urlpatterns = [url(r'^$', coreviews.Hello),
]