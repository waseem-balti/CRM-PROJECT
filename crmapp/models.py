import random
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin
from .validations import *
from django.utils.timezone import now, timedelta
from django.conf import settings
import uuid

class CustomUserManager(BaseUserManager):   
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The email field must be set')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=False.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user( email , password, **extra_fields)


        
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, blank=True,null=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_company_owner = models.BooleanField(default=False)
    is_branch_head = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_department_head = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_executive = models.BooleanField(default=False)
    first_login = models.BooleanField(default=True)
    no_of_branch = models.PositiveIntegerField(null=True, blank=True)
    no_of_department = models.PositiveIntegerField(null=True, blank=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    phone_no = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    BRANCH_CHOICES = [
        ('branch1', 'Branch 1'),
        ('branch2', 'Branch 2'),
    ]

    DEPARTMENT_CHOICES = [
        ('department1', 'Department 1'),
        ('department2', 'Department 2'),
    ]  # Moved this to a class-level attribute

    STATUS_CHOICES = [
         ('active', 'Active'),
         ('blocked','Blocked'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    trial = models.BooleanField(default=False)

    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = CustomUserManager()

    trial_start_date = models.DateTimeField(default=timezone.now)
    trial_end_date = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))

    def start_trial(self, trial_duration_days=30):
        """
        Start a trial for the user if eligible.
        """
        if self.email in TrialedEmail:
            raise ValueError("Trial already availed by this user.")
        
        self.trial = True
        self.trial_start_date = timezone.now()
        self.trial_end_date = self.trial_start_date + timedelta(days=trial_duration_days)
        self.save()

    def is_trial_expired(self):
        """
        Check if the trial period has expired.
        """
        if self.trial_end_date and timezone.now() > self.trial_end_date:
            return True
        return False

    def deactivate_trial(self):
        """
        Deactivate the user if the trial period has expired.
        """
        if self.is_trial_expired():
            self.is_active = False
            self.trial = False
            self.save()

    def __str__(self):
        return self.email

    def reactivate_trial(self, reactivation_duration_days=30):
        if  self.is_trial_expired():
            self.trial_end_date = timezone.now() + timedelta(days=reactivation_duration_days)
            self.trial = True
            self.is_active = True
            self.save()
        else:
            raise ValueError("Trial is still active and cannot be reactivated.")
class TrialedEmail(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Upload_Project(models.Model):
    PRIVACY_CHOICES = [
        ('private', 'Private'),
        ('team', 'Team'),
        ('public', 'Public'),
    ]
    
    name = models.CharField(max_length=200)
    overview = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    start_date = models.DateField()
    due_date = models.DateField()
    priority = models.CharField(max_length=50, blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    team_members = models.ManyToManyField(CustomUser, related_name='projects')

    def __str__(self):
        return self.name





def generate_transaction_id():
    return f"tx-{''.join([str(random.randint(0, 9)) for _ in range(10)])}"

# In the model
class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    transaction_id = models.CharField(default=generate_transaction_id, editable=False, unique=True, max_length=13)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for {self.user.username}"

class Company(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    # website = models.URLField()
    website = models.CharField(max_length=200,null=True, blank=True, validators=[validate_custom_url])
    email = models.EmailField()
    phone_number = models.CharField(max_length=20 ,null=True, blank=True)
    logo = models.FileField(
        upload_to='company_logos',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    # created_by = models.ForeignKey('crmapp.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_companies')

    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_companies')
    def __str__(self):
        return self.name

class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_branch')
    def __str__(self):
        return self.name

class Department(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    DEPARTMENT_CHOICES = [
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
    ]
    name = models.CharField(max_length=255,choices=DEPARTMENT_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_department')
    # head_of_department = models.CharField(max_length=255)
    # contact_email = models.EmailField()
    # contact_phone = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    
class Currency(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=3, unique=True, help_text="Currency code (e.g., USD, EUR)")
    name = models.CharField(max_length=50, unique=True, help_text="Currency name")
    symbol = models.CharField(max_length=5, blank=True, null=True, help_text="Currency symbol")
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_currency')

    def __str__(self):
        return self.code
    
def one_month_later():
        return timezone.now() + timedelta(days=30)

class DpartmentalGoal(models.Model):
    # branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True,)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    mission = models.TextField(blank=True, null=True)
    from_date = models.DateField(default=timezone.now, null=True, blank=True)
    to_date = models.DateField(default=one_month_later, null=True, blank=True)
    goal = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_goal')
    def __str__(self):
        return self.goal
    class Meta:
        ordering = ['-to_date']

class KPI(models.Model):
    # branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True,)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    goal=models.CharField(max_length=500, blank=True, null=True)
    # expected_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expected_leads=models.PositiveIntegerField(blank=True, null=True, default=0)
    kpi=models.CharField(max_length=500, blank=True, null=True)
    target=models.CharField(max_length=500, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_kpi')
    def __str__(self):
        return self.kpi
    
class Funnel(models.Model):
    STAGE_CHOICES = [
        ('dnc', 'DNC (Did not connect)'),
        ('interested', 'Interested, need more info'),
        ('junk', 'Junk'),
        ('not_interested', 'Not interested, but qualified'),
        ('trial_demo', 'Trial/Demo/Meeting'),
        ('objection_handling', 'Objection Handling'),
        ('price_negotiation', 'Price Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    stage = models.CharField(max_length=100, choices=STAGE_CHOICES, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_funnel')

    def __str__(self):
        return self.stage


class LeadSource(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    source=models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_lead_source')
    def __str__(self):
        return self.source
#----------------------------Inventory ------------------------------------------------------------------------------



class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    primary_email = models.EmailField()
    office_phone = models.CharField(max_length=20, blank=True, null=True)
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    home_phone = models.CharField(max_length=20, blank=True, null=True)
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    reports_to = models.CharField(max_length=255, blank=True, null=True)
    secondary_email = models.EmailField(blank=True, null=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    SOCIAL_MEDIA_CHOICES = [
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('LinkedIn', 'LinkedIn'),
        ('Instagram', 'Instagram'),
        ('Email', 'Email'),
        ('Phone Call', 'Phone Call'),
        ('Other', 'Other'),
    ]
    lead_source = models.CharField(max_length=255, choices=SOCIAL_MEDIA_CHOICES, blank=True, null=True)

    support_start_date = models.DateField(blank=True, null=True)
    support_end_date = models.DateField(blank=True, null=True)

    # Address Details
    mailing_street = models.CharField(max_length=500,blank=True, null=True)
    mailing_city = models.CharField(max_length=255, blank=True, null=True)
    mailing_state = models.CharField(max_length=255, blank=True, null=True)
    mailing_zip = models.CharField(max_length=20, blank=True, null=True)
    mailing_country = models.CharField(max_length=255, blank=True, null=True)

    # Description Details
    description = models.TextField(blank=True, null=True)

    # Profile Picture
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_contact')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Price(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    price_book_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.price_book_name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product_active = models.BooleanField(default=True)
    part_number = models.CharField(max_length=50, blank=True, null=True)
    MANUFACTURAR_CHOICES = [
        ('vista', 'VISTA'),
        ('arkplus', 'Arkplus'),
    ]
    manufacturer = models.CharField(max_length=255, choices=MANUFACTURAR_CHOICES, blank=True, null=True)
    CATEGORY_CHOICES = [
        ('software', 'Software'),
        ('hardware', 'Hardware'),
        ('crm_application', 'CRM Application'),
    ]
    product_category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, blank=True, null=True)
    sales_start_date = models.DateField(default=timezone.now, null=True, blank=True)
    sales_end_date = models.DateField(default=one_month_later, null=True, blank=True)
    support_start_date = models.DateField(default=timezone.now, null=True, blank=True)
    support_expiry_date = models.DateField(default=one_month_later, null=True, blank=True)
    VEVDOR_CHOICES = [
        ('vista', 'VISTA'),
        ('arkplus', 'Arkplus'),
    ]
    vendor_name = models.CharField(max_length=255, choices=VEVDOR_CHOICES, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    serial_no = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sales_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    service_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # Stock Information
    usage_unit = models.CharField(max_length=50, blank=True, null=True)
    qty_per_unit = models.PositiveIntegerField(blank=True, null=True)
    qty_in_stock = models.PositiveIntegerField(blank=True, null=True)
    handler = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    # Product Image Information
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    # Description Details
    description = models.TextField(blank=True, null=True)
    terms_condition = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return self.name
  


class ProductService(models.Model):
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    USAGE_UNIT_CHOICES = [
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('incident', 'Incident'),
    ]
    usage_unit = models.CharField(max_length=255, choices=USAGE_UNIT_CHOICES, blank=True, null=True)
    active = models.BooleanField(default=True)
    num_units = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True)
    CATEGORY_CHOICES = [
        ('support', 'Support'),
        ('installation', 'Installation'),
        ('migration', 'Migration'),
        ('customization', 'Customization'),
        ('training', 'Training'),
    ]
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    support_start_date = models.DateField(default=timezone.now, null=True, blank=True)
    support_expiry_date = models.DateField(default=one_month_later, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

  



#----------------------------Marketing ------------------------------------------------------------------------------
class Campaign(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    CAMPAIGN_TYPE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('email', 'Email'),
        ('social_media', 'Social Media'),
    ]
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPE_CHOICES, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    target_audience = models.TextField(blank=True, null=True)
    sponsor = models.CharField(max_length=100, blank=True, null=True)
    channels = models.CharField(max_length=255,blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expected_leads = models.PositiveIntegerField(blank=True, null=True)
    start_date = models.DateField(default=timezone.now, null=True, blank=True)
    end_date = models.DateField(default=one_month_later, null=True, blank=True)
    goals_and_objectives = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    media = models.ImageField(upload_to='campaigns/', blank=True, null=True)
    def __str__(self):
        return self.name

    
class Lead(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    mobile_phone = models.CharField(max_length=18)
    fax = models.CharField(max_length=15, blank=True, null=True)
    lead_source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_source')
    company = models.CharField(max_length=255, blank=True, null=True)
    is_customer = models.BooleanField(default=False)  # New field to track customers
    INDUSTORY_CHOICES = [
        ('banking', 'Banking'),
        ('retailer', 'Retailer'),
        ('telecom', 'Telecom'),
        ('IT', 'Information Technology'),
        ('consulting', 'Consulting'),
        ('electronics', 'Electronics'),
    ]
    industry = models.CharField(max_length=255,choices=INDUSTORY_CHOICES, blank=True, null=True)
    lead_status = models.ForeignKey(Funnel, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    move_to_opportunity = models.BooleanField(default=False)
    accept = models.BooleanField(default=False)
    deal_close = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_lead')
    date_created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    lead_image = models.ImageField(upload_to='leads/', blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['branch', 'mobile_phone'], name='unique_mobile_phone_per_branch')
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Organization(models.Model):
    organization_name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    website = models.URLField(blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    fax = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    ownership = models.CharField(max_length=255, blank=True, null=True)
    INDUSTORY_CHOICES = [
        ('banking', 'Banking'),
        ('telecom', 'Telecom'),
        ('IT', 'Information Technology'),
        ('consulting', 'Consulting'),
        ('electronics', 'Electronics'),
    ]
    industry = models.CharField(max_length=255,choices=INDUSTORY_CHOICES, blank=True, null=True)
    organization_type = models.CharField(max_length=255, blank=True, null=True)
    no_of_employees = models.PositiveIntegerField(blank=True, null=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    notify_owner = models.BooleanField(default=False)

    # Address Details
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)

    billing_po_box = models.CharField(max_length=255, blank=True, null=True)
    shipping_po_box = models.CharField(max_length=255, blank=True, null=True)

    billing_city = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=255, blank=True, null=True)

    billing_state = models.CharField(max_length=255, blank=True, null=True)
    shipping_state = models.CharField(max_length=255, blank=True, null=True)

    billing_postal_code = models.CharField(max_length=20, blank=True, null=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True, null=True)

    billing_country = models.CharField(max_length=255, blank=True, null=True)
    shipping_country = models.CharField(max_length=255, blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.organization_name
# inventory
class Invoice(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    customer=models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    package = models.CharField(max_length=50,blank=True, null=True)

    invoice_number = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity= models.PositiveIntegerField(blank=True, null=True)
    deal_duration = models.CharField(max_length=255,blank=True, null=True)
    deal_start_date = models.DateField(default=timezone.now, null=True, blank=True)
    deal_expiry_date = models.DateField(default=one_month_later, null=True, blank=True)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    date_created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_invoice')
    def __str__(self):
        return self.invoice_number

class ProductQuotation(models.Model):
    # General Details
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    quotation_number = models.CharField(max_length=20, unique=True)
    quotation_date = models.DateField(default=timezone.now, null=True, blank=True)
    expiration_date = models.DateField(default=one_month_later, null=True, blank=True)
    # Customer Details
    
    customer_name=models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    # Product Details
    # product_name = models.CharField(max_length=255)
    product_name = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Total Price
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # Additional Notes
    
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Quotation #{self.quotation_number} for {self.product_name}"







class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Fields from CustomUser
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    department = models.CharField(max_length=20, choices=CustomUser.DEPARTMENT_CHOICES, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Additional Fields
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)

    # Contact Information
    address = models.CharField(max_length=500,null=True, blank=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    # Employment Information
    employee_id = models.CharField(max_length=20, unique=True)
    hire_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='direct_reports')

    # Other Employment Information
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract'), ('Internship', 'Internship')], blank=True, null=True)
    work_location = models.CharField(max_length=50, blank=True, null=True)
    work_mode = models.CharField(max_length=20, choices=[('Remote', 'Remote'), ('Onsite', 'Onsite'), ('Hybrid', 'Hybrid')], blank=True, null=True)

    # Emergency Contact Information
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)

    # Education Information
    education_degree = models.CharField(max_length=50, blank=True, null=True)
    education_institution = models.CharField(max_length=100, blank=True, null=True)
    graduation_year = models.PositiveIntegerField(null=True, blank=True)

    # Skills and Certifications
    skills = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)

    # Other Information
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    





class DailyTarget(models.Model):
    todays_motivation = models.CharField(max_length=255,blank=True, null=True)
    todays_goals = models.TextField(blank=True, null=True)
    todays_appointments = models.TextField(blank=True, null=True)
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    #New Calls
    target = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    achieved = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    #New Leads
    provided = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    qualified = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    #Account Creations
    acsount_createion = models.PositiveBigIntegerField(null=True, blank=True,default=0)
    #Revenue Generated
    revenue_enrated = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    
    #Today's Visits
    area = models.CharField(max_length=255,blank=True, null=True)
    purpose = models.CharField(max_length=255,blank=True, null=True)
    #Trails/Demos
    trail = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    
    
    date_created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_daily_target')
    def __str__(self):
        return self.todays_motivation
    





class AssignProduct(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    target = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    date_created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_product')

    def __str__(self):
        return f"Assigned {self.product.name if self.product else 'Unknown Product'} to {self.user.email if self.user else 'Unknown User'}"

    


class ScheduleCalls(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    call_msg_CHOICES = [
        ('call', 'Call'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('msg', 'Msg'),
    ]
    schedule_for = models.CharField(max_length=255,choices=call_msg_CHOICES, blank=True, null=True)
    date_time = models.DateField(default=timezone.now, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedule_call')
    is_sent = models.BooleanField(default=False)
    def __str__(self):
        return self.lead
    

class LeadSummary(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)], default=1)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='lead_summary')
    def __str__(self):
        return self.summary

class ContactActivity(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    type_CHOICES = [
        ('call', 'Call'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('msg', 'Msg'),
    ]
    contact_type = models.CharField(max_length=255,choices=type_CHOICES, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.contact_type
      


class JunkReason(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, related_name='junk_reason')
    client_industry_relevance = models.CharField(max_length=3, choices=[('yes', 'YES'), ('no', 'NO')],blank=True, null=True)
    client_budget = models.CharField(max_length=3, choices=[('yes', 'YES'), ('no', 'NO')],blank=True, null=True)
    client_authority = models.CharField(max_length=3, choices=[('yes', 'YES'), ('no', 'NO')],blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.details
    # def save(self, *args, **kwargs):
    #     if len(self.details.split()) < 1:
    #         raise ValueError("Details for junk reason must be at least 20 words.")
    #     super().save(*args, **kwargs)


class LostReason(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, related_name='lost_reason')
    client_no_industry = models.CharField(max_length=3, choices=[('yes', 'YES'), ('no', 'NO')],blank=True, null=True)
    client_no_budget = models.CharField(max_length=3, choices=[('yes', 'YES'), ('no', 'NO')],blank=True, null=True)
    needs_no_satisfied = models.CharField(max_length=3, choices=[('yes', 'YES'), ('no', 'NO')],blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.details


class AuditLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    resource_name = models.CharField(max_length=255, null=True, blank=True)  # e.g., "Lead"
    resource_id = models.PositiveIntegerField(null=True, blank=True)  # Affected resource ID
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    changes = models.JSONField(null=True, blank=True)  # For tracking what changed

    def __str__(self):
        return f"AuditLog {self.id} - {self.action}"


class Calendar(models.Model):
    date = models.DateField(null=False, blank=False, unique=True)

    def __str__(self):
        return str(self.date)

class Category(models.Model):
    DANGER = 'Danger'
    SUCCESS = 'Success'
    PRIMARY = 'Primary'
    INFO = 'Info'
    DARK = 'Dark'
    WARNING = 'Warning'

    CATEGORY_CHOICES = [
        (DANGER, 'Danger'),
        (SUCCESS, 'Success'),
        (PRIMARY, 'Primary'),
        (INFO, 'Info'),
        (DARK, 'Dark'),
        (WARNING, 'Warning'),
    ]

    name = models.TextField(null=False, blank=False)

    def clean(self):
        if self.name not in dict(self.CATEGORY_CHOICES):
            raise ValidationError(('Invalid category'))

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Folder(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    folder = models.ForeignKey(Folder, related_name="files", on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    size = models.FloatField(null=True, blank=True)  # File size in MB
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    file_type = models.CharField(max_length=50, null=True, blank=True)
    path = models.FileField(upload_to="files/", null=True, blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    url = models.URLField(blank=True, null=True)
    media = models.FileField(upload_to='media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} likes {self.post}'



class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
    



class Contest(models.Model):
    name = models.CharField(max_length=255)
    objective = models.TextField()
    description = models.TextField(blank=True, null=True)
    attached_file = models.FileField(upload_to='contest_files/', blank=True, null=True)
    department = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contests')
    launch_date = models.DateTimeField()
    due_date = models.DateTimeField()
    company = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
