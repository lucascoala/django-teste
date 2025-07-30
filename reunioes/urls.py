from django.urls import path
from .views import ReuniaoConselhoCreate, ReuniaoConselhoDelete, ReuniaoConselhoUpdade, ReuniaoConselhoList, ReuniaoConselhoView
from .views import ReuniaoDiaconosCreate, ReuniaoDiaconosDelete, ReuniaoDiaconosUpdade, ReuniaoDiaconosList, ReuniaoDiaconosView

urlpatterns = [
   # path('endereço/', MinhaView.as_view(), name = "Nome-da-url"),
   path('cadastrar/reuniaoconselho', ReuniaoConselhoCreate.as_view(), name = "cadastrar-reuniaoconselho"),
   path('editar/reuniaoconselho/<int:pk>', ReuniaoConselhoUpdade.as_view(), name =  'editar-reuniaoconselho'),
   path('excluir/reuniaoconselho/<int:pk>', ReuniaoConselhoDelete.as_view(), name =  'excluir-reuniaoconselho'),
   path('visualizar/reuniaoconselho/<int:pk>', ReuniaoConselhoView.as_view(), name =  'visualizar-idreuniaoconselho'),
   path('listar/reuniaoconselho', ReuniaoConselhoList.as_view(), name =  'listar-reuniaoconselho'),

   #__________________________________________________________________________

   path('cadastrar/reuniaodiaconos', ReuniaoDiaconosCreate.as_view(), name = "cadastrar-reuniaodiaconos"),
   path('editar/reuniaodiaconos/<int:pk>', ReuniaoDiaconosUpdade.as_view(), name =  'editar-reuniaodiaconos'),
   path('excluir/reuniaodiaconos/<int:pk>', ReuniaoDiaconosDelete.as_view(), name =  'excluir-reuniaodiaconos'),
   path('visualizar/reuniaodiaconos/<int:pk>', ReuniaoDiaconosView.as_view(), name =  'visualizar-idreuniaodiaconos'),
   path('listar/reuniaodiaconos', ReuniaoDiaconosList.as_view(), name =  'listar-reuniaodiaconos'),
]
