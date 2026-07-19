import random
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from faker import Faker
from team.models import TeamModels
# ======================================================================================================================
# دستور مدیریتی برای ساخت داده‌های ساختگی (فیک) برای اعضای تیم
# اجرا با: python manage.py generate_teams
# یا با تعداد دلخواه: python manage.py generate_teams --count 8
class Command(BaseCommand):

    help = "ساخت اعضای تیم ساختگی برای تست بخش تیم"

    # تعریف آرگومان اختیاری برای تعداد اعضا
    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=8,
            help="تعداد اعضایی که باید ساخته شود (پیش‌فرض: 8)",
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
    def get_random_image(self, image_files, name_prefix="team"):
        chosen_file = random.choice(image_files)

        with open(chosen_file, "rb") as f:
            content = f.read()

        extension = chosen_file.suffix
        new_name = f"{name_prefix}-{random.randint(1000, 9999)}{extension}"

        return ContentFile(content, name=new_name)

    # اجرای اصلی دستور
    def handle(self, *args, **options):
        count = options["count"]

        fake = Faker("fa_IR")

        image_files = self.get_image_files()
        self.stdout.write(self.style.SUCCESS(f"تعداد {len(image_files)} عکس در پوشه پیدا شد."))

        # ----------------------------------------------------------------
        # لیست سمت‌های شغلی
        positions = [
            "طراح داخلی ارشد", "معمار", "مدیر پروژه", "طراح فضای سبز",
            "کارشناس نورپردازی", "مدل‌ساز سه‌بعدی", "مدیر هنری", "مشاور طراحی",
        ]

        # لیست مهارت‌های احتمالی
        possible_skills = [
            "طراحی داخلی", "مدل سازی سه بعدی", "برنامه ریزی فضایی",
            "نورپردازی", "مدیریت پروژه", "طراحی پایدار", "رندرینگ",
            "طراحی مبلمان", "معماری منظر", "مشاوره رنگ",
        ]

        # ----------------------------------------------------------------
        # ساخت اعضای تیم ساختگی
        for i in range(count):

            full_name = fake.name()
            skills = random.sample(possible_skills, k=3)

            # آیا این عضو مدیر شرکته؟ (فقط اولین عضو ساخته‌شده مدیر باشه، اختیاری)
            is_manager = (i == 0)

            member = TeamModels(
                full_name=full_name,
                position=random.choice(positions),
                description=fake.paragraph(nb_sentences=3),
                email=fake.email(),
                phone=f"09{random.randint(100000000, 999999999)}",
                address=fake.address(),

                # مهارت اول
                skill_one=skills[0],
                skill_one_percent=random.randint(60, 99),

                # مهارت دوم
                skill_two=skills[1],
                skill_two_percent=random.randint(60, 99),

                # مهارت سوم
                skill_three=skills[2],
                skill_three_percent=random.randint(60, 99),

                is_manager=is_manager,
                manager_quote=fake.paragraph(nb_sentences=2) if is_manager else None,

                is_active=True,
            )

            # انتخاب و اتصال یک عکس تصادفی واقعی از پوشه
            random_image_file = self.get_random_image(image_files, name_prefix=full_name)
            member.image.save(random_image_file.name, random_image_file, save=False)

            member.save()

            self.stdout.write(self.style.SUCCESS(f"عضو تیم ساخته شد: {full_name}"))

        self.stdout.write(self.style.SUCCESS(f"\n✅ تعداد {count} عضو تیم با موفقیت ساخته شد."))
# ======================================================================================================================