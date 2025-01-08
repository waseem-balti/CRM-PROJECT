from django import forms
from .models import Company, Branch, Department, Currency, DpartmentalGoal, KPI, Funnel, LeadSource, Invoice, DailyTarget,ScheduleCalls,LeadSummary

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'website', 'email', 'phone_number','logo']

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['logo'].required = False


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = [ 'name','company', 'location', 'contact_person', 'contact_email', 'contact_phone']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BranchForm, self).__init__(*args, **kwargs)
        user_companies = Company.objects.filter(created_by=user)
        # user_companies = Company.objects.all()
        self.fields['company'].queryset = user_companies


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['branch','name', 'description'] #, 'head_of_department', 'contact_email', 'contact_phone'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DepartmentForm, self).__init__(*args, **kwargs)
        if user.is_company_owner==True:
            user_companies = Branch.objects.filter(created_by=user)
            # user_companies = Branch.objects.all()
            self.fields['branch'].queryset = user_companies
        else:
            user_companies = Branch.objects.filter(created_by=user.created_by)
            # user_companies = Branch.objects.all()
            self.fields['branch'].queryset = user_companies


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = [ 'name','branch' ,'code', 'symbol']
 
class DpartmentalGoalForm(forms.ModelForm):
    class Meta:
        model = DpartmentalGoal
        fields = ['department','mission','from_date','to_date','goal']
    



class KPIForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = ['department','expected_leads','kpi','target']
       

class FunnelForm(forms.ModelForm):
    class Meta:
        model = Funnel
        fields = ['department','stage']


class LeadSourceForm(forms.ModelForm):
    class Meta:
        model = LeadSource
        fields = '__all__'




# <-----------------------------------------------------User Forms ------------------------------------------------------------------------>

from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django import forms
from .models import CustomUser, UserProfile

class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm password (again) ",widget= forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email"] #branch
        labels = {"email": "Email"}

class EditUserprofileForm(UserChangeForm):
    password = None
    class Meta:
        model =CustomUser
        fields = ["username","first_name","last_name","email"]
        labels={"email":"Email"}


class EditAdminprofileForm(UserChangeForm):
    password = None
    class Meta:
        model =CustomUser
        fields = "__all__"
        labels={"email":"Email"}
        exclude = ['password','last_login','groups','user_permissions','date_joined','created_by','branch','department']


class EditOwnerprofileForm(UserChangeForm):
    password = None
    class Meta:
        model =CustomUser
        fields = ["username", "first_name", "last_name", "email",'is_branch_head','is_diractor','is_department_head','is_manager','is_executive'] 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user','manager']

class CompanyOwnerForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm password (again) ",widget= forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email", 'is_company_owner', 'no_of_branch','no_of_department']
        labels={"email":"Email"}



class BranchHeadrForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm password (again) ",widget= forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email", 'is_branch_head']
        labels={"email":"Email"}


class DirectorForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm password (again) ",widget= forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email", 'is_diractor']
        labels={"email":"Email"}


class DepartmentHeadForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm password (again) ",widget= forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email", 'is_department_head']
        labels={"email":"Email"}

class ManagerForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm password (again) ",widget= forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email", 'is_manager']
        labels={"email":"Email"}

class ExecutiveForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm password (again) ",widget= forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email", 'is_executive']
        labels={"email":"Email"}


class CustomeUserForm(UserCreationForm):
    password2 = forms.CharField(label="Confirm password (again) ",widget= forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email", 'is_executive','is_manager','is_department_head','is_diractor','is_branch_head']
        labels={"email":"Email"}



from .models import Contact, Price, ProductQuotation, ProductService, Product,AssignProduct
#-----------------------------------Inventory-------------------------------------------------------------
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['branch', 'assigned_to']


class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['price_book_name', 'active','currency','description']

class ProductQuotationForm(forms.ModelForm):
    class Meta:
        model = ProductQuotation
        fields = '__all__'



class ProductServiceForm(forms.ModelForm):
    class Meta:
        model = ProductService
        fields = '__all__'
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['branch']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude = ['date_created','price_per_month','branch', 'customer', 'product','price']

#-----------------------------------Marketing-------------------------------------------------------------

from .models import Campaign, Lead, Organization

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = '__all__'
        exclude = ['branch']
        


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'
        exclude = ['branch']

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Disable the mobile_phone field during editing
            self.fields['mobile_phone'].widget.attrs['disabled'] = True

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        # Exclude the current instance from the check if it's being edited
        if Lead.objects.filter(mobile_phone=mobile_phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A lead with this mobile number already exists.")
        return mobile_phone
    
    

class ImportLeadsForm(forms.Form):
    file = forms.FileField()


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'


class DailyTargetForm(forms.ModelForm):
    class Meta:
        model = DailyTarget
        fields = '__all__'
        exclude = ['date_created']



class AssignProductForm(forms.ModelForm):
    class Meta:
        model = AssignProduct
        fields = '__all__'
        exclude = ['date_created']


class ScheduleCallsForm(forms.ModelForm):
    class Meta:
        model = ScheduleCalls
        fields = '__all__'
        exclude = ['created_by','lead']


class ScheduleCallsForm(forms.ModelForm):
    class Meta:
        model = ScheduleCalls
        fields = '__all__'
        exclude = ['created_by','lead']


class LeadSummaryForm(forms.ModelForm):
    class Meta:
        model = LeadSummary
        fields = '__all__'
        exclude = ['created_by','lead','date_created']



from .models import JunkReason, LostReason

class JunkReasonForm(forms.ModelForm):
    class Meta:
        model = JunkReason
        fields = ['client_industry_relevance', 'client_budget', 'client_authority', 'details']



class LostReasonForm(forms.ModelForm):
    class Meta:
        model = LostReason
        fields = ['client_no_industry', 'client_no_budget', 'needs_no_satisfied', 'details']
