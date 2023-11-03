from datetime import datetime
import io
from django.db.models import Sum
from django.template.loader import render_to_string
from dotenv import load_dotenv
from apps.order.models import Order, OrderItem
from apps.user.models import BaseUserModel
from apps.product.models import ProductModel
from django.shortcuts import render
from django.http import FileResponse
from django.http import HttpResponse
import pdfkit
import os

load_dotenv()


def stats_view(request):
    all_clients_count = BaseUserModel.objects.filter(is_staff=False).count()
    individual_users_count = BaseUserModel.objects.filter(user_type='individual', is_staff=False).count()
    company_users_count = BaseUserModel.objects.filter(user_type='company', is_staff=False).count()
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None
    orders = Order.objects.all()
    if start_date:
        orders = orders.filter(date_created__gte=start_date)
    if end_date:
        orders = orders.filter(date_created__lte=end_date)
    sold_items_count = orders.aggregate(Sum('total_quantity'))['total_quantity__sum'] or 0
    sales = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

    orders_stats = {
        name: Order.objects.filter(status=status).count()
        for status, name in Order.ORDER_STATUS_CHOICES
    }
    active_products_count = ProductModel.objects.filter(is_active=True).count()
    inactive_products_count = ProductModel.objects.filter(is_active=False).count()
    total_product_cards = ProductModel.objects.count()
    context = {
        'all_clients_count': all_clients_count,
        'individual_users_count': individual_users_count,
        'company_users_count': company_users_count,
        'sold_items_count': sold_items_count,
        'sales': sales,
        'orders_stats': orders_stats,
        'active_products_count': active_products_count,
        'inactive_products_count': inactive_products_count,
        'total_product_cards': total_product_cards,
    }
    return render(request, 'admin/statistics.html', context)


def create_pdf(request):
    all_clients_count = BaseUserModel.objects.filter(is_staff=False).count()
    individual_users_count = BaseUserModel.objects.filter(user_type='individual', is_staff=False).count()
    company_users_count = BaseUserModel.objects.filter(user_type='company', is_staff=False).count()
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None
    orders = Order.objects.all()
    if start_date:
        orders = orders.filter(date_created__gte=start_date)
    if end_date:
        orders = orders.filter(date_created__lte=end_date)
    sold_items_count = orders.aggregate(Sum('total_quantity'))['total_quantity__sum'] or 0
    sales = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

    orders_stats = {
        name: Order.objects.filter(status=status).count()
        for status, name in Order.ORDER_STATUS_CHOICES
    }
    active_products_count = ProductModel.objects.filter(is_active=True).count()
    inactive_products_count = ProductModel.objects.filter(is_active=False).count()
    total_product_cards = ProductModel.objects.count()
    context = {
        'all_clients_count': all_clients_count,
        'individual_users_count': individual_users_count,
        'company_users_count': company_users_count,
        'sold_items_count': sold_items_count,
        'sales': sales,
        'orders_stats': orders_stats,
        'active_products_count': active_products_count,
        'inactive_products_count': inactive_products_count,
        'total_product_cards': total_product_cards,
    }

    pdfkit_config = pdfkit.configuration(wkhtmltopdf=os.getenv('PDK_CONFIG'))
    html_template = render_to_string('admin/to_pdf.html', context)
    pdf_content = pdfkit.from_string(html_template, False, configuration=pdfkit_config)
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="statistics.pdf"'
    return response