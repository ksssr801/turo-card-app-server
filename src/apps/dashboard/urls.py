from rest_framework import routers, urlpatterns
from . import views

router = routers.SimpleRouter()
router.register('', views.DashboardViewSet, basename="dashboard_app")
urlpatterns = router.urls