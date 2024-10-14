from django.shortcuts import render

# Create your views here.

def home_screen_view(request):
    
    # context = {}
    # context['something'] = "This is some string that I am passing to the view"
    # context['some_number'] = 99999
    
    # context = {
    #     "some_text": "This is some text",
    #     "some_number": 123,
    #     "some_list": [1, 2, 3, 4],
    # }

    list_of_values = []
    list_of_values.append("First entry")
    list_of_values.append("Second entry")
    list_of_values.append("Third entry")
    list_of_values.append("Fourth entry")
    context = { "list_of_values" : list_of_values }

    
    return render(request, "personal/home.html", context)