from ads.models import Ad, Comment, Fav
from ads.forms import CommentForm, CreateForm
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from ads.utils import dump_queries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.urls import resolve
from django.core.paginator import Paginator
from django.views.generic import ListView



#METERLE REGISTRO DE USUARIOS
#https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog




class AdListView(OwnerListView):
    model = Ad
    template_name = "ads/ad_list.html"
    paginate_by = 2


    context_object_name = "ad_list"

    # #paginacion va funcionando con esto
    def get_queryset(self):
        current_url = resolve(self.request.path_info).url_name 
        
        if 'my_ads' in current_url:
            obj_iniciales = Ad.objects.filter(owner=self.request.user.id)
        else:
            obj_iniciales = Ad.objects.all()

        query = self.request.GET.get("search", False) #barra buscar

        if query:
            obje = obj_iniciales.filter(
                 Q(title__icontains=query) | Q(text__icontains=query)).order_by(
                     '-updated_at').distinct()[:10]
            return obje

        obje = obj_iniciales.order_by('-updated_at')[:10]

        for obj in obje:
            obj.natural_updated = naturaltime(obj.updated_at)

        return obje

             #paginacion va funcionando con esto
    
    # def get_queryset(self):
    #     current_url = resolve(self.request.path_info).url_name 
        
    #     if 'my_ads' in current_url:
    #         ad_list = Ad.objects.filter(owner=request.user.id)
    #     else:
    #         ad_list = Ad.objects.all()

    #     strval = self.request.GET.get("search", False) #barra buscar
    #     if strval :
    #          # Simple title-only search
    #          # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

    #          # Multi-field search
    #          # __icontains for case-insensitive search
    #          query = Q(title__icontains=strval) 
    #          query.add(Q(text__icontains=strval), Q.OR)
    #          objects = ad_list.filter(query).select_related().order_by('-updated_at')[:10]
    #     else :
    #          # try both versions with > 4 posts and watch the queries that happen
    #          objects = ad_list.all().order_by('-updated_at')[:10]
    #          # objects = Post.objects.select_related().all().order_by('-updated_at')[:10]
    #      # Augment the post_list
    #     for obj in objects:
    #          obj.natural_updated = naturaltime(obj.updated_at)

    
    # def get(self, request) :



    #     current_url = resolve(request.path_info).url_name 
        
    #     if 'my_ads' in current_url:
    #         ad_list = Ad.objects.filter(owner=request.user.id)
        
    #     else:
    #         ad_list = Ad.objects.all()
        
    #     p = Paginator(ad_list,3) #paginacion, 9 elementos por pagina

    #     #print(p.num_pages) #numero de paginas

    #     #for page in p.page_range:
    #     #    print(page)

    #     #p1 = p.page(1) #<Page 1 of 3>
        
    #     strval =  request.GET.get("search", False) #barra buscar
    #     if strval :
    #         # Simple title-only search
    #         # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

    #         # Multi-field search
    #         # __icontains for case-insensitive search
    #         query = Q(title__icontains=strval) 
    #         query.add(Q(text__icontains=strval), Q.OR)
    #         objects = ad_list.filter(query).select_related().order_by('-updated_at')[:10]
    #     else :
    #         # try both versions with > 4 posts and watch the queries that happen
    #         objects = ad_list.all().order_by('-updated_at')[:10]
    #         # objects = Post.objects.select_related().all().order_by('-updated_at')[:10]
    #     # Augment the post_list
    #     for obj in objects:
    #         obj.natural_updated = naturaltime(obj.updated_at)

    #     ctx = {'ad_list' : objects,  'search': strval}
    #     retval= render(request, self.template_name, ctx)
    #     dump_queries()
    #     return retval





class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    def get(self, request, pk) :
        x = Ad.objects.get(id=pk) #haces una query
        comments = Comment.objects.filter(ad=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)


class AdCreateView(LoginRequiredMixin, View):
    #model = Ad
    #fields = ['title','price', 'text', 'picture']

    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):

    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()

        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):  #para heredar
    model = Ad


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=f)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])


def stream_file(request, pk):
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response

