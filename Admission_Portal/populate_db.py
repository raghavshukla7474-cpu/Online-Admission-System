import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from django.contrib.auth.models import User
from admission.models import Course, AdminProfile
def populate():
    print("Populating initial data...")
    # Create Courses
    courses = [
        # Existing seed
        {
            "code": "CS101",
            "name": "B.Sc. Computer Science",
            "description": "Comprehensive program covering software engineering, algorithms, database management, artificial intelligence, and web technologies.",
            "duration_years": 3,
            "fees": 12500.00
        },
        {
            "code": "BA102",
            "name": "B.B.A. Business Administration",
            "description": "Gain insight into corporate management, operations research, marketing ethics, global supply chain, and entrepreneurial leadership.",
            "duration_years": 3,
            "fees": 11000.00
        },
        {
            "code": "ME103",
            "name": "B.Tech Mechanical Engineering",
            "description": "Rigorous engineering curriculum focusing on thermodynamics, machine design, aerodynamics, fluid dynamics, and modern robotics systems.",
            "duration_years": 4,
            "fees": 16000.00
        },
        {
            "code": "EE104",
            "name": "B.Tech Electrical Engineering",
            "description": "Advanced specialization course focusing on microcontrollers, signals, power transmission, embedded systems, and sustainable energy grids.",
            "duration_years": 4,
            "fees": 15500.00
        },

        # Required courses (missing in previous seed)
        {
            "code": "BC105",
            "name": "BCA (Bachelor of Computer Applications)",
            "description": "Foundation in programming, data structures, databases, software engineering fundamentals, and practical application development.",
            "duration_years": 3,
            "fees": 13000.00
        },
        {
            "code": "MC201",
            "name": "MCA (Master of Computer Applications)",
            "description": "Advanced software development, system design, computer networks, databases, and emerging technologies with project-based learning.",
            "duration_years": 2,
            "fees": 16000.00
        },
        {
            "code": "MB301",
            "name": "MBA (Master of Business Administration)",
            "description": "Leadership and management training with specialization tracks across finance, marketing, operations, HR, and strategy.",
            "duration_years": 2,
            "fees": 19000.00
        },
        {
            "code": "MT402",
            "name": "M.Tech (MTEK) (Master of Technology)",
            "description": "Advanced engineering coursework with specialization options, research-oriented projects, and deep technical skill development.",
            "duration_years": 2,
            "fees": 22000.00
        },
        {
            "code": "BCO205",
            "name": "B.Com (Bachelor of Commerce)",
            "description": "Commerce education focusing on accounting, taxation, economics, business law, auditing, and practical financial literacy.",
            "duration_years": 3,
            "fees": 12000.00
        },
        {
            "code": "BB401",
            "name": "BBA (Bachelor of Business Administration)",
            "description": "Business fundamentals covering management principles, marketing, organizational behavior, entrepreneurship, and analytics.",
            "duration_years": 3,
            "fees": 12500.00
        },
        {
            "code": "BT501",
            "name": "B.Tech (General) (BTECH)",
            "description": "Engineering program with core subjects in mathematics, physics, programming, and engineering fundamentals with elective specialization.",
            "duration_years": 4,
            "fees": 17500.00
        }
    ]

    for c in courses:
        course, created = Course.objects.get_or_create(
            code=c["code"],
            defaults={
                "name": c["name"],
                "description": c["description"],
                "duration_years": c["duration_years"],
                "fees": c["fees"],
                "is_active": True
            }
        )

        # Always set/update required fields
        course.name = c["name"]
        course.description = c["description"]
        course.duration_years = c["duration_years"]
        course.fees = c["fees"]
        course.is_active = True

        if created:
            print(f"Created Course: {course.name}")
        else:
            print(f"Updated Course: {course.name}")
        course.save()


    # Create Superuser/Admin

    if not User.objects.filter(username="admin").exists():
        admin_user = User.objects.create_superuser("admin", "admin@apex.edu", "admin123")
        admin_user.first_name = "System"
        admin_user.last_name = "Administrator"
        admin_user.save()
        
        # Create Admin Profile
        AdminProfile.objects.create(
            user=admin_user,
            phone="1234567890",
            role="SuperAdmin"
        )
        print("Created Superuser account (username: 'admin', password: 'admin123') and AdminProfile.")
    else:
        print("Superuser account 'admin' already exists.")
    print("Initial population successfully completed!")
if __name__ == "__main__":
    populate()
