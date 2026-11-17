from django.test import RequestFactory, TestCase
from .alumniadmin_views import alumni_students_list


class AlumniStudentsListTests(TestCase):
    def test_search_uses_department_name_field(self):
        request = RequestFactory().post(
            "/alumni_admin/alumni_students_list",
            {"query": "engineering"},
        )

        response = alumni_students_list(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
