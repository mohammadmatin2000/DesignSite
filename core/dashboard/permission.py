from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.models import UserType
# ======================================================================================================================
# دسترسی مخصوص کاربران مشتری (Customer)
class HasCustomerPermission(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.type == UserType.customer.value
        return False
# ======================================================================================================================
# دسترسی مخصوص کاربران ادمین و سوپریوزر
class HasAdminPermission(UserPassesTestMixin):

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.type in (
                UserType.admin,
                UserType.superuser,
            )
        )
# ======================================================================================================================