from django.urls import path
from .views import ContactView, AboutView ,NewsletterSubscribeView
# ======================================================================================================================
# نام فضای آدرس‌دهی اپلیکیشن تماس
app_name = 'contact'
# ======================================================================================================================
# مسیرهای مربوط به تماس با ما، درباره ما و خبرنامه
urlpatterns = [

    # نمایش صفحه تماس با ما و پردازش فرم تماس
    path('contact-us/', ContactView.as_view(), name='contact-us'),

    # نمایش صفحه درباره ما
    path('about-us/', AboutView.as_view(), name='about-us'),

    # پردازش عضویت کاربر در خبرنامه
    path('newsletter/', NewsletterSubscribeView.as_view(), name='newsletter'),
]

# ======================================================================================================================
