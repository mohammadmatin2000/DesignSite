from django.db import models
# ======================================================================================================================
# ذخیره خدمات ارائه شده توسط مجموعه
class ServiceModel(models.Model):

    # عنوان خدمت
    title = models.CharField(max_length=255)

    # توضیح کوتاه خدمت
    description = models.TextField()

    # تصویر شاخص خدمت
    image = models.ImageField(
        upload_to="images/"
    )

    # ترتیب نمایش در سایت
    order = models.PositiveIntegerField(
        default=0
    )

    # وضعیت فعال یا غیرفعال بودن خدمت
    is_active = models.BooleanField(
        default=True
    )

    # تاریخ ایجاد
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    # تاریخ آخرین بروزرسانی
    updated_date = models.DateTimeField(
        auto_now=True
    )

    # نمایش عنوان خدمت در پنل مدیریت
    def __str__(self):
        return self.title
# ======================================================================================================================
# ذخیره اطلاعات و جزئیات کامل هر خدمت
class ServiceDetailModel(models.Model):

    # ارتباط یک به یک با سرویس اصلی
    service = models.OneToOneField(
        ServiceModel,
        on_delete=models.CASCADE,
        related_name='detail'
    )

    # آدرس یکتای صفحه
    slug = models.SlugField(unique=True)

    # عنوان صفحه جزئیات
    title = models.CharField(max_length=255)

    # توضیحات ابتدایی خدمت
    description = models.TextField()

    # بخش "در مورد خدمات"
    about_service = models.TextField()

    # بخش "انواع فضاها"
    spaces_description = models.TextField()

    # بخش "عناصر کلیدی"
    key_elements_description = models.TextField()

    # تاریخ ایجاد
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    # تاریخ آخرین بروزرسانی
    updated_date = models.DateTimeField(
        auto_now=True
    )

    # نمایش عنوان خدمت در پنل مدیریت
    def __str__(self):
        return self.title
# ======================================================================================================================
# ذخیره گالری تصاویر هر خدمت
class ServiceGalleryModel(models.Model):

    # ارتباط با جزئیات خدمت
    service = models.ForeignKey(
        ServiceDetailModel,
        on_delete=models.CASCADE,
        related_name='gallery'
    )

    # تصویر مربوط به خدمت
    image = models.ImageField(
        upload_to='images/'
    )

    # نمایش نام خدمت در پنل مدیریت
    def __str__(self):
        return self.service.title
# ======================================================================================================================