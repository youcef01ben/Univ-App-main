from django.shortcuts import render,redirect
from .importExcel import importExcel 
from .models import Etudiant,Verifier, Domaine, Filiere
from django.contrib import messages
from .forms import DomaineForm, FiliereForm
from .filters import EtudiantFilter, VerifierFilter
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, permission_required
import os
from django.core.files.storage import default_storage
from django.http import JsonResponse

@login_required(login_url='/login/')
def dashboard(request):
    table_header = ['Mat. Etudiant',
                    'Nom',
                    'Prénom',
                    'Date de naiss.',
                    'Code domaine',
                    'Code filière',
                    'Code niveau',
                    'Date de l\'examen',
                    'Heure de l\'examen']
    records = VerifierFilter(request.GET, queryset=Verifier.objects.all())
    print(request.user.has_perm("base.add_domaine"))
    context={
        'records':records,
        'header':table_header,
        'admin': request.user.groups.filter(name='admins').exists(),
        'stuff':request.user.groups.filter(name='stuff').exists(),
    }
    return render(request, 'base/records.html', context)

@login_required(login_url='/login/')
def student(request):
    table_header = ['Mat. Etudiant',
                    'Nom',
                    'Prénom',
                    'Date de naiss.',
                    'Code domaine',
                    'Code filière',
                    'Code niveau']
    students = EtudiantFilter(request.GET, queryset=Etudiant.objects.all())
    context = {
        'students':students,
        'header':table_header,
        'admin': request.user.groups.filter(name='admins').exists(),
        'stuff':request.user.groups.filter(name='stuff').exists(),
    }
    return render(request, 'base/student.html',context)

@login_required(login_url='/login/')
@permission_required('base.add_etudiant')
def addStudent(request):
    if request.method == 'POST':
        if request.FILES.get('myfile'):
            myfile = request.FILES.get('myfile')
            redir = importExcel(request,myfile)
            if(redir):
                return redirect('base:student')
        else:
            messages.error(request, 'Vous n\'avez pas selction un fichier excel !!! ')
    return render(request, 'base/ajouter-etudiants.html')

@login_required(login_url='/login/')
@permission_required('base.delete_etudiant')
def deleteStudents(request):
    if request.method == 'POST':
        Etudiant.objects.all().delete()
        return redirect('base:student')
    return render(request, 'base/sup_etudiants.html')

@login_required(login_url='/login/')
@permission_required('base.add_domaine')
def addDomaine(request):
    form = DomaineForm()
    if request.method == 'POST':
        try:
            Domaine.objects.create(
                code=request.POST.get('code'),
                nom=request.POST.get('nom')
            )
            return redirect('base:dashboard')
        except IntegrityError as e:
            messages.error(request, 'Le Code <strong>'+str(request.POST.get('code'))+'</strong> est deja existant !!!')
        
    context={
        'form':form
    }
    return render(request, 'base/domaine.html',context)

@login_required(login_url='/login/')
@permission_required('base.add_filiere')
def addFiliere(request):
    form = FiliereForm()
    if request.method == 'POST':
        try:
            Filiere.objects.create(
                code=request.POST.get('code'),
                nom=request.POST.get('nom')
            )
            return redirect('base:dashboard')
        except IntegrityError as e:
            messages.error(request, 'Le Code <strong>'+str(request.POST.get('code'))+'</strong> est deja existant !!!')
        
    context={
        'form':form
    }
    return render(request, 'base/filiere.html',context)


def addImage(request):
    if request.method == 'POST' and request.FILES.get('image'):
            image_file = request.FILES['image']
            file_path = default_storage.save('C:/Users/HP/Desktop/images' + image_file.name, image_file)

            # Obtenez l'URL de l'image en fonction du chemin relatif
            image_url = default_storage.url(file_path)

            return JsonResponse({'image': image_url})
    else:
            return JsonResponse({'message': 'Invalid request.'})
    return render(request, 'home.html')

