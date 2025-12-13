from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy

class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    A robust mixin that ensures the user is logged in AND belongs to specific Groups.
    It provides UI feedback (Flash Messages) instead of a generic 403 error page.
    """
    required_roles = []  # Define in subclass: e.g. ['Teacher', 'Principal']
    permission_denied_message = "You do not have the required role to access this area."
    redirect_on_fail = 'dashboard'  # Name of the URL to redirect to on failure

    def get_required_roles(self):
        """
        Normalizes required_roles to a list, even if a single string is passed.
        Raises an error if the developer forgot to set roles.
        """
        if self.required_roles is None or (isinstance(self.required_roles, list) and not self.required_roles):
             raise ImproperlyConfigured(
                f'{self.__class__.__name__} is missing the "required_roles" attribute. '
                f'Define it as a list of Group names, e.g., required_roles = ["Teacher"]'
            )
        
        if isinstance(self.required_roles, str):
            return [self.required_roles]
        
        return self.required_roles

    def test_func(self):
        """
        The logic that determines True (Access Granted) or False (Access Denied).
        """
        user = self.request.user
        
        # 1. Ensure user is active (standard security check)
        if not user.is_active:
            return False

        # 2. Superusers (Devs/Admins) should always have access
        if user.is_superuser:
            return True

        # 3. Check if the user belongs to ANY of the required groups
        roles = self.get_required_roles()
        return user.groups.filter(name__in=roles).exists()

    def handle_no_permission(self):
        """
        Custom handling when test_func returns False.
        Instead of a 403 Page, we give a nice error message and redirect.
        """
        # Case A: User is not logged in at all -> Send to Login
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        # Case B: User is logged in but lacks permissions -> Send Flash Message + Redirect
        messages.error(self.request, self.permission_denied_message)
        
        # Try to redirect to the configured fallback url (e.g., 'dashboard')
        # If the URL name doesn't exist, it falls back to the homepage '/'
        try:
            return redirect(self.redirect_on_fail)
        except:
            return redirect('/')

# --- Pre-configured Mixins for Clean Views ---

class AdminRequiredMixin(RoleRequiredMixin):
    required_roles = ['Admin', 'Principal']
    permission_denied_message = "Restricted: Administrative access only."

class TeacherRequiredMixin(RoleRequiredMixin):
    required_roles = ['Teacher', 'Admin'] # Admins usually can act as Teachers
    permission_denied_message = "Restricted: Teacher access only."

class FinanceRequiredMixin(RoleRequiredMixin):
    required_roles = ['Bursar', 'Accountant', 'Admin']
    permission_denied_message = "Restricted: Finance Department only."