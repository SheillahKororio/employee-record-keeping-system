from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Employee


class EmployeeManagementTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="manager", password="secure-test-password"
        )
        self.client.force_login(self.user)
        self.employee = Employee.objects.create(
            eid="EMP-001",
            ename="Avery Jordan",
            eemail="avery@example.com",
            econtact="555-0101",
        )

    def test_dashboard_searches_employee_fields(self):
        response = self.client.get(reverse("show"), {"q": "avery"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Avery Jordan")
        self.assertEqual(response.context["result_count"], 1)

    def test_create_and_update_employee(self):
        create_response = self.client.post(
            reverse("createEmp"),
            {
                "eid": "EMP-002",
                "ename": "Sam Rivera",
                "eemail": "sam@example.com",
                "econtact": "555-0102",
            },
        )
        self.assertRedirects(create_response, reverse("show"))
        self.assertTrue(Employee.objects.filter(eid="EMP-002").exists())

        update_response = self.client.post(
            reverse("update", args=[self.employee.id]),
            {
                "eid": "EMP-001",
                "ename": "Avery Lee",
                "eemail": "avery.lee@example.com",
                "econtact": "555-0101",
            },
        )
        self.assertRedirects(update_response, reverse("show"))
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.ename, "Avery Lee")

    def test_employee_deletion_requires_post(self):
        get_response = self.client.get(
            reverse("destroy", args=[self.employee.id])
        )
        self.assertEqual(get_response.status_code, 403)
        self.assertTrue(Employee.objects.filter(pk=self.employee.pk).exists())

        post_response = self.client.post(
            reverse("destroy", args=[self.employee.id])
        )
        self.assertRedirects(post_response, reverse("show"))
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())

    def test_employee_pages_require_login(self):
        self.client.logout()

        response = self.client.get(reverse("show"))

        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('show')}"
        )
