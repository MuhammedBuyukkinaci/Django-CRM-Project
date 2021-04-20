from django.test import TestCase
from django.shortcuts import reverse

# Create your tests here.

class LandingPageTest(TestCase):

    def test_status_code(self):
        # To do some sort of test
        response = self.client.get(reverse("landing-page"))
        # print(response.content)
        print(response.status_code)
        self.assertEqual(response.status_code,200)# Expected 200 as status_code

    def test_template_name(self):
        response = self.client.get(reverse("landing-page"))
        self.assertTemplateUsed(response,"landing.html") # Expected landing.html as template
        pass