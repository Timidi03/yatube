from django.test import TestCase, Client
import datetime as dt
from django.contrib.auth.models import User


class TestTariffPlans(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_home_page_unauthorized_user(self):
        response = self.client.get('/practice/')
        self.assertEqual(response.status_code, 200)
        
    def test_admin_section_for_unauthorized_user(self):
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 200)
        
    def test_plans_variable_in_template_context(self):
        response = self.client.get('/practice/')
        self.assertIn('plans', response.context)
        
    def test_template_name_on_rendering_home_page(self):
        response = self.client.get('/practice/')
        self.assertTemplateUsed(response, 'index1.html')
    
    def test_plans_variable_type(self):
        response = self.client.get('/practice/')
        plans = response.context['plans']
        self.assertIsInstance(plans, list)
        self.assertEqual(len(plans), 3)
        for plan in plans:
            self.assertIsInstance(plan, dict)
            
    def test_tariff_names_and_contact_link_on_page(self):
        response = self.client.get('/practice/')
        pass
    