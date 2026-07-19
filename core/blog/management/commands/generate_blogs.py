import random
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from blog.models import BlogModels, CategoryModels, TagModel, CommentModel
# ======================================================================================================================
# دستور مدیریتی برای ساخت داده‌های ساختگی (فیک) برای وبلاگ
# اجرا با: python manage.py generate_blog
# یا با تعداد دلخواه: python manage.py generate_blog --count 20
class Command(BaseCommand):

    help = "ساخت دسته‌بندی، برچسب، مقالات و نظرات ساختگی برای تست وبلاگ"

    # تعریف آرگومان‌های اختیاری
    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="تعداد مقالاتی که باید ساخته شود (پیش‌فرض: 10)",
        )
        parser.add_argument(
            "--comments",
            type=int,
            default=5,
            help="حداکثر تعداد نظر برای هر مقاله (پیش‌فرض: 5)",
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
    def get_random_image(self, image_files, name_prefix="blog"):
        chosen_file = random.choice(image_files)

        with open(chosen_file, "rb") as f:
            content = f.read()

        extension = chosen_file.suffix
        new_name = f"{slugify(name_prefix)}-{random.randint(1000, 9999)}{extension}"

        return ContentFile(content, name=new_name)

    # اجرای اصلی دستور
    def handle(self, *args, **options):
        count = options["count"]
        max_comments = options["comments"]

        # استفاده از لوکال فارسی برای تولید متن‌های واقعی‌تر
        fake = Faker("fa_IR")

        # بارگذاری لیست عکس‌های موجود یک بار، قبل از شروع حلقه
        image_files = self.get_image_files()
        self.stdout.write(self.style.SUCCESS(f"تعداد {len(image_files)} عکس در پوشه پیدا شد."))

        # ----------------------------------------------------------------
        # ساخت دسته‌بندی‌های ثابت (اگر از قبل وجود نداشته باشند)
        category_names = ["طراحی داخلی", "معماری", "دکوراسیون", "نورپردازی", "مبلمان"]
        categories = []

        for name in category_names:
            category, created = CategoryModels.objects.get_or_create(title=name)
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f"دسته‌بندی ساخته شد: {name}"))

        # ----------------------------------------------------------------
        # ساخت برچسب‌های ثابت (اگر از قبل وجود نداشته باشند)
        tag_names = ["مدرن", "کلاسیک", "مینیمال", "لوکس", "چوبی", "رنگی"]
        tags = []

        for name in tag_names:
            tag, created = TagModel.objects.get_or_create(title=name)
            tags.append(tag)
            if created:
                self.stdout.write(self.style.SUCCESS(f"برچسب ساخته شد: {name}"))

        # ----------------------------------------------------------------
        # ساخت مقالات ساختگی به همراه نظرات هرکدام
        for i in range(count):

            title = fake.sentence(nb_words=6).rstrip(".")

            blog = BlogModels(
                title=title,
                category=random.choice(categories),
                short_description=fake.paragraph(nb_sentences=3),
                content="\n\n".join(fake.paragraphs(nb=5)),
                views=random.randint(0, 500),
                status=random.choice(["published", "published", "published", "draft"]),
            )

            random_image_file = self.get_random_image(image_files, name_prefix=title)

            blog.image.save(
                random_image_file.name,
                random_image_file,
                save=False,
            )

            blog.save()

            # اضافه کردن ۱ تا ۳ برچسب تصادفی به هر مقاله
            blog.tags.set(random.sample(tags, k=random.randint(1, 3)))

            self.stdout.write(self.style.SUCCESS(f"مقاله ساخته شد: {title}"))

            # --------------------------------------------------------
            # ساخت نظرات ساختگی برای همین مقاله
            comment_count = random.randint(0, max_comments)

            for _ in range(comment_count):
                CommentModel.objects.create(
                    blog=blog,
                    fullname=fake.name(),
                    email=fake.email(),
                    website=fake.url() if random.choice([True, False]) else None,
                    message=fake.paragraph(nb_sentences=2),
                    is_approved=random.choice([True, True, True, False]),
                )

            if comment_count:
                self.stdout.write(self.style.SUCCESS(f"  └─ {comment_count} نظر برای این مقاله ساخته شد"))

        self.stdout.write(self.style.SUCCESS(f"\n✅ تعداد {count} مقاله (همراه با نظرات) با موفقیت ساخته شد."))
# ======================================================================================================================