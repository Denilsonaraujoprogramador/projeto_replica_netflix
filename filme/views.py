from audioop import reverse
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForms, FormHomepage


class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated: #verifica se o usuario está autenticado/logado
            #redireciona para home
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs) #redireciona para a home page desse template home page

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')


class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme

class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme

    def get(self, request, *args, **kwargs):
        #contabilizar as visualizações
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super(Detalhesfilme, self).get(request, *args, **kwargs) #Redireciona o usuario para url final

    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        #filtras tabela de filmes por categoria
        filmes_relacionados = self.model.objects.filter(categoria=self.get_object().categoria)[0:5]
        context["filmes_relacionados"] = filmes_relacionados
        return context

class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None

class Paginaperfil(LoginRequiredMixin ,UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')
        
        

class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForms

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')




#def homepage(request):
#    return render(request, 'homepage.html')


#def homefilmes(request):
#    context = {}
#    lista_filmes = Filme.objects.all()
#    context ['lista_filmes'] = lista_filmes
#    return render(request, 'homefilmes.html', context)    
