# from django.shortcuts import render, get_object_or_404
# from .models import Doctor

# def doctors_list_page(request):
#     doctors = Doctor.objects.all()
#     return render(request, "doctors_list.html", {"doctors": doctors})


# def doctor_detail_page(request, pk):
#     doctor = get_object_or_404(Doctor, pk=pk)
#     return render(request, "doctor_detail.html", {"doctor": doctor})
