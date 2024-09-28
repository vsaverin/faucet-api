from django.urls import path

from . import views

urlpatterns = [
    path("faucet/fund", views.FaucetView.as_view(), name="fund_faucet"),
    path("faucet/stats", views.FaucetStatsView.as_view(), name="faucet_stats"),
]
