# from django.http import Http404
# from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Album, Song
from .forms import UserForm, LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginView(View):
    form_class = LoginForm
    template_name = 'music/login.html'

    # display blank LoginForm
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process user data
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        # 驗證帳號
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # 登入後重導
                login(request, user)
                return redirect('music:index')
        else:
            form = self.form_class(request.POST)
            # not login
            return render(request, self.template_name, {'form': form, 'error_message': 'Account or password error'})


class LogoutView(View):
    templates_name = 'music/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class(None)
        logout(request)

        return render(request, self.template_name, {'form': form, 'error_message': 'Logout success!'})


class IndexView(LoginRequiredMixin, generic.ListView):

    login_url = "/music/login/"
    template_name = "music/index.html"
    # default is object_list
    context_object_name = "albums"

    def get_queryset(self):
        return Album.objects.all()


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumUpdate(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

    model = Album


class AlbumDelete(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('music:index')
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        # check data
        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # password need 加密
            user.set_password(password)
            user.save()

            # return User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')
        else:
            # not login
            return render(request, self.template_name, {'form': form})


# def favorite(request, album_id):
#     album = get_object_or_404(Album, pk=album_id)
#     try:
#         selected_song = album.song_set.get(pk=request.POST['song'])
#     except(KeyError, Song.DoesNotExist):
#         return render(request, 'music/detail.html', {
#             'album': album,
#             'error_message': "You did not select a valid song",
#         })
#     else:
#         # set True to False,False to True
#         selected_song.set_favorite()
#     return render(request, 'music/detail.html', {'album': album})
