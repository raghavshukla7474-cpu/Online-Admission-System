from django.contrib.auth.models import User
from django.db import models
import datetime


class Course(models.Model):
    # model fixes for app_label
    code = models.CharField(max_length=20, unique=True)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration_years = models.IntegerField(default=3)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Student(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Application(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    application_number = models.CharField(max_length=20, unique=True, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    remarks = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.application_number:
            year = datetime.date.today().year
            last_app = Application.objects.filter(application_number__startswith=f"APP-{year}-").order_by('-id').first()
            if last_app:
                last_num = int(last_app.application_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.application_number = f"APP-{year}-{new_num:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.application_number} - {self.student.user.username} ({self.status})"


class ApprovalDecisionHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='decision_history')
    from_status = models.CharField(max_length=20, choices=Application.STATUS_CHOICES, null=True, blank=True)
    to_status = models.CharField(max_length=20, choices=Application.STATUS_CHOICES)

    # Snapshot of the admin's remarks at decision time
    remarks = models.TextField(blank=True, null=True)

    decided_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='decisions_made')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.application.application_number}: {self.from_status} -> {self.to_status} ({self.created_at})"


class Documents(models.Model):
    DOCUMENT_TYPES = (
        ('Photo', 'Passport Photo'),
        ('Signature', 'Signature Scan'),
        ('Marksheet_10', '10th Grade Marksheet'),
        ('Marksheet_12', '12th Grade Marksheet'),
        ('ID_Proof', 'Government Issued ID Proof'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.document_type}"


class AdminProfile(models.Model):
    ROLE_CHOICES = (
        ('SuperAdmin', 'Super Admin'),
        ('AdmissionsOfficer', 'Admissions Officer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='AdmissionsOfficer')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"


