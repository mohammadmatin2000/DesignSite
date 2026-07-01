from django.core.exceptions import ValidationError
import re
# ======================================================================================================================
# اعتبارسنجی شماره موبایل ایران (شروع با 09 و شامل 11 رقم)
def validate_iranian_cellphone_number(value):
    pattern = r"^09\d{9}$"
    if not re.match(pattern, value):
        raise ValidationError("Enter a valid Iranian cellphone number.")
# ======================================================================================================================