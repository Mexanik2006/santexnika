from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import AccountForm

@login_required
def client_list(request):
    clients = Account.objects.all()
    return render(request, "client/clientlist.html", {"clients": clients})

@login_required
def client_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientlist')
    else:
        form = AccountForm()
    
    return render(request, "client/clientform.html", {
        "form": form,
        "title": "Yangi mijoz yaratish",
        "action": "clientcreate"
    })

@login_required
def client_view(request, id):
    client = get_object_or_404(Account, id=id)
    return render(request, "client/clientview.html", {"client": client})

@login_required
def client_edit(request, id):
    client = get_object_or_404(Account, id=id)
    
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clientlist')
    else:
        form = AccountForm(instance=client)
    
    return render(request, "client/clientform.html", {
        "form": form,
        "title": "Mijozni tahrirlash",
        "action": "clientedit",
        "client": client
    })

@login_required
def client_delete(request, id):
    client = get_object_or_404(Account, id=id)
    
    if request.method == 'POST':
        client.delete()
        return redirect('clientlist')
    
    return render(request, "client/clientdelete.html", {"client": client})