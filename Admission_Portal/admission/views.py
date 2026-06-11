from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
import csv
import datetime
from django.conf import settings





# NOTE: admission/models.py is missing in this project snapshot.
# Your views import models from .models, which crashes Django startup.
# For now comment out model import so the server can start.

from .models import Application, Course, Documents, Student, ApprovalDecisionHistory, ContactMessage

from .forms import ApplicationForm, DocumentUploadForm, StudentProfileForm, StudentRegistrationForm, ContactForm



def index_view(request):

    courses = Course.objects.filter(is_active=True)
    return render(request, 'index.html', {'courses': courses})
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_form = StudentRegistrationForm(request.POST)
        profile_form = StudentProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            student = profile_form.save(commit=False)
            student.user = user
            student.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to the student portal.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = StudentRegistrationForm()
        profile_form = StudentProfileForm()
        
    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
def login_view(request):
    if request.user.is_authenticated:
        # Check if admin
        if request.user.is_staff or hasattr(request.user, 'admin_profile'):
            return redirect('admin_dashboard')
        return redirect('dashboard')

    courses = Course.objects.filter(is_active=True).order_by('code')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                if user.is_staff or hasattr(user, 'admin_profile'):
                    return redirect('admin_dashboard')
                return redirect('dashboard')
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'courses': courses})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')
@login_required
def dashboard_view(request):
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        # If user is staff, redirect to admin
        if request.user.is_staff or hasattr(request.user, 'admin_profile'):
            return redirect('admin_dashboard')
        # Otherwise, force profile creation or log out
        messages.error(request, "Student profile not found. Please log in as a student.")
        logout(request)
        return redirect('login')
    applications = Application.objects.filter(student=student).order_by('-submission_date')
    documents = Documents.objects.filter(student=student)
    
    context = {
        'student': student,
        'applications': applications,
        'documents': documents,
        'has_applied': applications.exists()
    }
    return render(request, 'dashboard.html', context)
@login_required
def apply_view(request):
    student = get_object_or_404(Student, user=request.user)
    
    # Check if student already has a pending or approved application
    existing_app = Application.objects.filter(student=student, status__in=['Pending', 'Approved']).first()
    if existing_app:
        messages.warning(request, f"You already have a {existing_app.status.lower()} application ({existing_app.application_number}).")
        return redirect('status')
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = student
            application.status = 'Pending'
            application.save()
            messages.success(request, "Application submitted successfully! Please upload your documents to complete the process.")
            return redirect('upload')
    else:
        form = ApplicationForm()
        
    return render(request, 'admission_form.html', {'form': form})
@login_required
def upload_view(request):
    student = get_object_or_404(Student, user=request.user)
    application = Application.objects.filter(student=student).order_by('-submission_date').first()
    
    if not application:
        messages.warning(request, "Please fill out the admission form before uploading documents.")
        return redirect('apply')
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.student = student
            document.application = application
            
            # Check if this type of document was already uploaded
            existing = Documents.objects.filter(student=student, application=application, document_type=document.document_type).first()
            if existing:
                existing.file = document.file
                existing.save()
                messages.success(request, f"Updated {existing.get_document_type_display()} successfully!")
            else:
                document.save()
                messages.success(request, f"Uploaded {document.get_document_type_display()} successfully!")
                
            return redirect('upload')
    else:
        form = DocumentUploadForm()
        
    uploaded_docs = Documents.objects.filter(student=student, application=application)
    required_types = [t[0] for t in Documents.DOCUMENT_TYPES]
    uploaded_types = [d.document_type for d in uploaded_docs]
    missing_types = [t for t in Documents.DOCUMENT_TYPES if t[0] not in uploaded_types]
    
    is_complete = len(uploaded_docs) >= len(required_types)
    return render(request, 'document_upload.html', {
        'form': form,
        'uploaded_docs': uploaded_docs,
        'missing_types': missing_types,
        'is_complete': is_complete,
        'application': application
    })
@login_required
def status_view(request):
    student = get_object_or_404(Student, user=request.user)
    application = Application.objects.filter(student=student).order_by('-submission_date').first()
    
    if not application:
        messages.info(request, "You have not submitted any applications yet.")
        return redirect('apply')
    uploaded_docs = Documents.objects.filter(student=student, application=application)
    doc_count = uploaded_docs.count()
    total_docs = len(Documents.DOCUMENT_TYPES)
    
    context = {
        'application': application,
        'doc_count': doc_count,
        'total_docs': total_docs,
        'docs_uploaded': doc_count >= total_docs,
    }
    return render(request, 'application_status.html', context)

# Admin views
def is_admin(user):
    # Stronger role check: staff or admin_profile.
    return bool(user and user.is_authenticated and (user.is_superuser or user.is_staff or hasattr(user, 'admin_profile')))

@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('dashboard')
        
    applications = Application.objects.all().order_by('-submission_date')
    
    # Filter by search
    q = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    course_filter = request.GET.get('course', '')
    
    if q:
        applications = applications.filter(
            student__user__first_name__icontains=q
        ) | applications.filter(
            student__user__last_name__icontains=q
        ) | applications.filter(
            application_number__icontains=q
        ) | applications.filter(
            student__user__username__icontains=q
        )
        
    if status_filter:
        applications = applications.filter(status=status_filter)
        
    if course_filter:
        applications = applications.filter(course_id=course_filter)
        
    courses = Course.objects.all()
    
    # Counts
    stats = {
        'total': Application.objects.count(),
        'pending': Application.objects.filter(status='Pending').count(),
        'approved': Application.objects.filter(status='Approved').count(),
        'rejected': Application.objects.filter(status='Rejected').count(),
    }
    
    pending_inquiries = ContactMessage.objects.filter(is_resolved=False).count()
    
    return render(request, 'admin_dashboard.html', {
        'applications': applications,
        'courses': courses,
        'stats': stats,
        'q': q,
        'status_filter': status_filter,
        'course_filter': course_filter,
        'pending_inquiries': pending_inquiries
    })
@login_required
def admin_application_detail(request, app_id):
    if not is_admin(request.user):
        return redirect('dashboard')

    application = get_object_or_404(Application, id=app_id)
    documents = Documents.objects.filter(application=application)
    history = ApprovalDecisionHistory.objects.filter(application=application).order_by('-created_at')

    return render(request, 'admin_application_detail.html', {
        'application': application,
        'documents': documents,
        'history': history,
    })

@login_required
def admin_application_update(request, app_id):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('dashboard')

    application = get_object_or_404(Application, id=app_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        remarks = request.POST.get('remarks')

        if status in ['Pending', 'Approved', 'Rejected']:
            from_status = application.status
            to_status = status

            application.status = to_status
            application.remarks = remarks
            application.save()

            # Persist immutable history row
            ApprovalDecisionHistory.objects.create(
                application=application,
                from_status=from_status,
                to_status=to_status,
                remarks=remarks,
                decided_by=request.user,
            )

            # Send email notification to student
            # (In production you'd use Celery; here it's synchronous.)
            from django.core.mail import send_mail

            subject = f"Admission application {application.application_number} update"
            if to_status == 'Approved':
                body_status = 'Approved'
            elif to_status == 'Rejected':
                body_status = 'Rejected'
            else:
                body_status = 'Pending'

            body = (
                f"Your admission application ({application.application_number}) has been updated to: {body_status}.\n\n"
                f"Remarks: {remarks or '-'}\n\n"
                "You can log in to your student dashboard to see the latest status in real time."
            )

            send_mail(
                subject=subject,
                message=body,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'no-reply@example.com',
                recipient_list=[application.student.user.email],
                fail_silently=True,
            )


            # Broadcast websocket message to the student
            from asgiref.sync import async_to_sync
            from channels.layers import get_channel_layer

            channel_layer = get_channel_layer()
            if channel_layer:
                async_to_sync(channel_layer.group_send)(
                    f"student_{application.student.user.id}",
                    {
                        'type': 'status_update',

                        'application_number': application.application_number,
                        'status': application.status,
                        'remarks': application.remarks,
                        'decided_at': datetime.datetime.utcnow().isoformat(),
                    },
                )

            messages.success(request, f"Application {application.application_number} updated to {to_status}.")
        else:
            messages.error(request, "Invalid status submitted.")

    return redirect('admin_dashboard')

@login_required
def admin_reports(request):
    if not is_admin(request.user):
        return redirect('dashboard')
        
    if request.GET.get('export') == 'csv':
        # Generate CSV of Approved applicants
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="approved_students_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Application Number', 'Username', 'Full Name', 'Email', 'Phone', 'Course Code', 'Course Name', 'Status', 'Date Approved'])
        
        approved_apps = Application.objects.filter(status='Approved')
        for app in approved_apps:
            writer.writerow([
                app.application_number,
                app.student.user.username,
                f"{app.student.user.first_name} {app.student.user.last_name}",
                app.student.user.email,
                app.student.phone,
                app.course.code,
                app.course.name,
                app.status,
                app.updated_at.strftime('%Y-%m-%d %H:%M')
            ])
            
        return response
        
    # Calculate stats for reporting dashboard
    total = Application.objects.count()
    approved = Application.objects.filter(status='Approved').count()
    pending = Application.objects.filter(status='Pending').count()
    rejected = Application.objects.filter(status='Rejected').count()
    
    admission_rate = round((approved / total * 100), 1) if total > 0 else 0
    
    courses = Course.objects.all()
    course_data = []
    max_count = 1
    for c in courses:
        count = c.applications.count()
        course_data.append({
            'name': c.name,
            'code': c.code,
            'count': count
        })
        if count > max_count:
            max_count = count
            
    # Calculate relative heights for custom dashboard charts
    for item in course_data:
        item['height_percent'] = int((item['count'] / max_count) * 80) + 10  # height between 10% and 90%
        
    context = {
        'total': total,
        'approved': approved,
        'pending': pending,
        'rejected': rejected,
        'admission_rate': admission_rate,
        'course_data': course_data,
    }
    return render(request, 'admin_reports.html', context)


@login_required
def admin_delete_student(request, student_id):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('dashboard')

    if request.method == 'POST':
        student = get_object_or_404(Student, id=student_id)
        user = student.user
        student_name = f"{user.first_name} {user.last_name}"
        user.delete()
        messages.success(request, f"Student {student_name} and all associated data deleted successfully.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect('admin_dashboard')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us! Your inquiry has been submitted and our support desk will contact you soon.")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            initial_data['email'] = request.user.email
            if hasattr(request.user, 'student_profile'):
                initial_data['phone'] = request.user.student_profile.phone
            elif hasattr(request.user, 'admin_profile'):
                initial_data['phone'] = request.user.admin_profile.phone
        form = ContactForm(initial=initial_data)

    return render(request, 'contact.html', {'form': form})


@login_required
def contact_messages_view(request):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('dashboard')

    status_filter = request.GET.get('status', 'all')
    if status_filter == 'pending':
        inquiries = ContactMessage.objects.filter(is_resolved=False).order_by('-created_at')
    elif status_filter == 'resolved':
        inquiries = ContactMessage.objects.filter(is_resolved=True).order_by('-created_at')
    else:
        inquiries = ContactMessage.objects.all().order_by('-created_at')

    # Calculate statistics for inquiry tabs
    stats = {
        'total': ContactMessage.objects.count(),
        'pending': ContactMessage.objects.filter(is_resolved=False).count(),
        'resolved': ContactMessage.objects.filter(is_resolved=True).count(),
    }

    return render(request, 'contact_messages.html', {
        'inquiries': inquiries,
        'status_filter': status_filter,
        'stats': stats,
    })


@login_required
def contact_message_toggle_resolved(request, msg_id):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('dashboard')

    inquiry = get_object_or_404(ContactMessage, id=msg_id)
    inquiry.is_resolved = not inquiry.is_resolved
    inquiry.save()

    status_text = "resolved" if inquiry.is_resolved else "pending"
    messages.success(request, f"Inquiry status updated to {status_text}.")
    return redirect('contact_messages')


@login_required
def contact_message_delete(request, msg_id):
    if not is_admin(request.user):
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('dashboard')

    if request.method == 'POST':
        inquiry = get_object_or_404(ContactMessage, id=msg_id)
        subject = inquiry.subject
        inquiry.delete()
        messages.success(request, f"Inquiry '{subject}' deleted successfully.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect('contact_messages')


def about_view(request):
    return render(request, 'about.html')




