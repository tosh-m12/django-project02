from django.shortcuts import render, get_object_or_404, redirect
from .models import DailyReport, Employee
from datetime import datetime, date, timedelta
from calendar import monthrange
from django.views.decorators.csrf import csrf_exempt
import csv
from io import TextIOWrapper, StringIO
from django.contrib import messages
from django.http import HttpResponse

def index(request):
    # 対象日（パラメータ or 今日）
    target_str = request.GET.get('date')
    if target_str:
        try:
            target_date = datetime.strptime(target_str, '%Y-%m-%d').date()
        except:
            target_date = date.today()
    else:
        target_date = date.today()

    # 全従業員取得（有効な人のみ）
    employees = Employee.objects.filter(is_active=True).order_by('name')

    # 日報データを従業員ごとに取得
    reports = {r.employee_id: r for r in DailyReport.objects.filter(date=target_date)}

    context = {
        'target_date': target_date,
        'employees': employees,
        'reports': reports,
    }
    return render(request, 'daily_report_app/index.html', context)

def employee_edit(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    # 年月指定（なければ今月）
    try:
        year = int(request.GET.get('year', date.today().year))
        month = int(request.GET.get('month', date.today().month))
    except ValueError:
        year, month = date.today().year, date.today().month

    num_days = monthrange(year, month)[1]
    month_dates = [date(year, month, day) for day in range(1, num_days + 1)]

    if request.method == 'POST':
        for d in month_dates:
            d_str = d.strftime('%Y-%m-%d')
            fields = {}
            updated = False

            for field in ['inbound', 'outbound', 'shipment', 'customs', 'delivery', 'special_tag']:
                val = request.POST.get(f'{field}_{d_str}')
                if val is not None:
                    val = val.strip()
                    if val == '':
                        fields[field] = None  # 空欄 → None
                        updated = True
                    else:
                        try:
                            num = int(val)
                            if num >= 0:
                                fields[field] = num
                                updated = True
                        except ValueError:
                            continue  # 無効な入力は無視

            remarks_val = request.POST.get(f'remarks_{d_str}')
            if remarks_val is not None:
                fields['remarks'] = remarks_val.strip()  # 空欄OK
                updated = True

            if updated:
                r, _ = DailyReport.objects.get_or_create(employee=employee, date=d)
                for key, value in fields.items():
                    setattr(r, key, value)
                r.save()


        return redirect(f'{request.path}?year={year}&month={month}')






    reports = DailyReport.objects.filter(employee=employee, date__year=year, date__month=month)
    report_dict = {r.date: r for r in reports}

    context = {
        'employee': employee,
        'year': year,
        'month': month,
        'month_dates': month_dates,
        'reports': report_dict,
    }
    return render(request, 'daily_report_app/employee_edit.html', context)

@csrf_exempt
def employee_list(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            name = request.POST.get('name', '').strip()
            if name:
                Employee.objects.create(name=name)

        elif action == 'delete':
            emp_id = request.POST.get('id')
            Employee.objects.filter(id=emp_id).delete()

        elif action == 'update':
            emp_id = request.POST.get('id')
            new_name = request.POST.get('name', '').strip()
            if emp_id and new_name:
                emp = Employee.objects.get(id=emp_id)
                emp.name = new_name
                emp.save()

        return redirect('employee_list')

    employees = Employee.objects.all()
    return render(request, 'daily_report_app/employee_list.html', {'employees': employees})

def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.DictReader(file_data)

        reader.fieldnames = [name.strip().lstrip('\ufeff') for name in reader. fieldnames]

        imported = 0
        for row in reader:
            try:
                employee_name = row['name'].strip()
                date_str = row['date'].strip()
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

                employee, _ = Employee.objects.get_or_create(name=employee_name)

                report, _ = DailyReport.objects.get_or_create(employee=employee, date=date_obj)
                report.inbound = int(row.get('inbound', 0) or 0)
                report.outbound = int(row.get('outbound', 0) or 0)
                report.shipment = int(row.get('shipment', 0) or 0)
                report.customs = int(row.get('customs', 0) or 0)
                report.delivery = int(row.get('delivery', 0) or 0)
                report.special_tag = int(row.get('special_tag', 0) or 0)
                report.remarks = row.get('remarks', '')
                report.save()
                imported += 1
            except Exception as e:
                print(f'Error: {e}')
                continue

        messages.success(request, f'{imported} 件のデータを取り込みました。')
        return redirect('upload_csv')

    return render(request, 'daily_report_app/upload_csv.html')

def download_csv(request):
    target_str = request.GET.get('date')
    all_data = request.GET.get('all_data') == 'on'

    if all_data:
        reports = DailyReport.objects.select_related('employee').order_by('date', 'employee__name')
        filename = 'daily_report_all.csv'
    else:
        try:
            target_date = datetime.strptime(target_str, '%Y-%m-%d').date() if target_str else date.today()
        except ValueError:
            target_date = date.today()
        reports = DailyReport.objects.filter(date=target_date).select_related('employee')
        filename = f'daily_report_{target_date.strftime("%Y%m%d")}.csv'

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['name', 'date', 'inbound', 'outbound', 'shipment', 'customs', 'delivery', 'special_tag', 'remarks'])

    for r in reports:
        writer.writerow([
            str(r.employee.name),
            r.date.strftime('%Y-%m-%d'),  # ← 修正ポイント！
            str(r.inbound),
            str(r.outbound),
            str(r.shipment),
            str(r.customs),
            str(r.delivery),
            str(r.special_tag),
            str(r.remarks),
        ])

    response = HttpResponse(
        content='\ufeff' + buffer.getvalue(),
        content_type='text/csv'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

