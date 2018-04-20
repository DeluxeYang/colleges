from django.urls import path
from backend.views import college, news, ranking, professor


urlpatterns = [
    path('', news.index),

    ######################################################################
    # college
    path('college/', college.index),
    path('college/search/<str:param>/', college.index),
    path('college/search/<str:param>/<int:digit>/', college.index),

    path('college/retrieve/', college.retrieve_colleges),
    path('college/retrieve/<str:param>/', college.retrieve_colleges),
    path('college/pick/<str:param>/', college.college_search_pick),
    path('college/retrieve/<str:param>/<int:digit>/', college.retrieve_colleges),

    path('college/add/', college.add_college),
    path('college/modify/<int:college_id>/', college.modify_college),
    path('college/delete/', college.delete_college),
    path('college/batch_delete/', college.batch_delete_college),
    path('college/import/', college.import_college),
    path('college/clean/', college.clean_college),

    ######################################################################
    # news
    path('news/', news.index),
    path('news/search/<str:param>/', news.index),
    path('news/search/<str:param>/<int:digit>/', news.index),

    path('news/retrieve/', news.retrieve_news),
    path('news/retrieve/<str:param>/', news.retrieve_news),
    path('news/retrieve/<str:param>/<int:digit>/', news.retrieve_news),

    path('news/pick/<str:param>/', news.news_search_pick),

    path('news/<int:news_id>/', news.get_news),
    path('news/add/', news.add_news),
    path('news/modify/<int:news_id>/', news.modify_news),
    path('news/delete/', news.delete_news),
    path('news/batch_delete/', news.batch_delete_news),

    ######################################################################
    # ranking
    path('ranking/', ranking.index),
    path('ranking/retrieve/', ranking.retrieve_ranking),
    path('ranking/<int:ranking_id>/', ranking.get_ranking),

    path('ranking/import/<int:ranking_id>/', ranking.import_ranking),

    path('ranking/add/', ranking.add_ranking),
    path('ranking/delete/', ranking.delete_ranking),
    path('ranking/batch_delete/', ranking.batch_delete_ranking),

    path('rankings/', ranking.rankings_index),
    path('rankings/retrieve/', ranking.retrieve_rankings),
    path('rankings/<int:ranking_id>/', ranking.rankings_index),
    path('rankings/retrieve/<int:ranking_id>/', ranking.retrieve_rankings),
    path('rankings/delete/', ranking.delete_rankings),
    path('rankings/batch_delete/', ranking.batch_delete_rankings_batches),

    path('rankings/content/<int:batch_id>/', ranking.rankings_content_index),
    path('rankings/content/retrieve/<int:batch_id>/', ranking.retrieve_rankings_content),
    path('rankings/search/college/', ranking.rankings_search_pick),

    ######################################################################
    # professor
    path('professor/', professor.index),
    path('professor/retrieve/', professor.retrieve_professor),
    path('professor/<int:professor_id>/', professor.get_professor),

    path('professor/import/<int:professor_id>/', professor.import_professor),

    path('professor/add/', professor.add_professor),
    path('professor/delete/', professor.delete_professor),
    path('professor/batch_delete/', professor.batch_delete_professor),

    path('professors/', professor.professors_index),
    path('professors/retrieve/', professor.retrieve_professors),
    path('professors/<int:professor_id>/', professor.professors_index),
    path('professors/retrieve/<int:professor_id>/', professor.retrieve_professors),
    path('professors/delete/', professor.delete_professors),
    path('professors/batch_delete/', professor.batch_delete_professors_batches),

    path('professors/content/<int:batch_id>/', professor.professors_content_index),
    path('professors/content/retrieve/<int:batch_id>/', professor.retrieve_professors_content),
    path('professors/search/college/', professor.professors_search_pick),
]
