from django.shortcuts import redirect



def api_root(request):
    return redirect('api-root')

def rest_framework(request):
    return redirect('rest_framework')