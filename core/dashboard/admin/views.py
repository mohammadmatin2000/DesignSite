from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from projects.models import ProjectModel, ProjectCategoryModel
from dashboard.permission import HasAdminPermission
from order.models import OrderModel
from contacts.models import ContactMessageModel
from shop.models import ProductModels, CategoryModels, TagModels
from services.models import ServiceModel, ServiceGalleryModel
from team.models import TeamModels
from index.models import GalleryModel
from blog.models import BlogModels, CategoryModels as BlogCategoryModels, TagModel as BlogTagModel, CommentModel
from contacts.models import NewsletterSubscriberModel, HistoryItemModel, ProcessStepModel, AwardModel
from .forms import (
    ProductForm, CategoryForm, TagForm,
    ServiceForm, ServiceGalleryForm, TeamForm, GalleryForm,
    BlogForm, BlogCategoryForm, BlogTagForm,ProjectForm,ProjectCategoryForm,HistoryItemForm,ProcessStepForm,AwardForm
)
# ======================================================================================================================
# میکسین مشترک برای همه‌ی ویوهای ادمین
class AdminRequiredMixin(LoginRequiredMixin, HasAdminPermission):
    pass
# ======================================================================================================================
# صفحه‌ی اصلی داشبورد ادمین (آمار کلی)
class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "dashboard/admin/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        paid_orders = OrderModel.objects.filter(status__in=["paid", "shipped", "delivered"])

        context["total_orders"] = OrderModel.objects.count()
        context["pending_orders"] = OrderModel.objects.filter(status="pending").count()
        context["total_revenue"] = sum(order.total_price for order in paid_orders)
        context["unread_messages"] = ContactMessageModel.objects.filter(is_read=False).count()
        context["total_products"] = ProductModels.objects.count()
        context["total_blogs"] = BlogModels.objects.count()
        context["pending_comments"] = CommentModel.objects.filter(is_approved=False).count()
        context["recent_orders"] = OrderModel.objects.all()[:5]

        return context
# ======================================================================================================================
# ==================================== سفارش‌ها ====================================
class AdminOrderListView(AdminRequiredMixin, ListView):
    model = OrderModel
    template_name = "dashboard/admin/order/order-list.html"
    context_object_name = "orders"
    paginate_by = 15

    def get_queryset(self):
        queryset = OrderModel.objects.all()
        status = self.request.GET.get("status")
        q = self.request.GET.get("q", "").strip()

        if status:
            queryset = queryset.filter(status=status)

        if q:
            if q.isdigit():
                queryset = queryset.filter(id=int(q))
            else:
                queryset = queryset.filter(full_name__icontains=q)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_status"] = self.request.GET.get("status", "")
        context["status_choices"] = OrderModel.STATUS_CHOICES
        return context
# ======================================================================================================================
class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    model = OrderModel
    template_name = "dashboard/admin/order/order-detail.html"
    context_object_name = "orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = OrderModel.STATUS_CHOICES
        return context
# ======================================================================================================================
class AdminOrderUpdateStatusView(AdminRequiredMixin, View):

    def post(self, request, pk):
        order = get_object_or_404(OrderModel, pk=pk)
        new_status = request.POST.get("status")

        if new_status in dict(OrderModel.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, "وضعیت سفارش با موفقیت بروزرسانی شد.")
        else:
            messages.error(request, "وضعیت نامعتبر است.")

        return redirect("dashboard:admin:order-list")
# ======================================================================================================================
# ======================================================================================================================
class AdminOrderDeleteView(AdminRequiredMixin, DeleteView):
    model = OrderModel
    template_name = "dashboard/admin/order/order-delete.html"
    success_url = reverse_lazy("dashboard:admin:order-list")

    def form_valid(self, form):
        messages.success(self.request, "سفارش با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
# ==================================== پیام‌ها ====================================
class AdminMessageListView(AdminRequiredMixin, ListView):
    model = ContactMessageModel
    template_name = "dashboard/admin/messages/message-list.html"
    context_object_name = "contact_messages"
    paginate_by = 15

    def get_queryset(self):
        queryset = ContactMessageModel.objects.all().order_by("-created_date")
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset
# ======================================================================================================================
class AdminMessageDetailView(AdminRequiredMixin, DetailView):
    model = ContactMessageModel
    template_name = "dashboard/admin/messages/message-detail.html"
    context_object_name = "contact_message"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not self.object.is_read:
            self.object.is_read = True
            self.object.save()
        return response
# ======================================================================================================================
class AdminMessageDeleteView(AdminRequiredMixin, DeleteView):
    model = ContactMessageModel
    template_name = "dashboard/admin/messages/message-delete.html"
    success_url = reverse_lazy("dashboard:admin:message-list")

    def form_valid(self, form):
        messages.success(self.request, "پیام با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
# ======================================================================================================================
# ==================================== محصولات ====================================
class AdminProductListView(AdminRequiredMixin, ListView):
    model = ProductModels
    template_name = "dashboard/admin/products/products/product-list.html"
    context_object_name = "products"
    paginate_by = 15

    def get_queryset(self):
        queryset = ProductModels.objects.all()
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset
# ======================================================================================================================
class AdminProductCreateView(AdminRequiredMixin, CreateView):
    model = ProductModels
    form_class = ProductForm
    template_name = "dashboard/admin/products/products/product-create.html"
    success_url = reverse_lazy("dashboard:admin:product-list")

    def form_valid(self, form):
        messages.success(self.request, "محصول با موفقیت اضافه شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminProductUpdateView(AdminRequiredMixin, UpdateView):
    model = ProductModels
    form_class = ProductForm
    template_name = "dashboard/admin/products/products/product-update.html"
    success_url = reverse_lazy("dashboard:admin:product-list")

    def form_valid(self, form):
        messages.success(self.request, "محصول با موفقیت ویرایش شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminProductDeleteView(AdminRequiredMixin, DeleteView):
    model = ProductModels
    template_name = "dashboard/admin/products/products/product-delete.html"
    success_url = reverse_lazy("dashboard:admin:product-list")

    def form_valid(self, form):
        messages.success(self.request, "محصول با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
# ---------------------------- دسته‌بندی و برچسب شاپ ----------------------------
class AdminCategoryListView(AdminRequiredMixin, ListView):
    model = CategoryModels
    template_name = "dashboard/admin/products/categories/category-list.html"
    context_object_name = "categories"
# ======================================================================================================================
class AdminCategoryCreateView(AdminRequiredMixin, CreateView):
    model = CategoryModels
    form_class = CategoryForm
    template_name = "dashboard/admin/products/categories/category-create.html"
    success_url = reverse_lazy("dashboard:admin:category-list")
# ======================================================================================================================
class AdminCategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = CategoryModels
    form_class = CategoryForm
    template_name = "dashboard/admin/products/categories/category-update.html"
    success_url = reverse_lazy("dashboard:admin:category-list")
# ======================================================================================================================
class AdminCategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = CategoryModels
    template_name = "dashboard/admin/products/categories/category-delete.html"
    success_url = reverse_lazy("dashboard:admin:category-list")
# ======================================================================================================================
class AdminTagListView(AdminRequiredMixin, ListView):
    model = TagModels
    template_name = "dashboard/admin/products/tags/tag-list.html"
    context_object_name = "tags"
# ======================================================================================================================
class AdminTagCreateView(AdminRequiredMixin, CreateView):
    model = TagModels
    form_class = TagForm
    template_name = "dashboard/admin/products/tags/tag-create.html"
    success_url = reverse_lazy("dashboard:admin:tag-list")
# ======================================================================================================================
class AdminTagUpdateView(AdminRequiredMixin, UpdateView):
    model = TagModels
    form_class = TagForm
    template_name = "dashboard/admin/products/tags/tag-update.html"
    success_url = reverse_lazy("dashboard:admin:tag-list")
# ======================================================================================================================
class AdminTagDeleteView(AdminRequiredMixin, DeleteView):
    model = TagModels
    template_name = "dashboard/admin/products/tags/tag-delete.html"
    success_url = reverse_lazy("dashboard:admin:tag-list")
# ======================================================================================================================
# ==================================== خدمات ====================================
class AdminServiceListView(AdminRequiredMixin, ListView):
    model = ServiceModel
    template_name = "dashboard/admin/services/services/service-list.html"
    context_object_name = "services"
    paginate_by = 15

    def get_queryset(self):
        queryset = ServiceModel.objects.all()
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset
# ======================================================================================================================
class AdminServiceCreateView(AdminRequiredMixin, CreateView):
    model = ServiceModel
    form_class = ServiceForm
    template_name = "dashboard/admin/services/services/service-create.html"
    success_url = reverse_lazy("dashboard:admin:service-list")

    def form_valid(self, form):
        messages.success(self.request, "خدمت با موفقیت اضافه شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminServiceUpdateView(AdminRequiredMixin, UpdateView):
    model = ServiceModel
    form_class = ServiceForm
    template_name = "dashboard/admin/services/services/service-update.html"
    success_url = reverse_lazy("dashboard:admin:service-list")

    def form_valid(self, form):
        messages.success(self.request, "خدمت با موفقیت ویرایش شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminServiceDeleteView(AdminRequiredMixin, DeleteView):
    model = ServiceModel
    template_name = "dashboard/admin/services/services/service-delete.html"
    success_url = reverse_lazy("dashboard:admin:service-list")

    def form_valid(self, form):
        messages.success(self.request, "خدمت با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminServiceGalleryCreateView(AdminRequiredMixin, CreateView):
    model = ServiceGalleryModel
    form_class = ServiceGalleryForm
    template_name = "dashboard/admin/services/services-gallery/service-gallery-create.html"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:service-update", kwargs={"pk": self.object.service.id})
# ======================================================================================================================
class AdminServiceGalleryDeleteView(AdminRequiredMixin, DeleteView):
    model = ServiceGalleryModel
    template_name = "dashboard/admin/services/services-gallery/service-gallery-delete.html"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:service-update", kwargs={"pk": self.object.service.id})
# ======================================================================================================================
# ==================================== تیم ====================================
class AdminTeamListView(AdminRequiredMixin, ListView):
    model = TeamModels
    template_name = "dashboard/admin/team/team-list.html"
    context_object_name = "team_members"
    paginate_by = 15

    def get_queryset(self):
        queryset = TeamModels.objects.all()
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(full_name__icontains=q)
        return queryset
# ======================================================================================================================
class AdminTeamCreateView(AdminRequiredMixin, CreateView):
    model = TeamModels
    form_class = TeamForm
    template_name = "dashboard/admin/team/team-create.html"
    success_url = reverse_lazy("dashboard:admin:team-list")

    def form_valid(self, form):
        messages.success(self.request, "عضو تیم با موفقیت اضافه شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminTeamUpdateView(AdminRequiredMixin, UpdateView):
    model = TeamModels
    form_class = TeamForm
    template_name = "dashboard/admin/team/team-update.html"
    success_url = reverse_lazy("dashboard:admin:team-list")

    def form_valid(self, form):
        messages.success(self.request, "عضو تیم با موفقیت ویرایش شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminTeamDeleteView(AdminRequiredMixin, DeleteView):
    model = TeamModels
    template_name = "dashboard/admin/team/team-delete.html"
    success_url = reverse_lazy("dashboard:admin:team-list")

    def form_valid(self, form):
        messages.success(self.request, "عضو تیم با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
# ==================================== گالری صفحه اصلی ====================================
class AdminGalleryListView(AdminRequiredMixin, ListView):
    model = GalleryModel
    template_name = "dashboard/admin/gallery/gallery-list.html"
    context_object_name = "gallery_images"
    paginate_by = 20
# ======================================================================================================================
class AdminGalleryCreateView(AdminRequiredMixin, CreateView):
    model = GalleryModel
    form_class = GalleryForm
    template_name = "dashboard/admin/gallery/gallery-create.html"
    success_url = reverse_lazy("dashboard:admin:gallery-list")

    def form_valid(self, form):
        messages.success(self.request, "تصویر با موفقیت اضافه شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminGalleryUpdateView(AdminRequiredMixin, UpdateView):
    model = GalleryModel
    form_class = GalleryForm
    template_name = "dashboard/admin/gallery/gallery-update.html"
    success_url = reverse_lazy("dashboard:admin:gallery-list")

    def form_valid(self, form):
        messages.success(self.request, "تصویر با موفقیت ویرایش شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminGalleryDeleteView(AdminRequiredMixin, DeleteView):
    model = GalleryModel
    template_name = "dashboard/admin/gallery/gallery-delete.html"
    success_url = reverse_lazy("dashboard:admin:gallery-list")

    def form_valid(self, form):
        messages.success(self.request, "تصویر با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
# ==================================== بلاگ ====================================
class AdminBlogListView(AdminRequiredMixin, ListView):
    model = BlogModels
    template_name = "dashboard/admin/blog/blogs/blog-list.html"
    context_object_name = "blogs"
    paginate_by = 15

    def get_queryset(self):
        queryset = BlogModels.objects.all()
        q = self.request.GET.get("q")
        status = self.request.GET.get("status")
        if q:
            queryset = queryset.filter(title__icontains=q)
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = BlogModels.STATUS_CHOICES
        context["current_status"] = self.request.GET.get("status", "")
        return context
# ======================================================================================================================
class AdminBlogCreateView(AdminRequiredMixin, CreateView):
    model = BlogModels
    form_class = BlogForm
    template_name = "dashboard/admin/blog/blogs/blog-create.html"
    success_url = reverse_lazy("dashboard:admin:blog-list")

    def form_valid(self, form):
        messages.success(self.request, "مقاله با موفقیت اضافه شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminBlogUpdateView(AdminRequiredMixin, UpdateView):
    model = BlogModels
    form_class = BlogForm
    template_name = "dashboard/admin/blog/blogs/blog-update.html"
    success_url = reverse_lazy("dashboard:admin:blog-list")

    def form_valid(self, form):
        messages.success(self.request, "مقاله با موفقیت ویرایش شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminBlogDeleteView(AdminRequiredMixin, DeleteView):
    model = BlogModels
    template_name = "dashboard/admin/blog/blogs/blog-delete.html"
    success_url = reverse_lazy("dashboard:admin:blog-list")

    def form_valid(self, form):
        messages.success(self.request, "مقاله با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
# ---------------------------- دسته‌بندی و برچسب بلاگ ----------------------------
class AdminBlogCategoryListView(AdminRequiredMixin, ListView):
    model = BlogCategoryModels
    template_name = "dashboard/admin/blog/categories/blog-category-list.html"
    context_object_name = "categories"
# ======================================================================================================================
class AdminBlogCategoryCreateView(AdminRequiredMixin, CreateView):
    model = BlogCategoryModels
    form_class = BlogCategoryForm
    template_name = "dashboard/admin/blog/categories/blog-category-create.html"
    success_url = reverse_lazy("dashboard:admin:blog-category-list")
# ======================================================================================================================
class AdminBlogCategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = BlogCategoryModels
    form_class = BlogCategoryForm
    template_name = "dashboard/admin/blog/categories/blog-category-update.html"
    success_url = reverse_lazy("dashboard:admin:blog-category-list")
# ======================================================================================================================
class AdminBlogCategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = BlogCategoryModels
    template_name = "dashboard/admin/blog/categories/blog-category-delete.html"
    success_url = reverse_lazy("dashboard:admin:blog-category-list")
# ======================================================================================================================
class AdminBlogTagListView(AdminRequiredMixin, ListView):
    model = BlogTagModel
    template_name = "dashboard/admin/blog/tags/blog-tag-list.html"
    context_object_name = "tags"
# ======================================================================================================================
class AdminBlogTagCreateView(AdminRequiredMixin, CreateView):
    model = BlogTagModel
    form_class = BlogTagForm
    template_name = "dashboard/admin/blog/tags/blog-tag-create.html"
    success_url = reverse_lazy("dashboard:admin:blog-tag-list")
# ======================================================================================================================
class AdminBlogTagUpdateView(AdminRequiredMixin, UpdateView):
    model = BlogTagModel
    form_class = BlogTagForm
    template_name = "dashboard/admin/blog/tags/blog-tag-update.html"
    success_url = reverse_lazy("dashboard:admin:blog-tag-list")
# ======================================================================================================================
class AdminBlogTagDeleteView(AdminRequiredMixin, DeleteView):
    model = BlogTagModel
    template_name = "dashboard/admin/blog/tags/blog-tag-delete.html"
    success_url = reverse_lazy("dashboard:admin:blog-tag-list")
# ======================================================================================================================
# ---------------------------- نظرات بلاگ ----------------------------
class AdminCommentListView(AdminRequiredMixin, ListView):
    model = CommentModel
    template_name = "dashboard/admin/blog/comments/comment-list.html"
    context_object_name = "comments"
    paginate_by = 20

    def get_queryset(self):
        queryset = CommentModel.objects.all()
        status = self.request.GET.get("status")
        if status == "approved":
            queryset = queryset.filter(is_approved=True)
        elif status == "pending":
            queryset = queryset.filter(is_approved=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_status"] = self.request.GET.get("status", "")
        return context
# ======================================================================================================================
class AdminCommentApproveView(AdminRequiredMixin, View):

    def post(self, request, pk):
        comment = get_object_or_404(CommentModel, pk=pk)
        comment.is_approved = True
        comment.save()
        messages.success(request, "نظر تایید شد.")
        return redirect("dashboard:admin:comment-list")
# ======================================================================================================================
class AdminCommentDeleteView(AdminRequiredMixin, DeleteView):
    model = CommentModel
    template_name = "dashboard/admin/blog/comments/comment-delete.html"
    success_url = reverse_lazy("dashboard:admin:comment-list")

    def form_valid(self, form):
        messages.success(self.request, "نظر با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
# ---------------------------- پروژه ها ----------------------------
class AdminProjectListView(AdminRequiredMixin, ListView):
    model = ProjectModel
    template_name = "dashboard/admin/projects/projects/project-list.html"
    context_object_name = "projects"
    paginate_by = 15

    def get_queryset(self):
        queryset = ProjectModel.objects.all()
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset
# ======================================================================================================================
class AdminProjectCreateView(AdminRequiredMixin, CreateView):
    model = ProjectModel
    form_class = ProjectForm
    template_name = "dashboard/admin/projects/projects/project-create.html"
    success_url = reverse_lazy("dashboard:admin:project-list")

    def form_valid(self, form):
        messages.success(self.request, "پروژه با موفقیت اضافه شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminProjectUpdateView(AdminRequiredMixin, UpdateView):
    model = ProjectModel
    form_class = ProjectForm
    template_name = "dashboard/admin/projects/projects/project-update.html"
    success_url = reverse_lazy("dashboard:admin:project-list")

    def form_valid(self, form):
        messages.success(self.request, "پروژه با موفقیت ویرایش شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminProjectDeleteView(AdminRequiredMixin, DeleteView):
    model = ProjectModel
    template_name = "dashboard/admin/projects/projects/project-delete.html"
    success_url = reverse_lazy("dashboard:admin:project-list")

    def form_valid(self, form):
        messages.success(self.request, "پروژه با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
# ---------------------------- دسته‌بندی پروژه ----------------------------
class AdminProjectCategoryListView(AdminRequiredMixin, ListView):
    model = ProjectCategoryModel
    template_name = "dashboard/admin/projects/categories/project-category-list.html"
    context_object_name = "categories"
# ======================================================================================================================
class AdminProjectCategoryCreateView(AdminRequiredMixin, CreateView):
    model = ProjectCategoryModel
    form_class = ProjectCategoryForm
    template_name = "dashboard/admin/projects/categories/project-category-create.html"
    success_url = reverse_lazy("dashboard:admin:project-category-list")
# ======================================================================================================================
class AdminProjectCategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = ProjectCategoryModel
    form_class = ProjectCategoryForm
    template_name = "dashboard/admin/projects/categories/project-category-update.html"
    success_url = reverse_lazy("dashboard:admin:project-category-list")
# ======================================================================================================================
class AdminProjectCategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = ProjectCategoryModel
    template_name = "dashboard/admin/projects/categories/project-category-delete.html"
    success_url = reverse_lazy("dashboard:admin:project-category-list")
# ======================================================================================================================
# ==================================== خبرنامه ====================================
class AdminNewsletterListView(AdminRequiredMixin, ListView):
    model = NewsletterSubscriberModel
    template_name = "dashboard/admin/contacts/newsletter-list.html"
    context_object_name = "subscribers"
    paginate_by = 20

    def get_queryset(self):
        queryset = NewsletterSubscriberModel.objects.all().order_by("-subscribed_date")
        q = self.request.GET.get("q", "").strip()
        if q:
            queryset = queryset.filter(email__icontains=q)
        return queryset
# ======================================================================================================================
class AdminNewsletterDeleteView(AdminRequiredMixin, DeleteView):
    model = NewsletterSubscriberModel
    template_name = "dashboard/admin/contacts/newsletter-delete.html"
    success_url = reverse_lazy("dashboard:admin:newsletter-list")

    def form_valid(self, form):
        messages.success(self.request, "مشترک با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
# ==================================== سابقه شرکت ====================================
class AdminHistoryListView(AdminRequiredMixin, ListView):
    model = HistoryItemModel
    template_name = "dashboard/admin/contacts/history-list.html"
    context_object_name = "history_items"
# ======================================================================================================================
class AdminHistoryCreateView(AdminRequiredMixin, CreateView):
    model = HistoryItemModel
    form_class = HistoryItemForm
    template_name = "dashboard/admin/contacts/history-create.html"
    success_url = reverse_lazy("dashboard:admin:history-list")

    def form_valid(self, form):
        messages.success(self.request, "آیتم سابقه با موفقیت اضافه شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminHistoryUpdateView(AdminRequiredMixin, UpdateView):
    model = HistoryItemModel
    form_class = HistoryItemForm
    template_name = "dashboard/admin/contacts/history-update.html"
    success_url = reverse_lazy("dashboard:admin:history-list")

    def form_valid(self, form):
        messages.success(self.request, "آیتم سابقه با موفقیت ویرایش شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminHistoryDeleteView(AdminRequiredMixin, DeleteView):
    model = HistoryItemModel
    template_name = "dashboard/admin/contacts/history-delete.html"
    success_url = reverse_lazy("dashboard:admin:history-list")

    def form_valid(self, form):
        messages.success(self.request, "آیتم سابقه با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
# ==================================== مراحل کاری ====================================
class AdminProcessListView(AdminRequiredMixin, ListView):
    model = ProcessStepModel
    template_name = "dashboard/admin/contacts/process-list.html"
    context_object_name = "process_steps"
# ======================================================================================================================
class AdminProcessCreateView(AdminRequiredMixin, CreateView):
    model = ProcessStepModel
    form_class = ProcessStepForm
    template_name = "dashboard/admin/contacts/process-create.html"
    success_url = reverse_lazy("dashboard:admin:process-list")

    def form_valid(self, form):
        messages.success(self.request, "مرحله کاری با موفقیت اضافه شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminProcessUpdateView(AdminRequiredMixin, UpdateView):
    model = ProcessStepModel
    form_class = ProcessStepForm
    template_name = "dashboard/admin/contacts/process-update.html"
    success_url = reverse_lazy("dashboard:admin:process-list")

    def form_valid(self, form):
        messages.success(self.request, "مرحله کاری با موفقیت ویرایش شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminProcessDeleteView(AdminRequiredMixin, DeleteView):
    model = ProcessStepModel
    template_name = "dashboard/admin/contacts/process-delete.html"
    success_url = reverse_lazy("dashboard:admin:process-list")

    def form_valid(self, form):
        messages.success(self.request, "مرحله کاری با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================
# ==================================== جوایز ====================================
class AdminAwardListView(AdminRequiredMixin, ListView):
    model = AwardModel
    template_name = "dashboard/admin/contacts/award-list.html"
    context_object_name = "awards"
# ======================================================================================================================
class AdminAwardCreateView(AdminRequiredMixin, CreateView):
    model = AwardModel
    form_class = AwardForm
    template_name = "dashboard/admin/contacts/award-create.html"
    success_url = reverse_lazy("dashboard:admin:award-list")

    def form_valid(self, form):
        messages.success(self.request, "جایزه با موفقیت اضافه شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminAwardUpdateView(AdminRequiredMixin, UpdateView):
    model = AwardModel
    form_class = AwardForm
    template_name = "dashboard/admin/contacts/award-update.html"
    success_url = reverse_lazy("dashboard:admin:award-list")

    def form_valid(self, form):
        messages.success(self.request, "جایزه با موفقیت ویرایش شد.")
        return super().form_valid(form)
# ======================================================================================================================
class AdminAwardDeleteView(AdminRequiredMixin, DeleteView):
    model = AwardModel
    template_name = "dashboard/admin/contacts/award-delete.html"
    success_url = reverse_lazy("dashboard:admin:award-list")

    def form_valid(self, form):
        messages.success(self.request, "جایزه با موفقیت حذف شد.")
        return super().form_valid(form)
# ======================================================================================================================