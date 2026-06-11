from django.contrib import admin

from .models import Course, Student, Application, Documents, AdminProfile, ApprovalDecisionHistory, ContactMessage




@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active", "created_at")
    search_fields = ("code", "name")
    list_filter = ("is_active",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "city", "created_at")
    search_fields = ("user__username", "user__first_name", "user__last_name")


class DocumentsInline(admin.TabularInline):
    model = Documents
    extra = 0
    readonly_fields = ("uploaded_at",)


class ApprovalDecisionHistoryInline(admin.TabularInline):
    model = ApprovalDecisionHistory
    extra = 0
    readonly_fields = ("created_at", "decided_by", "from_status", "to_status", "remarks")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("application_number", "student", "course", "status", "submission_date", "updated_at")
    list_filter = ("status", "course")
    search_fields = ("application_number", "student__user__username", "student__user__first_name", "student__user__last_name")
    inlines = [DocumentsInline, ApprovalDecisionHistoryInline]


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "application", "document_type", "uploaded_at")
    list_filter = ("document_type",)
    search_fields = ("student__user__username", "application__application_number")


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone", "created_at")
    list_filter = ("role",)
    search_fields = ("user__username",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_resolved")
    list_filter = ("is_resolved", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)


