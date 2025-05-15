from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("adolescente/dashboard/", views.dashboard_adolescente, name="dashboard_adolescente"),
    path('presenca/<int:evento_id>/<str:status>/', views.registrar_presenca, name='registrar_presenca'),

    path('lider/dashboard/', views.dashboard, name='dashboard'),
    path('lider/evento/novo/', views.criar_evento, name='criar_evento'),
    path('lider/evento/editar/<int:id>/', views.editar_evento, name='editar_evento'),
    path('lider/evento/excluir/<int:id>/', views.excluir_evento, name='excluir_evento'),

]