from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        labels = {
            "eid": "Employee ID",
            "ename": "Full name",
            "eemail": "Work email",
            "econtact": "Phone number",
        }
        widgets = {
            "eid": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. EMP-104"}),
            "ename": forms.TextInput(attrs={"class": "form-control", "placeholder": "Employee full name"}),
            "eemail": forms.EmailInput(attrs={"class": "form-control", "placeholder": "name@company.com"}),
            "econtact": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
        }