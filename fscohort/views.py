from typing import List
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import StudentForm
from .models import Student
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic import DeleteView

# Create your views here.
# class yapısı home page
class HomeView(TemplateView):
    template_name = "fscohort/home.html"
    
# Function yapısı home page
def home(request):
    return render(request, "fscohort/home.html")
    
#* /////////////////////////////////

class StudentList(ListView):
    model = Student
    context_object_name = 'students'
    # queryset = Student.objects.filter(first_name = 'ali')
    
    def get_queryset(self):
        return super().get_queryset()

def student_list(request):

    students = Student.objects.all()

    context = {
        "students":students
    }

    return render(request, "fscohort/student_list.html", context)

#* /////////////////////////////////

class StudentDetailView(DetailView):
    model = Student
    pk_url_kwarg = 'slug'
    
def student_detail(request,id):
    student = Student.objects.get(id=id)
    context = {
        "student":student
    }

    return render(request, "fscohort/student_detail.html", context)

#* /////////////////////////////////

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "fscohort/student_add.html"
    success_url = reverse_lazy('list')
    
    def form_valid(self, form):
        self.object = form.save()
        if not self.object.number:
            self.object.number = 999
        self.object.save()
        return super().form_valid(form)


def student_add(request):
    form = StudentForm()

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/list/")


    context = {

       "form":form
    }

    return render(request, "fscohort/student_add.html", context)

#* /////////////////////////////////

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "fscohort/student_update.html" # default app/modelname_form.html
    success_url = reverse_lazy('list')
    # pk_url_kwarg = 'id'

def student_update(request, id):

    student = Student.objects.get(id=id)

    form = StudentForm(instance=student)

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("list")

    context= {

        "student":student,
        "form":form
    }

    return render(request, "fscohort/student_update.html", context)

#* ///////////////////////////////

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'fscohort/student_delete.html'
    success_url= reverse_lazy('list')

def student_delete(request, id):
    student = Student.objects.get(id=id)
    if request.method == "POST":
        student.delete()
        return redirect("list")

    context= {
        "student":student
    }

    return render(request, "fscohort/student_delete.html",context)
