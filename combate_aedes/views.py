from django.shortcuts import render

# Crie suas visualizações aqui.

# Exibe página princibal do sistema
def home(request):
    return render(request, 'home.html')