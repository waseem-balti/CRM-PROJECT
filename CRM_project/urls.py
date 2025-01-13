from django.contrib import admin
from django.urls import include, path
from crmapp.swagger import urlpatterns as swagger_urls
from django.conf import settings
from django.conf.urls.static import static
from crmapp.Auth import  auth_urls
from crmapp.crm_user import  user_profile_urls
from crmapp.company import  lead_urls, branch_urls, company_urls, funnel_urls, company_department_urls, junk_reason_urls, kpi_urls, lostreason_urls, currency_urls
from crmapp.trailAcc import trail_urls
from crmapp.opportunity import opportunity_urls
from crmapp.customer import customer_urls
from crmapp.assignproducts import assign_product_urls
from crmapp.dailytargets import daily_target_urls
from crmapp.schedulecalls import schedule_calls_urls
from crmapp.contactactivity import contact_activity_urls
from crmapp.leadsummary import lead_summary_urls
from crmapp.Inventory import Contact_urls,Price_urls,Product_urls,Organization_urls,Quotation_urls,invoice_urls,Project_urls
from crmapp.Reports import inventory_report_urls, product_report_urls, campaign_report_urls
from crmapp.campaign import campaign_urls
from crmapp.UserMenagement import User_Management_urls
from crmapp.payments import payment_urls
from crmapp.audit import audit_urls
from crmapp.calendar import calendar_urls
from crmapp.FileMenagement import FileManagement_urls
from crmapp.social_feeds import social_feeds_urls
from crmapp.tasks import task_urls



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(swagger_urls)),
    path('auth/', include(auth_urls)),
    path('userprofile/', include(user_profile_urls)),
    path('leads/', include(lead_urls)),
    path('branches/', include(branch_urls)),
    path('company/', include(company_urls)),
    path('funnels/', include(funnel_urls)),
    path('deparments/', include(company_department_urls)),
    path('junkreasons/', include(junk_reason_urls)),
    path('kpis/', include(kpi_urls)),
    path('lostreason/', include(lostreason_urls)),
    path('currency/', include(currency_urls)),
    path('trail/', include(trail_urls)),
    path('oppertunity/', include(opportunity_urls)),
    path('customer/', include(customer_urls)),
    path('invoice/', include(invoice_urls)),
    path('assignproduct/', include(assign_product_urls)),
    path('contactactivity/', include(contact_activity_urls)),
    path('schedulecall/', include(schedule_calls_urls)),
    path('dailytarget/', include(daily_target_urls)),
    path('leadsummary/', include(lead_summary_urls)),
    path('contact/', include(Contact_urls)),
    path('price/', include(Price_urls)),
    path('product/', include(Product_urls)),
    path('organization/', include(Organization_urls)),
    path('ProductQuotation/', include(Quotation_urls)),
    path('InventoryReports/', include(inventory_report_urls)),
    path('campaigns/', include(campaign_urls)),
    path('ProductReports/', include(product_report_urls)),
    path('CampaignReports/', include(campaign_report_urls)),
    path('UserManagement/', include(User_Management_urls)),
    path('payments/', include(payment_urls)),
    path('audit/', include(audit_urls)),
    path('calendar/', include(calendar_urls)),
    path('file/', include(FileManagement_urls)),
    path('CreateProject/', include(Project_urls)),
    path('socialfeeds/', include(social_feeds_urls)),
    path('tasks/', include(task_urls)),
    # path('addcustomer/', include(add_customer_urls)),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)