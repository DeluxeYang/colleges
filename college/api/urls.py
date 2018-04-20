from django.urls import include, path
from api.views import college, news, rest
from rest_framework.urlpatterns import format_suffix_patterns
# API endpoints
urlpatterns = format_suffix_patterns([
    path('', rest.api_root),
    path('college/', college.CollegeList.as_view(), name='college-list'),
    path('college/<int:pk>/', college.CollegeDetail.as_view(), name='college-detail'),
    # url('college/by/', college.CollegesByNation.as_view(), name='college-by'),
])

urlpatterns += [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('college/by/nation/', college.get_colleges_by_nation),

    path('news/image_upload/', news.image_upload),
]
