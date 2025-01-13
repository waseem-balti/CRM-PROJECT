from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import CustomUser
from django.utils.timezone import now
from .models import (
    UserProfile, Company, Branch, Department, Currency, CustomUser,
    DpartmentalGoal, KPI, Funnel, Lead, JunkReason, LostReason, DailyTarget,
    AssignProduct, ScheduleCalls, LeadSummary, ContactActivity, LeadSource,
    Contact, Price, Product, ProductService, Campaign, Organization,
    Invoice, ProductQuotation,  Payment, AuditLog, Event, 
    Upload_Project, Post, Comment, Like, Contact, Task, Contest,
    Folder, File
)




@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'created_by__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'folder', 'owner', 'size', 'file_type', 'uploaded_at')
    search_fields = ('name', 'folder__name', 'owner__username')
    list_filter = ('uploaded_at', 'file_type')
    ordering = ('-uploaded_at',)


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords must match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    # Add custom fieldsets for better grouping
    fieldsets = (
        ('User', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
        ('Important Dates', {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        for user in queryset.filter(trial=True, trial_end_date__lte=now()):
            user.trial = False
            user.save()
        return queryset

    # Add custom action for bulk deactivating users
    actions = ['deactivate_users']

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected users have been deactivated.")

    deactivate_users.short_description = "Deactivate selected users"


# Admin Classes for Models
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'website', 'email', 'phone_number', 'created_by']
    search_fields = ['name', 'email', 'created_by__username']
    list_filter = ['website', 'created_by']


class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'contact_person', 'contact_email', 'contact_phone', 'company']
    search_fields = ['name', 'contact_person', 'contact_email', 'contact_phone', 'company__name']
    list_filter = ['company']


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'branch']
    search_fields = ['name', 'description', 'branch__name']
    list_filter = ['branch']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['company', 'code', 'name', 'symbol']
    search_fields = ['code', 'name', 'symbol', 'company__name']
    list_filter = ['company']


class LeadAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'branch', 'mobile_phone']
    search_fields = ['first_name', 'last_name', 'email', 'branch__name', 'mobile_phone']
    list_filter = ['branch', 'assigned_to']


class LeadSourceAdmin(admin.ModelAdmin):
    list_display = ['source', 'branch', 'created_by']
    search_fields = ['source', 'branch__name']
    list_filter = ['branch']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'primary_email', 'mobile_phone', 'branch']
    search_fields = ['first_name', 'last_name', 'primary_email', 'mobile_phone', 'branch__name']
    list_filter = ['branch']


class PriceAdmin(admin.ModelAdmin):
    list_display = ['price_book_name', 'branch', 'currency', 'active']
    search_fields = ['price_book_name', 'branch__name', 'currency__name']
    list_filter = ['branch', 'currency']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'product_active', 'manufacturer', 'product_category', 'price']
    search_fields = ['name', 'branch__name', 'manufacturer', 'product_category']
    list_filter = ['branch', 'product_category']


class ProductServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'active', 'usage_unit', 'price']
    search_fields = ['name', 'branch__name', 'usage_unit']
    list_filter = ['branch', 'category']


class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'status', 'campaign_type', 'product']
    search_fields = ['name', 'branch__name', 'campaign_type']
    list_filter = ['branch', 'status']


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['organization_name', 'branch', 'phone_no', 'email']
    search_fields = ['organization_name', 'branch__name', 'email']
    list_filter = ['branch', 'industry']


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'branch', 'customer', 'product', 'price']
    search_fields = ['invoice_number', 'branch__name', 'customer__first_name', 'product__name']
    list_filter = ['branch', 'customer']


class ProductQuotationAdmin(admin.ModelAdmin):
    list_display = ['quotation_number', 'branch', 'customer_name', 'product_name', 'total_price']
    search_fields = ['quotation_number', 'branch__name', 'customer_name__first_name', 'product_name__name']
    list_filter = ['branch', 'customer_name']


class DailyTargetAdmin(admin.ModelAdmin):
    list_display = ['todays_motivation', 'todays_goals', 'target', 'achieved', 'date_created']
    search_fields = ['todays_motivation', 'todays_goals']
    list_filter = ['date_created']


class AssignProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'target', 'date_created']
    search_fields = ['user__email', 'product__name']
    list_filter = ['date_created']


class ScheduleCallsAdmin(admin.ModelAdmin):
    list_display = ['lead', 'schedule_for', 'date_time', 'is_sent']
    search_fields = ['lead__first_name', 'schedule_for']
    list_filter = ['schedule_for', 'date_time']


class LeadSummaryAdmin(admin.ModelAdmin):
    list_display = ['lead', 'summary', 'rating', 'date_created']
    search_fields = ['lead__first_name', 'summary']
    list_filter = ['rating']


class ContactActivityAdmin(admin.ModelAdmin):
    list_display = ['lead', 'contact_type', 'date_created']
    search_fields = ['lead__first_name', 'contact_type']
    list_filter = ['contact_type']


# Admin Classes for Missing Models
class DepartmentalGoalAdmin(admin.ModelAdmin):
    list_display = ['department', 'goal', 'from_date', 'to_date', 'created_by']
    search_fields = ['goal', 'department__name']
    list_filter = ['to_date', 'department']


class KPIAdmin(admin.ModelAdmin):
    list_display = ['department', 'goal', 'kpi', 'target', 'created_by']
    search_fields = ['kpi', 'goal', 'department__name']
    list_filter = ['department']


class FunnelAdmin(admin.ModelAdmin):
    list_display = ['department', 'stage', 'created_by']
    search_fields = ['stage', 'department__name']
    list_filter = ['stage', 'department']


class JunkReasonAdmin(admin.ModelAdmin):
    list_display = ['lead', 'client_industry_relevance', 'client_budget', 'client_authority', 'details']
    search_fields = ['lead__first_name', 'details']
    list_filter = ['client_industry_relevance', 'client_budget', 'client_authority']


class LostReasonAdmin(admin.ModelAdmin):
    list_display = ['lead', 'client_no_industry', 'client_no_budget', 'needs_no_satisfied', 'details']
    search_fields = ['lead__first_name', 'details']
    list_filter = ['client_no_industry', 'client_no_budget', 'needs_no_satisfied']


class TrialedEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']
    search_fields = ['email']
    list_filter = ['created_at']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'amount', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at')
    search_fields = ('transaction_id',)

    def has_add_permission(self, request):
        """Disable add functionality in admin if not needed."""
        return super().has_add_permission(request)

class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'resource_name', 'resource_id', 'timestamp', 'ip_address', 'description']
    search_fields = ['user__email', 'action', 'resource_name', 'resource_id']
    list_filter = ['action', 'timestamp', 'resource_name']


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_time', 'end_time', 'category', 'user']
    search_fields = ['title', 'user__email']
    list_filter = ['category', 'start_time']

class UploadProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'due_date', 'priority', 'budget', 'privacy']
    search_fields = ['name', 'overview', 'team_members__username']
    list_filter = ['privacy', 'start_date', 'due_date']



class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'url', 'media', 'created_at', 'updated_at']
    search_fields = ['content', 'author__username', 'url']
    list_filter = ['created_at', 'updated_at']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content', 'created_at', 'updated_at']
    search_fields = ['content', 'author__username', 'post__content']
    list_filter = ['created_at', 'updated_at']

class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    search_fields = ['user__username', 'post__content']
    list_filter = ['created_at']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'due_date', 'assigned_to', 'created_at']
    search_fields = ['title', 'description', 'assigned_to__username']
    list_filter = ['status', 'due_date', 'created_at']




class ContestAdmin(admin.ModelAdmin):
    list_display = ['name', 'objective', 'department', 'assigned_to', 'launch_date', 'due_date', 'company', 'created_at']
    search_fields = ['name', 'objective', 'department', 'company', 'assigned_to__username']
    list_filter = ['launch_date', 'due_date', 'created_at']



# Register All Admin Classes
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Lead, LeadAdmin)
admin.site.register(LeadSource, LeadSourceAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductService, ProductServiceAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(ProductQuotation, ProductQuotationAdmin)
admin.site.register(DailyTarget, DailyTargetAdmin)
admin.site.register(AssignProduct, AssignProductAdmin)
admin.site.register(ScheduleCalls, ScheduleCallsAdmin)
admin.site.register(LeadSummary, LeadSummaryAdmin)
admin.site.register(ContactActivity, ContactActivityAdmin)
admin.site.register(DpartmentalGoal, DepartmentalGoalAdmin)
admin.site.register(KPI, KPIAdmin)
admin.site.register(Funnel, FunnelAdmin)
admin.site.register(JunkReason, JunkReasonAdmin)
admin.site.register(LostReason, LostReasonAdmin)
admin.site.register(AuditLog, AuditLogAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Upload_Project, UploadProjectAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Contest, ContestAdmin)