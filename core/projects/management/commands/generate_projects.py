import random
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from projects.models import ProjectCategoryModel, ProjectModel
# ======================================================================================================================
# دستور مدیریتی برای ساخت داده‌های ساختگی (فیک) برای پروژه‌ها
# اجرا با: python manage.py generate_projects
# یا با تعداد دلخواه: python manage.py generate_projects --count 12
class Command(BaseCommand):

    help = "ساخت دسته‌بندی و پروژه‌های ساختگی برای تست بخش نمونه کارها"

    # تعریف آرگومان اختیاری برای تعداد پروژه‌ها
    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=12,
            help="تعداد پروژه‌هایی که باید ساخته شود (پیش‌فرض: 12)",
        )

    # پیدا کردن مسیر پوشه‌ی عکس‌ها (کنار همین فایل دستور)
    def get_images_folder(self):
        return Path(__file__).resolve().parent / "images"

    # لیست تمام فایل‌های عکس موجود در پوشه
    def get_image_files(self):
        images_folder = self.get_images_folder()

        if not images_folder.exists():
            raise FileNotFoundError(f"پوشه‌ی عکس‌ها پیدا نشد: {images_folder}")

        valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
        image_files = [
            f for f in images_folder.iterdir()
            if f.is_file() and f.suffix.lower() in valid_extensions
        ]

        if not image_files:
            raise FileNotFoundError(f"هیچ فایل عکسی داخل پوشه پیدا نشد: {images_folder}")

        return image_files

    # انتخاب یک عکس تصادفی از پوشه و بازگرداندن آن به‌صورت ContentFile
    def get_random_image(self, image_files, name_prefix="project"):
        chosen_file = random.choice(image_files)

        with open(chosen_file, "rb") as f:
            content = f.read()

        extension = chosen_file.suffix
        new_name = f"{slugify(name_prefix)}-{random.randint(1000, 9999)}{extension}"

        return ContentFile(content, name=new_name)

    # اجرای اصلی دستور
    def handle(self, *args, **options):
        count = options["count"]

        fake = Faker("fa_IR")

        image_files = self.get_image_files()
        self.stdout.write(self.style.SUCCESS(f"تعداد {len(image_files)} عکس در پوشه پیدا شد."))

        # ----------------------------------------------------------------
        # ساخت دسته‌بندی‌های ثابت (اگر از قبل وجود نداشته باشند)
        category_names = ["مسکونی", "تجاری", "اداری", "خانه ویلایی", "آپارتمانی", "فضای عمومی"]
        categories = []

        for name in category_names:
            category, created = ProjectCategoryModel.objects.get_or_create(title=name)
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f"دسته‌بندی ساخته شد: {name}"))

        # ----------------------------------------------------------------
        # لیست شهرهای فارسی برای فیلد موقعیت
        locations = [
            "تهران، ایران", "شیراز، ایران", "اصفهان، ایران", "مشهد، ایران",
            "تبریز، ایران", "کیش، ایران", "رشت، ایران", "کرج، ایران",
        ]

        # لیست استراتژی‌های طراحی
        strategies = ["مینیمالیستی", "مدرن", "کلاسیک", "صنعتی", "اسکاندیناوی", "بوهو"]

        # ----------------------------------------------------------------
        # ساخت پروژه‌های ساختگی
        for i in range(count):

            # ساخت عنوان فارسی طبیعی برای پروژه (بدون استفاده از catch_phrase که فقط انگلیسی است)
            title = fake.sentence(nb_words=5).rstrip(".")

            main_category = random.choice(categories)

            project = ProjectModel(
                title=title,
                category=main_category,
                location=random.choice(locations),
                year=random.randint(1398, 1405),
                description=fake.paragraph(nb_sentences=2),

                # اطلاعات متا صفحه جزئیات
                client=fake.name(),
                project_type=main_category.title,
                architect=fake.name(),
                duration=f"{random.randint(2, 12)} ماه",
                strategy=random.choice(strategies),
                display_date=f"{random.randint(1, 29)} {random.choice(['فروردین', 'خرداد', 'مرداد', 'مهر', 'دی'])} {random.randint(1398, 1405)}",

                # بخش «طراحی با جزئیات»
                short_description=fake.paragraph(nb_sentences=4),

                # ویژگی‌های پروژه (ستون اول)
                feature_one_title="فضای باز",
                feature_one_desc=fake.sentence(nb_words=10),
                feature_two_title="نورپردازی طبیعی",
                feature_two_desc=fake.sentence(nb_words=10),
                feature_three_title="مصالح پایدار",
                feature_three_desc=fake.sentence(nb_words=10),

                # ویژگی‌های پروژه (ستون دوم)
                feature_four_title="چیدمان هوشمند",
                feature_four_desc=fake.sentence(nb_words=10),
                feature_five_title="طراحی سفارشی",
                feature_five_desc=fake.sentence(nb_words=10),

                # باکس‌های آماری
                stat_one_value=f"{random.randint(80, 500)}",
                stat_one_label="متر مربع",
                stat_two_value=f"{random.randint(2, 10)}",
                stat_two_label="اتاق",
                stat_three_value=f"{random.randint(1, 5)}",
                stat_three_label="طبقه",
                stat_four_value=f"{random.randint(2, 12)}",
                stat_four_label="ماه اجرا",

                # بخش «نتیجه باور نکردنی»
                result_description=fake.paragraph(nb_sentences=3),
            )

            # انتخاب و اتصال یک عکس تصادفی واقعی از پوشه
            random_image_file = self.get_random_image(image_files, name_prefix=title)
            project.image.save(random_image_file.name, random_image_file, save=False)

            project.save()

            # اضافه کردن ۰ تا ۲ دسته‌بندی اضافه (متفاوت از دسته‌بندی اصلی)
            other_categories = [c for c in categories if c != main_category]
            if other_categories:
                extra_count = random.randint(0, min(2, len(other_categories)))
                project.extra_category.set(random.sample(other_categories, k=extra_count))

            self.stdout.write(self.style.SUCCESS(f"پروژه ساخته شد: {title}"))

        self.stdout.write(self.style.SUCCESS(f"\n✅ تعداد {count} پروژه با موفقیت ساخته شد."))
# ======================================================================================================================