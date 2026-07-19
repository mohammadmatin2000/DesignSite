import random
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from services.models import ServiceModel, ServiceGalleryModel
# ======================================================================================================================
# دستور مدیریتی برای ساخت داده‌های ساختگی (فیک) برای خدمات
# اجرا با: python manage.py generate_services
# یا با تعداد دلخواه: python manage.py generate_services --count 6 --gallery 4
class Command(BaseCommand):

    help = "ساخت خدمات ساختگی به همراه گالری تصاویر هرکدام"

    # تعریف آرگومان‌های اختیاری
    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=6,
            help="تعداد خدماتی که باید ساخته شود (پیش‌فرض: 6)",
        )
        parser.add_argument(
            "--gallery",
            type=int,
            default=4,
            help="حداکثر تعداد تصویر گالری برای هر خدمت (پیش‌فرض: 4)",
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
    def get_random_image(self, image_files, name_prefix="service"):
        chosen_file = random.choice(image_files)

        with open(chosen_file, "rb") as f:
            content = f.read()

        extension = chosen_file.suffix
        new_name = f"{slugify(name_prefix)}-{random.randint(1000, 9999)}{extension}"

        return ContentFile(content, name=new_name)

    # اجرای اصلی دستور
    def handle(self, *args, **options):
        count = options["count"]
        max_gallery = options["gallery"]

        fake = Faker("fa_IR")

        image_files = self.get_image_files()
        self.stdout.write(self.style.SUCCESS(f"تعداد {len(image_files)} عکس در پوشه پیدا شد."))

        # ----------------------------------------------------------------
        # عناوین ثابت و معنادار برای خدمات (به‌جای عنوان کاملاً رندوم)
        service_titles = [
            "طراحی داخلی مسکونی",
            "طراحی فضای تجاری",
            "طراحی فضای اداری",
            "مشاوره و برنامه‌ریزی فضا",
            "بازسازی و نوسازی",
            "طراحی سه بعدی و تجسم",
            "طراحی نورپردازی",
            "انتخاب مبلمان و دکوراسیون",
            "طراحی چیدمان فضای باز",
            "مدیریت پروژه ساخت",
        ]

        # اگر تعداد درخواستی بیشتر از عناوین ثابت بود، از عنوان‌های فیک هم استفاده می‌کنیم
        titles_to_use = service_titles[:count] if count <= len(service_titles) else (
            service_titles + [fake.sentence(nb_words=4).rstrip(".") for _ in range(count - len(service_titles))]
        )

        # ----------------------------------------------------------------
        # ساخت خدمات ساختگی
        for i, title in enumerate(titles_to_use):

            service = ServiceModel(
                title=title,
                description=fake.paragraph(nb_sentences=2),
                about_service=fake.paragraph(nb_sentences=4),
                spaces_description=fake.paragraph(nb_sentences=3),
                key_elements_description=fake.paragraph(nb_sentences=3),
                order=i,
                is_active=True,
            )

            # انتخاب و اتصال یک عکس تصادفی واقعی از پوشه (تصویر شاخص)
            random_image_file = self.get_random_image(image_files, name_prefix=title)
            service.image.save(random_image_file.name, random_image_file, save=False)

            service.save()

            self.stdout.write(self.style.SUCCESS(f"خدمت ساخته شد: {title}"))

            # --------------------------------------------------------
            # ساخت گالری تصاویر برای همین خدمت
            gallery_count = random.randint(1, max_gallery)

            for _ in range(gallery_count):
                gallery_image_file = self.get_random_image(image_files, name_prefix=f"{title}-gallery")

                gallery_item = ServiceGalleryModel(service=service)
                gallery_item.image.save(gallery_image_file.name, gallery_image_file, save=False)
                gallery_item.save()

            self.stdout.write(self.style.SUCCESS(f"  └─ {gallery_count} تصویر گالری برای این خدمت ساخته شد"))

        self.stdout.write(self.style.SUCCESS(f"\n✅ تعداد {len(titles_to_use)} خدمت (همراه با گالری) با موفقیت ساخته شد."))
# ======================================================================================================================