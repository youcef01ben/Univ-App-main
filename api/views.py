import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VerifierSerializer, EtudiantSerializer
from base.models import Domaine, Verifier ,Etudiant,Filiere

@api_view(['GET'])
def getStudent(request,mat):
    student = Etudiant.objects.get(mat=mat)   
    serializer = EtudiantSerializer(student, many=False)
    
    #print (type(serializer.data))
    student_1 = json.dumps(serializer.data)
    newData = {"filiereNom":str(student.filiere),"domaineNom":str(student.domaine)}
    student_1 = json.loads(student_1)
    student_1.update(newData)
    student2 = json.dumps(student_1)
    print(student_1)
    
    
    return Response(json.loads(student2))

@api_view(['POST'])
def createRecord(request):
    serializer = VerifierSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
