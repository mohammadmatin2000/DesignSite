import random
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from shop.models import (
    ProductModels,
    CategoryModels,
    TagModels,
    ProductImageModels,
    ProductReviewModels,
)
# ======================================================================================================================
# دستور مدیریتی برای ساخت داده‌های ساختگی (فیک) برای فروشگاه
# اجرا با: python manage.py generate_shop
# یا با تعداد دلخواه: python manage.py generate_shop --count 20
class Command(BaseCommand):

    help = "ساخت دسته‌بندی، برچسب، محصولات، گالری و نظرات ساختگی برای تست فروشگاه"

    # تعریف آرگومان‌های اختیاری
    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="تعداد محصولاتی که باید ساخته شود (پیش‌فرض: 10)",
        )
        parser.add_argument(
            "--reviews",
            type=int,
            default=5,
            help="حداکثر تعداد نظر برای هر محصول (پیش‌فرض: 5)",
        )
        parser.add_argument(
            "--gallery",
            type=int,
            default=4,
            help="حداکثر تعداد تصویر گالری برای هر محصول (پیش‌فرض: 4)",
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
    def get_random_image(self, image_files, name_prefix="product"):
        chosen_file = random.choice(image_files)

        with open(chosen_file, "rb") as f:
            content = f.read()

        extension = chosen_file.suffix
        new_name = f"{slugify(name_prefix)}-{random.randint(1000, 9999)}{extension}"

        return ContentFile(content, name=new_name)

    # اجرای اصلی دستور
    def handle(self, *args, **options):
        count = options["count"]
        max_reviews = options["reviews"]
        max_gallery = options["gallery"]

        # استفاده از لوکال فارسی برای تولید متن‌های واقعی‌تر
        fake = Faker("fa_IR")

        # بارگذاری لیست عکس‌های موجود یک بار، قبل از شروع حلقه
        image_files = self.get_image_files()
        self.stdout.write(self.style.SUCCESS(f"تعداد {len(image_files)} عکس در پوشه پیدا شد."))

        # ----------------------------------------------------------------
        # ساخت دسته‌بندی‌های ثابت (اگر از قبل وجود نداشته باشند)
        category_names = ["مبلمان", "میز و صندلی", "دکوراسیون", "نورپردازی", "قفسه و کتابخانه"]
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
            tag, created = TagModels.objects.get_or_create(title=name)
            tags.append(tag)
            if created:
                self.stdout.write(self.style.SUCCESS(f"برچسب ساخته شد: {name}"))

        # ----------------------------------------------------------------
        # ساخت محصولات ساختگی به همراه گالری و نظرات هرکدام
        for i in range(count):

            title = fake.sentence(nb_words=4).rstrip(".")

            price = random.randint(200, 5000) * 10
            has_discount = random.choice([True, False, False])
            old_price = int(price * random.uniform(1.15, 1.6)) if has_discount else None

            product = ProductModels(
                title=title,
                category=random.choice(categories),
                sku=f"SKU-{random.randint(10000, 99999)}",
                price=price,
                old_price=old_price,
                short_description=fake.paragraph(nb_sentences=2),
                description="\n\n".join(fake.paragraphs(nb=4)),
                stock=random.randint(0, 50),
                is_available=random.choice([True, True, True, False]),
                is_featured=random.choice([True, False, False, False]),
                views=random.randint(0, 800),
            )

            random_image_file = self.get_random_image(image_files, name_prefix=title)

            product.image.save(
                random_image_file.name,
                random_image_file,
                save=False,
            )

            product.save()

            # اضافه کردن ۱ تا ۳ برچسب تصادفی به هر محصول
            product.tags.set(random.sample(tags, k=random.randint(1, 3)))

            self.stdout.write(self.style.SUCCESS(f"محصول ساخته شد: {title}"))

            # --------------------------------------------------------
            # ساخت گالری تصاویر تصادفی برای همین محصول
            gallery_count = random.randint(0, max_gallery)

            for _ in range(gallery_count):
                gallery_image_file = self.get_random_image(image_files, name_prefix=f"{title}-gallery")

                gallery_image = ProductImageModels(product=product)
                gallery_image.image.save(
                    gallery_image_file.name,
                    gallery_image_file,
                    save=False,
                )
                gallery_image.save()

            if gallery_count:
                self.stdout.write(self.style.SUCCESS(f"  └─ {gallery_count} تصویر گالری برای این محصول ساخته شد"))

            # --------------------------------------------------------
            # ساخت نظرات ساختگی برای همین محصول
            review_count = random.randint(0, max_reviews)

            for _ in range(review_count):
                ProductReviewModels.objects.create(
                    product=product,
                    full_name=fake.name(),
                    email=fake.email(),
                    rating=random.randint(1, 5),
                    comment=fake.paragraph(nb_sentences=2),
                    is_approved=random.choice([True, True, True, False]),
                )

            if review_count:
                self.stdout.write(self.style.SUCCESS(f"  └─ {review_count} نظر برای این محصول ساخته شد"))

        self.stdout.write(self.style.SUCCESS(f"\n✅ تعداد {count} محصول (همراه با گالری و نظرات) با موفقیت ساخته شد."))
# ======================================================================================================================