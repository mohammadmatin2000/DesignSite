from django import forms
from shop.models import ProductModels, CategoryModels, TagModels
from services.models import ServiceModel, ServiceGalleryModel
from team.models import TeamModels
from index.models import GalleryModel
from blog.models import BlogModels, CategoryModels as BlogCategoryModels, TagModel as BlogTagModel
from projects.models import ProjectModel, ProjectCategoryModel
from contacts.models import HistoryItemModel, ProcessStepModel, AwardModel
# ======================================================================================================================
# ---------------------------- فرم‌های شاپ ----------------------------
class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModels
        fields = [
            "title", "category", "tags", "image", "sku", "price", "old_price",
            "short_description", "description", "is_available", "stock", "is_featured",
        ]
        widgets = {
            "short_description": forms.Textarea(attrs={"rows": 3}),
            "description": forms.Textarea(attrs={"rows": 6}),
        }
# ======================================================================================================================
class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModels
        fields = ["title"]
# ======================================================================================================================
class TagForm(forms.ModelForm):
    class Meta:
        model = TagModels
        fields = ["title"]
# ======================================================================================================================
# ---------------------------- فرم‌های خدمات ----------------------------
class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceModel
        fields = [
            "title", "description", "image", "about_service",
            "spaces_description", "key_elements_description", "order", "is_active",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "about_service": forms.Textarea(attrs={"rows": 4}),
            "spaces_description": forms.Textarea(attrs={"rows": 4}),
            "key_elements_description": forms.Textarea(attrs={"rows": 4}),
        }
# ======================================================================================================================
class ServiceGalleryForm(forms.ModelForm):
    class Meta:
        model = ServiceGalleryModel
        fields = ["service", "image"]
# ======================================================================================================================
# ---------------------------- فرم تیم ----------------------------
class TeamForm(forms.ModelForm):
    class Meta:
        model = TeamModels
        fields = [
            "full_name", "position", "image", "description", "email", "phone", "address",
            "skill_one", "skill_one_percent", "skill_two", "skill_two_percent",
            "skill_three", "skill_three_percent", "is_manager", "manager_quote", "is_active",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "manager_quote": forms.Textarea(attrs={"rows": 3}),
        }
# ======================================================================================================================
# ---------------------------- فرم گالری صفحه اصلی ----------------------------
class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryModel
        fields = ["image", "alt_text", "order", "is_active"]
# ======================================================================================================================
# ---------------------------- فرم‌های بلاگ ----------------------------
class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModels
        fields = [
            "title", "category", "tags", "image",
            "short_description", "content", "status",
        ]
        widgets = {
            "short_description": forms.Textarea(attrs={"rows": 3}),
            "content": forms.Textarea(attrs={"rows": 10}),
        }
# ======================================================================================================================
class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategoryModels
        fields = ["title"]
# ======================================================================================================================
class BlogTagForm(forms.ModelForm):
    class Meta:
        model = BlogTagModel
        fields = ["title"]
# ======================================================================================================================
# ---------------------------- فرم‌های پروژه ها ----------------------------
class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = [
            "title", "category", "extra_category", "location", "year", "image", "description",
            "client", "project_type", "architect", "duration", "strategy", "display_date",
            "short_description",
            "feature_one_title", "feature_one_desc",
            "feature_two_title", "feature_two_desc",
            "feature_three_title", "feature_three_desc",
            "feature_four_title", "feature_four_desc",
            "feature_five_title", "feature_five_desc",
            "stat_one_value", "stat_one_label",
            "stat_two_value", "stat_two_label",
            "stat_three_value", "stat_three_label",
            "stat_four_value", "stat_four_label",
            "result_description",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "short_description": forms.Textarea(attrs={"rows": 4}),
            "feature_one_desc": forms.Textarea(attrs={"rows": 2}),
            "feature_two_desc": forms.Textarea(attrs={"rows": 2}),
            "feature_three_desc": forms.Textarea(attrs={"rows": 2}),
            "feature_four_desc": forms.Textarea(attrs={"rows": 2}),
            "feature_five_desc": forms.Textarea(attrs={"rows": 2}),
            "result_description": forms.Textarea(attrs={"rows": 4}),
        }
# ======================================================================================================================
class ProjectCategoryForm(forms.ModelForm):
    class Meta:
        model = ProjectCategoryModel
        fields = ["title"]
# ======================================================================================================================
# ---------------------------- اطلاعات تماس ها ----------------------------
class HistoryItemForm(forms.ModelForm):
    class Meta:
        model = HistoryItemModel
        fields = ["image", "year", "description", "order", "is_active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
# ======================================================================================================================
class ProcessStepForm(forms.ModelForm):
    class Meta:
        model = ProcessStepModel
        fields = ["image", "title", "description", "order", "is_active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
# ======================================================================================================================
class AwardForm(forms.ModelForm):
    class Meta:
        model = AwardModel
        fields = ["title", "category", "year", "image", "order", "is_active"]
# ======================================================================================================================