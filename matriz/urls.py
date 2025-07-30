from django.urls import path
from .views import MatrizGUTCreate, MatrizGUTDelete, MatrizGUTList, MatrizGUTUpdade, MatrizGUTView
from .views import Matriz5W2HCreate, Matriz5W2HDelete, Matriz5W2HList, Matriz5W2HUpdade, Matriz5W2HView
urlpatterns = [
   # path('endereço/', MinhaView.as_view(), name = "Nome-da-url"),
   path('cadastrar/matrizGUT', MatrizGUTCreate.as_view(), name = "cadastrar-matrizGUT"),
   path('editar/matrizGUT/<int:pk>', MatrizGUTUpdade.as_view(), name =  'editar-matrizGUT'),
   path('excluir/matrizGUT/<int:pk>', MatrizGUTDelete.as_view(), name =  'excluir-matrizGUT'),
   path('visualizar/matrizGUT/<int:pk>', MatrizGUTView.as_view(), name =  'visualizar-matrizGUT'),
   path('listar/matrizGUT', MatrizGUTList.as_view(), name =  'listar-matrizGUT'),

   path('cadastrar/matriz5W2H', Matriz5W2HCreate.as_view(), name = "cadastrar-matriz5W2H"),
   path('editar/matriz5W2H/<int:pk>', Matriz5W2HUpdade.as_view(), name =  'editar-matriz5W2H'),
   path('excluir/matriz5W2H/<int:pk>', Matriz5W2HDelete.as_view(), name =  'excluir-matriz5W2H'),
   path('visualizar/matriz5W2H/<int:pk>', Matriz5W2HView.as_view(), name =  'visualizar-matriz5W2H'),
   path('listar/matriz5W2H', Matriz5W2HList.as_view(), name =  'listar-matriz5W2H'),

]
