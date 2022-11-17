from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='caser'),
    path('affine',views.affine,name='affine'),
    path('vigenere',views.vigenere,name='vigenere'),
    path('columnart',views.columnart,name='columnart'),
    path('simplet',views.simplet,name='simplet'),
    path('irregulart',views.irregulart,name='irregulart')
]
