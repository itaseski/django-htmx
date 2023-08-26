from django.urls import path

from . import views

app_name = 'adamchainz'

urlpatterns = [
    path("", views.index, name="index"),
    path("favicon.ico", views.favicon),
    path("csrf-demo/", views.csrf_demo, name="csrf-demo"),
    path("csrf-demo/checker/", views.csrf_demo_checker),
    path("error-demo/", views.error_demo),
    path("error-demo/trigger/", views.error_demo_trigger),
    path("middleware-tester/", views.middleware_tester),
    path("middleware-tester/table/", views.middleware_tester_table),
    path("partial-rendering/", views.partial_rendering),
    # BugBites 
    path("bb-index/", views.bb_index, name="bb-index"),
    path("bb-client-redirect/", views.bb_client_redirect, name="bb-client-redirect"),
    path("bb-client-refresh/", views.bb_client_refresh, name="bb-client-refresh"),
    path("bb-client-location/", views.bb_client_location, name="bb-client-location"),
    path("bb-success/", views.bb_success, name="bb-success"),
    path("bb-response-modyfying-functions/", views.bb_response_modyfying_functions,
         name="bb-response-modyfying-functions"),
    path("bb-poll-url/", views.bb_push_url, name="bb-poll-url"),
    path("bb-reswap/", views.bb_reswap, name="bb-reswap"),
    path("bb-retarget/", views.bb_retarget, name="bb-retarget"),
]
