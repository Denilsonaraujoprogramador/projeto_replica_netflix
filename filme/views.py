from multiprocessing import context
from unicodedata import category
from django.shortcuts import render
from .models import Filme
from django.views.generic import TemplateView, ListView, DetailView


# Create your views here.
#def homepage(request):
#    return render(request, 'homepage.html')

class Homepage(TemplateView):
    template_name = "homepage.html"

#def homefilmes(request):
#    context = {}
#    lista_filmes = Filme.objects.all()
#    context ['lista_filmes'] = lista_filmes
#    return render(request, 'homefilmes.html', context)

class Homefilmes(ListView):
    template_name = "homefilmes.html"
    model = Filme

class Detalhesfilme(DetailView):
    template_name = "detalhesfilme.html"
    model = Filme

    def get(self, request, *args, **kwargs):
        #contabilizar as visualizações
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        return super(Detalhesfilme, self).get(request, *args, **kwargs) #Redireciona o usuario para url final

    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        #filtras tabela de filmes por categoria
        filmes_relacionados = self.model.objects.filter(categoria=self.get_object().categoria)[0:5]
        context["filmes_relacionados"] = filmes_relacionados
        return context

class Pesquisafilme(ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None


    
