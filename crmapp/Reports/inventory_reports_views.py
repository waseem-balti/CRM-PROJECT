from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from .inventory_report_serializers import (
    ProductSerializer, LeadSerializer, CampaignSerializer,
    FunnelSerializer, KPISerializer, LeadSourceSerializer, InvoiceSerializer
)
from crmapp.models import Product, Lead, Campaign, Department, Funnel, KPI, LeadSource, Invoice, Branch


class InventoryReportAPI(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def validate_query_params(self, request):
        search_query = request.GET.get('search_query', '')
        if search_query and len(search_query) > 100:
            raise ValidationError("Search query too long. Limit it to 100 characters.")

    def get(self, request):
        # Validate query params
        self.validate_query_params(request)

        # Determine branches accessible by the user
        if request.user.is_company_owner:
            branches = Branch.objects.filter(created_by=request.user)
        else:
            if not hasattr(request.user, 'branch') or not request.user.branch:
                branches = Branch.objects.all()  # Allow access to all branches if user has no specific branch
            else:
                branches = Branch.objects.filter(pk=request.user.branch.id)

            # if not hasattr(request.user, 'branch') or not request.user.branch:
            #     branches = Branch.objects.all()  # Allow access to all branches if user has no specific branch
            # else:
            #     branches = Branch.objects.filter(pk=request.user.branch.id)

        # Fetch query params
        search_query = request.GET.get('search_query')
        filter_by_lead_status = request.GET.get('lead_status')
        leads_by_campaign = request.GET.get('campaign')
        lead_source_filter = request.GET.get('lead_source')

        # Filtering logic
        if search_query:
            search_conditions = Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(email__icontains=search_query)
            customers = Lead.objects.filter(search_conditions)
            search_product = Q(name__icontains=search_query) | Q(manufacturer__icontains=search_query) | Q(vendor_name__icontains=search_query) | Q(product_category__icontains=search_query)
            products = Product.objects.filter(search_product)

        elif leads_by_campaign:
            campaign = Campaign.objects.filter(id=leads_by_campaign).first()
            if not campaign:
                return Response({"error": "Invalid campaign ID."}, status=400)
            customers = Lead.objects.filter(campaign=campaign)
            products = Product.objects.filter(branch__in=branches)

        elif filter_by_lead_status:
            customers = Lead.objects.filter(lead_status=filter_by_lead_status)
            products = Product.objects.filter(branch__in=branches)

        elif lead_source_filter:
            customers = Lead.objects.filter(lead_source=lead_source_filter)
            products = Product.objects.filter(branch__in=branches)

        else:
            customers = Lead.objects.filter(branch__in=branches)
            products = Product.objects.filter(branch__in=branches)

        # Additional queries
        campaigns = Campaign.objects.filter(branch__in=branches)
        departments = Department.objects.filter(branch__in=branches, name='Sales')
        lead_funnel = Funnel.objects.filter(department__in=departments)
        kpi_targets = KPI.objects.filter(department__in=departments)
        lead_sources = LeadSource.objects.filter(branch__in=branches)
        invoices = Invoice.objects.filter(branch__in=branches)

        # Calculations
        customers = customers.filter(deal_close=True)
        total_customers = customers.count()
        total_products = products.count()
        revenue_generated = sum(invoice.price_per_month for invoice in invoices)

        # Serialize data
        data = {
            'products': ProductSerializer(products, many=True).data,
            'customers': LeadSerializer(customers, many=True).data,
            'total_customers': total_customers,
            'total_products': total_products,
            'revenue_generated': revenue_generated,
            'campaigns': CampaignSerializer(campaigns, many=True).data,
            'lead_funnel': FunnelSerializer(lead_funnel, many=True).data,
            'kpi_targets': KPISerializer(kpi_targets, many=True).data,
            'lead_sources': LeadSourceSerializer(lead_sources, many=True).data,
            'invoices': InvoiceSerializer(invoices, many=True).data,
        }

        return Response(data)
