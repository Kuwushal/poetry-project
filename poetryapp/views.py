import requests
from django.shortcuts import render
from django.core.paginator import Paginator


def home(request):
    return render(request, 'poetryapp/home.html')  


def search_poem(request):
    query = request.GET.get('q', '')  
    poems = []

    if query:
        # Try author search
        url = f"https://poetrydb.org/author/{query}"
        response = requests.get(url)
        data = response.json()

        # Only use data if it's a list (valid poems)
        if isinstance(data, list):
            poems = data
        else:
            # Try title search
            url = f"https://poetrydb.org/title/{query}"
            response = requests.get(url)
            data = response.json()
            if isinstance(data, list):
                poems = data

    # Pagination logic
    paginator = Paginator(poems, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'poetryapp/search_results.html', {
        'poems': page_obj,
        'query': query
    })

def poem_detail(request, title):
    # Assuming the API returns a list with the poem details
    url = f"https://poetrydb.org/title/{title}"
    response = requests.get(url)
    poem = response.json()

    if not poem:
        return render(request, 'poetryapp/poem_not_found.html', {'title': title})

    return render(request, 'poetryapp/poem_detail.html', {'poem': poem[0]})



def write_poem(request):
    return render(request, 'poetryapp/write_poem.html')