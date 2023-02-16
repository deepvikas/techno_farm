from django.urls import path
from django.contrib.auth import views as auth_views

from .views import AddFarmView, AddCropView, UpdateCropsView, UpdateFarmView, AvailableCropsView, GetAllFarmsDetails, GetFarm, AddSeasonView, AllSeasonsView

urlpatterns = [
    path('add/farm', AddFarmView.as_view(), name='add-farm-view'),
    path('add/crop', AddCropView.as_view(), name='add-crop-view'),
    path('update/crop/<int:farm_id>', UpdateCropsView.as_view(), name='update-crop-view'),
    path('update/my/farm/<int:farm_id>', UpdateFarmView.as_view(), name='update-my-farm'),
    path('get/crops', AvailableCropsView.as_view(), name='crops-view'),
    path('my/all/farms', GetAllFarmsDetails.as_view(), name='my-farms-view'),
    path('farm/detail/<int:farm_id>', GetFarm.as_view(), name='my-farms-view'),
    path('all/seasons', AllSeasonsView.as_view(), name='all-seasons-view'),
    path('add/season', AddSeasonView.as_view(), name='add-seasons-view'),
]