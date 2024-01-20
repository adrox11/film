from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie
from .forms import MovieForm  # Fixed typo in import statement


def index(request):
    movies = Movie.objects.all()
    context = {
        'movie_list': movies,
    }
    return render(request, "index.html", context)


def detail(request, movie_id):
    movie = get_object_or_404(Movie,
                              id=movie_id)  # Used get_object_or_404 to handle the case where the movie is not found
    return render(request, "detail.html", {'movie': movie})


def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index page after adding a movie

    form = MovieForm()  # Create a new form instance for the GET request
    return render(request, 'add.html', {'form': form})


def update(request, id):
    movie = Movie.objects.get(id=id)
    form = MovieForm(request.POST or None, request.FILES, instance=movie)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index page after updating a movie

    return render(request, 'edit.html', {'form': form, 'movie': movie})


def delete(request, id):
    if request.method == 'POST':
        movie = Movie.objects.get(id=id)
        movie.delete()
        return redirect('index')  # Redirect to the index page after deleting a movie

    return render(request, 'delete.html')
