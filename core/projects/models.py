from django.db import models
# ======================================================================================================================
# ذخیره دسته‌بندی‌های پروژه‌ها (مسکونی، تجاری، اداری و ...)
class ProjectCategoryModel(models.Model):

    # عنوان دسته‌بندی
    title = models.CharField(max_length=255)

    # نمایش عنوان دسته‌بندی در پنل مدیریت
    def __str__(self):
        return self.title
# ======================================================================================================================
# ذخیره اطلاعات کلی پروژه‌ها
class ProjectModel(models.Model):

    # عنوان پروژه
    title = models.CharField(max_length=255)

    # دسته‌بندی پروژه
    category = models.ForeignKey(
        ProjectCategoryModel,
        on_delete=models.CASCADE,
        related_name='projects_list'
    )

    # موقعیت جغرافیایی پروژه
    location = models.CharField(max_length=255)

    # سال اجرای پروژه
    year = models.PositiveIntegerField()

    # تصویر شاخص پروژه
    image = models.ImageField(upload_to='images/')

    # توضیحات کوتاه پروژه
    description = models.TextField(blank=True)

    # تاریخ ایجاد پروژه
    created_date = models.DateTimeField(auto_now_add=True)

    # تاریخ آخرین بروزرسانی پروژه
    updated_date = models.DateTimeField(auto_now=True)

    # نمایش عنوان پروژه در پنل مدیریت
    def __str__(self):
        return self.title
# ======================================================================================================================
# ذخیره اطلاعات و جزئیات کامل هر پروژه
class ProjectDetailModels(models.Model):

    # عنوان پروژه
    title = models.CharField(max_length=255)

    # آدرس یکتای پروژه برای استفاده در URL
    slug = models.SlugField(unique=True)

    # دسته‌بندی‌های مرتبط با پروژه
    categories = models.ManyToManyField(
        "ProjectCategoryModel",
        related_name="projects_details",
    )

    # تصویر اصلی پروژه
    image = models.ImageField(upload_to="projects/")

    # نام کارفرما
    client = models.CharField(
        max_length=255,
        verbose_name="نام کارفرما"
    )

    # نوع پروژه
    project_type = models.CharField(
        max_length=255,
        verbose_name="نوع پروژه"
    )

    # موقعیت جغرافیایی پروژه
    location = models.CharField(
        max_length=255,
        verbose_name="موقعیت"
    )

    # سال اجرای پروژه
    year = models.PositiveIntegerField(
        verbose_name="سال"
    )

    # توضیحات کلی پروژه
    short_description = models.TextField(
        verbose_name="توضیح کوتاه"
    )

    # توضیحات مربوط به نتیجه نهایی پروژه
    result_description = models.TextField(
        verbose_name="نتیجه پروژه"
    )

    # متراژ کل پروژه
    total_area = models.PositiveIntegerField(
        verbose_name="متراژ کل"
    )

    # تعداد اتاق‌های پروژه
    rooms = models.PositiveIntegerField(
        verbose_name="تعداد اتاق"
    )

    # متراژ هر طبقه
    floor_area = models.PositiveIntegerField(
        verbose_name="متراژ هر طبقه"
    )

    # زیربنای پروژه
    building_area = models.PositiveIntegerField(
        verbose_name="زیربنا"
    )

    # تاریخ ایجاد رکورد
    created_date = models.DateTimeField(auto_now_add=True)

    # تاریخ آخرین بروزرسانی رکورد
    updated_date = models.DateTimeField(auto_now=True)

    # نمایش عنوان پروژه در پنل مدیریت
    def __str__(self):
        return self.title
# ======================================================================================================================