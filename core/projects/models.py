from django.db import models
from django.utils.text import slugify
# ======================================================================================================================
# ذخیره دسته‌بندی‌های پروژه‌ها (مسکونی، تجاری، اداری و ...)
class ProjectCategoryModel(models.Model):

    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "دسته‌بندی پروژه"
        verbose_name_plural = "دسته‌بندی های پروژه"

    def __str__(self):
        return self.title
# ======================================================================================================================
# ذخیره اطلاعات کامل هر پروژه (لیست + جزئیات در یک مدل)
class ProjectModel(models.Model):

    # عنوان پروژه
    title = models.CharField(max_length=255)

    # آدرس یکتای پروژه برای استفاده در URL
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)

    # دسته‌بندی اصلی (نمایش در کارت لیست)
    category = models.ForeignKey(
        ProjectCategoryModel,
        on_delete=models.CASCADE,
        related_name="projects_list",
        verbose_name="دسته‌بندی اصلی"
    )

    # دسته‌بندی‌های اضافه (اختیاری - برای چند تگ روی هر کارت)
    extra_categories = models.ManyToManyField(
        ProjectCategoryModel,
        related_name="projects_extra",
        blank=True,
        verbose_name="دسته‌بندی‌های اضافه"
    )

    # موقعیت جغرافیایی پروژه
    location = models.CharField(max_length=255, verbose_name="موقعیت")

    # سال اجرای پروژه
    year = models.PositiveIntegerField(verbose_name="سال")

    # تصویر شاخص پروژه (کارت لیست)
    image = models.ImageField(upload_to="images/", verbose_name="تصویر شاخص")

    # توضیحات کوتاه پروژه (کارت لیست)
    description = models.TextField(blank=True, verbose_name="توضیح کوتاه لیست")

    # -------------------- اطلاعات متا صفحه جزئیات --------------------

    # نام کارفرما / مشتری
    client = models.CharField(max_length=255, blank=True, verbose_name="مشتری")

    # نوع پروژه
    project_type = models.CharField(max_length=255, blank=True, verbose_name="نوع پروژه")

    # معمار پروژه
    architect = models.CharField(max_length=255, blank=True, verbose_name="معمار")

    # مدت زمان پروژه (مثال: 6 ماه)
    duration = models.CharField(max_length=100, blank=True, verbose_name="شرایط (مدت زمان)")

    # استراتژی طراحی (مثال: مینیمالیست)
    strategy = models.CharField(max_length=255, blank=True, verbose_name="استراتژی")

    # تاریخ نمایشی (چون تو نمونه به‌صورت متنی فارسی است، نه DateField)
    display_date = models.CharField(max_length=100, blank=True, verbose_name="تاریخ نمایشی")

    # -------------------- بخش «طراحی با جزئیات» --------------------

    # توضیحات کلی صفحه‌ی جزئیات
    short_description = models.TextField(blank=True, verbose_name="توضیح کوتاه جزئیات")

    # -------------------- ویژگی‌های پروژه (ستون اول - ۳ آیتم) --------------------

    feature_one_title = models.CharField(max_length=255, blank=True, verbose_name="ویژگی ۱ - عنوان")
    feature_one_desc = models.TextField(blank=True, verbose_name="ویژگی ۱ - توضیح")

    feature_two_title = models.CharField(max_length=255, blank=True, verbose_name="ویژگی ۲ - عنوان")
    feature_two_desc = models.TextField(blank=True, verbose_name="ویژگی ۲ - توضیح")

    feature_three_title = models.CharField(max_length=255, blank=True, verbose_name="ویژگی ۳ - عنوان")
    feature_three_desc = models.TextField(blank=True, verbose_name="ویژگی ۳ - توضیح")

    # -------------------- ویژگی‌های پروژه (ستون دوم - ۲ آیتم) --------------------

    feature_four_title = models.CharField(max_length=255, blank=True, verbose_name="ویژگی ۴ - عنوان")
    feature_four_desc = models.TextField(blank=True, verbose_name="ویژگی ۴ - توضیح")

    feature_five_title = models.CharField(max_length=255, blank=True, verbose_name="ویژگی ۵ - عنوان")
    feature_five_desc = models.TextField(blank=True, verbose_name="ویژگی ۵ - توضیح")

    # -------------------- باکس‌های آماری (۴ تا) --------------------

    stat_one_value = models.CharField(max_length=100, blank=True, verbose_name="آمار ۱ - مقدار")
    stat_one_label = models.CharField(max_length=100, blank=True, verbose_name="آمار ۱ - برچسب")

    stat_two_value = models.CharField(max_length=100, blank=True, verbose_name="آمار ۲ - مقدار")
    stat_two_label = models.CharField(max_length=100, blank=True, verbose_name="آمار ۲ - برچسب")

    stat_three_value = models.CharField(max_length=100, blank=True, verbose_name="آمار ۳ - مقدار")
    stat_three_label = models.CharField(max_length=100, blank=True, verbose_name="آمار ۳ - برچسب")

    stat_four_value = models.CharField(max_length=100, blank=True, verbose_name="آمار ۴ - مقدار")
    stat_four_label = models.CharField(max_length=100, blank=True, verbose_name="آمار ۴ - برچسب")

    # -------------------- بخش «نتیجه باور نکردنی» --------------------

    result_description = models.TextField(blank=True, verbose_name="نتیجه پروژه")

    # تاریخ ایجاد
    created_date = models.DateTimeField(auto_now_add=True)

    # تاریخ آخرین بروزرسانی
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
# ======================================================================================================================