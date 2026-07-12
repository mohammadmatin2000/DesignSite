from django.db import models
# ======================================================================================================================
# مدل اعضای تیم
class TeamModels(models.Model):

    # نام و نام خانوادگی
    full_name = models.CharField(max_length=255)

    # سمت
    position = models.CharField(max_length=255)

    # تصویر
    image = models.ImageField(upload_to="image/")

    # درباره عضو
    description = models.TextField()

    # ایمیل
    email = models.EmailField()

    # شماره تماس
    phone = models.CharField(max_length=20)

    # آدرس
    address = models.CharField(max_length=255)

    # مهارت اول
    skill_one = models.CharField(max_length=100)
    skill_one_percent = models.PositiveIntegerField(default=0)

    # مهارت دوم
    skill_two = models.CharField(max_length=100)
    skill_two_percent = models.PositiveIntegerField(default=0)

    # مهارت سوم
    skill_three = models.CharField(max_length=100)
    skill_three_percent = models.PositiveIntegerField(default=0)

    # نمایش در سایت
    is_active = models.BooleanField(default=True)

    # تاریخ ایجاد
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "عضو تیم"
        verbose_name_plural = "اعضای تیم"

    # نمایش نام عضو
    def __str__(self):
        return self.full_name


# ======================================================================================================================