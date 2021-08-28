from django.contrib.auth.decorators import permission_required
from django.db.models import Sum, Count, Q, F
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from order.models import Order, ShoppingCart
from product.models import Book
from users.models import Customer, Personnel
from jdatetime import datetime
from datetime import date, timedelta
from django.http import HttpResponse
from .resources import OrderResource


@permission_required('product.view_category', raise_exception=True)
def admin_dashboard(request):
    """ Big function for passing required data to template """
    today_jalali = datetime.now().strftime("%H:%M:%S %Y-%m-%d")
    this_month = timezone.now().today().month
    month_orders_count = Order.objects.filter(order_date__month=this_month).count()

    today = timezone.now().day
    print(today)
    yesterday = timezone.now() - timedelta(days=1)
    yesterday = yesterday.day
    day_before_yesterday = timezone.now() - timedelta(days=2)
    day_before_yesterday = day_before_yesterday.day

    today_orders_count = Order.objects.filter(order_date__day=today).count()

    all_orders_count = Order.objects.count()

    customers = Customer.objects.all()

    all_customers_count = Customer.objects.count()
    all_authenticate_customers_count = Customer.objects.filter(email__isnull=False).count()

    today_authenticate_customers_count = Customer.objects.filter(date_joined__day=today, email__isnull=False).count()
    yesterday_authenticate_customers_count = Customer.objects.filter(date_joined__day=yesterday,
                                                                     email__isnull=False).count()
    before_yesterday_authenticate_customers_count = Customer.objects.filter(date_joined__day=day_before_yesterday,
                                                                            email__isnull=False).count()
    today_not_authenticate_customers_count = Customer.objects.filter(date_joined__day=today, email__isnull=True).count()
    yesterday_not_authenticate_customers_count = Customer.objects.filter(date_joined__day=yesterday,
                                                                         email__isnull=True).count()
    before_yesterday_not_authenticate_customers_count = Customer.objects.filter(date_joined__day=day_before_yesterday,
                                                                                email__isnull=True).count()

    today_customers_count = Customer.objects.filter(date_joined__day=today).count()
    yesterday_customers_count = Customer.objects.filter(date_joined__day=yesterday).count()
    before_yesterday_customers_count = Customer.objects.filter(date_joined__day=day_before_yesterday).count()

    total_sales_price = Order.objects.aggregate(total=Sum('total_price'))
    today_sales_price = Order.objects.filter(order_date__day=today).aggregate(total=Sum('total_price'))

    personnel = Personnel.objects.all()
    personnel_count = Personnel.objects.count()

    # chart for best sellers
    book_labels = []
    book_data = []

    best_sellers_books = ShoppingCart.objects.select_related('order').filter(order__status='submit').values(
        'item_id').annotate(total=Count('item_id')).order_by('-total').values_list('total', 'item__title')[:5]
    print(best_sellers_books)
    for book in best_sellers_books:
        book_labels.append(book[1])
        book_data.append(book[0])

    # chart for with discount and without discount books
    discount_labels = []
    discount_data = []

    discount_products = Book.objects.aggregate(
        # all_books=Count('id'),
        کتاب_های_با_تخفیف=Count('id', filter=Q(discount__isnull=False)),
        کتاب_های_بدون_تخفیف=Count('id', filter=Q(discount__isnull=True)),
    )
    for key in discount_products:
        discount_labels.append(key)
        discount_data.append(discount_products[key])

    return render(request, 'rtl.html', {
        'today_jalali': today_jalali,

        'all_orders_count': all_orders_count,
        'month_orders': month_orders_count,
        'today_orders_count': today_orders_count,

        'all_authenticate_customers_count': all_authenticate_customers_count,
        'today_authenticate_customers_count': today_authenticate_customers_count,
        'today_not_authenticate_customers_count': today_not_authenticate_customers_count,
        'yesterday_authenticate_customers_count': yesterday_authenticate_customers_count,
        'yesterday_not_authenticate_customers_count': yesterday_not_authenticate_customers_count,
        'before_yesterday_authenticate_customers_count': before_yesterday_authenticate_customers_count,
        'before_yesterday_not_authenticate_customers_count': before_yesterday_not_authenticate_customers_count,

        'all_customers_count': all_customers_count,
        'today_customers_count': today_customers_count,
        'yesterday_customers_count': yesterday_customers_count,
        'before_yesterday_customers_count': before_yesterday_customers_count,

        'total_sales_price': total_sales_price,
        'today_sales_price': today_sales_price,
        'personnel': personnel,
        'personnel_count': personnel_count,

        # charts
        'book_labels': book_labels,
        'book_data': book_data,

        'discount_labels': discount_labels,
        'discount_data': discount_data,

    })


# --------------------------------------------------------------------
def orders_chart(request):
    """ this function is for drawing order numbers per day """
    labels = []
    data = []
    queryset = Order.objects.extra({'order_date': "date(order_date)"}).values(
        'order_date').annotate(order_count=Count('id'))
    print(queryset)

    for entry in queryset:
        labels.append(entry['order_date'])
        print(entry['order_date'])
        data.append(entry['order_count'])
        print(entry['order_count'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


# --------------------------------------------------------------------
def export(request):
    """ function for export orders of day in xls file """
    today = timezone.now().day
    person_resource = OrderResource()
    queryset = Order.objects.filter(order_date__day=today, status='submit')
    dataset = person_resource.export(queryset)
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="orders.xls"'
    return response
