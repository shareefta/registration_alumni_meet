from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from .forms import *
from django.contrib import messages
import pandas as pd
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from django.db.models import Count, Sum

# Create your views here.
def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
    else:
        form = AdminLoginForm()
    return render(request, 'admin/admin_login.html', {'form': form})

@login_required
def admin_dashboard(request):
    reg_alumni = Alumni.objects.all().count()
    reg_wives = Alumni.objects.filter(name_of_wife__isnull=False).exclude(name_of_wife="").count()
    reg_children_below_5 = Alumni.objects.all().aggregate(Sum('no_of_child_below_5'))['no_of_child_below_5__sum'] or 0
    reg_children_above_5 = Alumni.objects.all().aggregate(Sum('no_of_child_above_5'))['no_of_child_above_5__sum'] or 0
    total_reg = reg_alumni + reg_wives + reg_children_below_5 + reg_children_above_5
    
    total_alumni = Alumni.objects.filter(is_registered=True).count()
    total_wives = Alumni.objects.filter(is_registered=True, name_of_wife__isnull=False).exclude(name_of_wife="").count()
    total_children_below_5 = Alumni.objects.filter(is_registered=True).aggregate(Sum('no_of_child_below_5'))['no_of_child_below_5__sum'] or 0
    total_children_above_5 = Alumni.objects.filter(is_registered=True).aggregate(Sum('no_of_child_above_5'))['no_of_child_above_5__sum'] or 0
    total_participants = total_alumni + total_wives + total_children_below_5 + total_children_above_5
    
    context = {
        'reg_alumni': reg_alumni,
        'reg_wives' : reg_wives,
        'reg_children_below_5' : reg_children_below_5,
        'reg_children_above_5': reg_children_above_5,
        'total_reg' : total_reg,
        'total_alumni': total_alumni,
        'total_wives': total_wives,
        'total_children_below_5': total_children_below_5,
        'total_children_above_5': total_children_above_5,
        'total_participants': total_participants,
    }
    
    return render(request, 'admin/admin_dashboard.html', context)

@login_required
def alumni(request):    
    return render(request, 'alumni/alumni.html')

@login_required
def alumni_list(request):
    alumni = Alumni.objects.all().order_by(Lower('name'))
    
    paginator = Paginator(alumni, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'alumni/alumni_list.html', {'page_obj' : page_obj})

@login_required
def alumni_create(request):
    if request.method == 'POST':
        form = AlumniForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alumni_list')
    else:
        form = AlumniForm()
    return render(request, 'alumni/alumni_registration.html', {'form': form})

@login_required
def alumni_update(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    if request.method == 'POST':
        form = AlumniForm(request.POST, instance=alumni)
        if form.is_valid():
            form.save()
            return redirect('alumni_list')
    else:
        form = AlumniForm(instance=alumni)
    return render(request, 'alumni/alumni_registration.html', {'form': form})

def alumni_delete(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    alumni.delete()
    messages.success(request, 'Alumni record deleted successfully!')
    return redirect('alumni_list')

@login_required
def alumni_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
                try:
                    # Read the Excel file
                    df = pd.read_excel(file)
                    df.columns = [col.strip().lower() for col in df.columns]
                    # Process the file and save to the database
                    for index, row in df.iterrows():
                        alumni_data = {
                            'name': row.get('name'),
                            'place': row.get('place'),
                            'mobile_number': row.get('mobile_number'),
                            'whatsapp_number': row.get('whatsapp_number'),
                            'name_of_wife': row.get('name_of_wife'),
                            'no_of_child_below_5': row.get('no_of_child_below_5'),
                            'no_of_child_above_5': row.get('no_of_child_above_5'),
                        }

                        form = AlumniForm(data=alumni_data)
                        if form.is_valid():
                            form.save()
                        else:
                            messages.error(request, f"Error with row {index + 1}: {form.errors}")

                    messages.success(request, 'Alumni uploaded successfully.')
                    return redirect('alumni_list')
                except Exception as e:
                    print('Step 9')
                    messages.error(request, f'Error processing file: {e}')
            else:
                messages.error(request, 'Please upload an Excel file.')
        else:
            print('Form is not valid')
    else:
        form = UploadFileForm()

    return render(request, 'alumni/upload_alumni.html', {'form': form})

@login_required
def export_pdf_alumni(request):
    alumni = Alumni.objects.all()

    context = {'alumni': alumni}
    html_string = render_to_string('alumni/alumni_list_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="alumni_list.pdf"'

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
    if not pdf.err:
        response.write(result.getvalue())
        return response
    return None

def export_pdf_participants(request):
    participants = Alumni.objects.filter(is_registered=True)

    context = {'participants': participants}
    html_string = render_to_string('alumni/participants_list_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="participants_list.pdf"'

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
    if not pdf.err:
        response.write(result.getvalue())
        return response
    return None

@login_required
def participants_list(request):
    participants = Alumni.objects.filter(is_registered=True).order_by(Lower('name'))
    
    paginator = Paginator(participants, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'alumni/participants_list.html', {'page_obj' : page_obj})

@login_required
def admin_logout(request):
    logout(request)
    return redirect('login')

def alumni_home(request):
    return render(request, 'alumni/alumni_home_user.html')

