from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from myapp.form import EmployeeForm
from myapp.models import Employee


@login_required
def createEmp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee added successfully.")
            return redirect("show")
    else:
        form = EmployeeForm()
    return render(request, "employee/index.html", {"form": form})


@login_required
def show(request):
    query = request.GET.get("q", "").strip()
    employees = Employee.objects.all()
    if query:
        employees = employees.filter(
            Q(eid__icontains=query)
            | Q(ename__icontains=query)
            | Q(eemail__icontains=query)
            | Q(econtact__icontains=query)
        )
    employees = employees.order_by("ename", "id")
    page_obj = Paginator(employees, 10).get_page(request.GET.get("page"))
    return render(
        request,
        "employee/show.html",
        {
            "employees": page_obj,
            "page_obj": page_obj,
            "search_query": query,
            "employee_count": Employee.objects.count(),
            "result_count": page_obj.paginator.count,
        },
    )


@login_required
def edit(request, id):
    employee = get_object_or_404(Employee, id=id)
    form = EmployeeForm(instance=employee)
    return render(
        request, "employee/edit.html", {"employee": employee, "form": form}
    )


@login_required
def update(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee details updated.")
            return redirect("show")
    else:
        form = EmployeeForm(instance=employee)
    return render(
        request, "employee/edit.html", {"employee": employee, "form": form}
    )


@login_required
def destroy(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method != "POST":
        return HttpResponseForbidden("Employee records can only be deleted by POST.")
    employee.delete()
    messages.success(request, "Employee record deleted.")
    return redirect("show")


def can_manage_accounts(user):
    return (
        user.is_authenticated
        and (user.is_superuser or user.groups.filter(name="Account Managers").exists())
    )


@login_required
def register_staff(request):
    if not can_manage_accounts(request.user):
        return HttpResponseForbidden(
            "You are not authorised to create staff accounts."
        )

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = False
            user.is_superuser = False
            user.save()
            messages.success(request, "Staff account created successfully.")
            return redirect("show")
    else:
        form = UserCreationForm()
    return render(request, "registration/register_staff.html", {"form": form})
