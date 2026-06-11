# Google Stitch Prompt: EduPortal University Admissions

Copy and paste the prompt below into **Google Stitch** to generate a modern, premium user interface designed specifically for this Django admissions application.

---

```text
Create a high-fidelity, interactive, and responsive web application called "EduPortal" — a modern University Admissions & Application Tracking System. 

Use a premium SaaS-style aesthetic with rich visuals, clean layouts, and smooth micro-animations.

### Design System & Theme:
- **Theme**: Light/Dark mode compatible. The default should feel sleek, airy, and professional.
- **Typography**: Modern Sans-Serif font (Inter or Outfit) for optimal readability and a tech-forward look.
- **Color Palette**:
  - Primary Background: Clean off-whites (#f8fafc) and soft grays (#f1f5f9).
  - Primary Brand/Actions: Royal Indigo (#6366f1) and Deep Violet (#4f46e5).
  - Dark Slate/Midnight (#0f172a) for text and header backgrounds to project credibility.
  - Success/Approved Status: Emerald Green (#10b981 / #d1fae5).
  - Warning/Pending Status: Amber Gold (#f59e0b / #fef3c7).
  - Danger/Rejected Status: Rose Red (#f43f5e / #ffe4e6).
- **Layout Style**: Use card layouts, subtle box-shadows, and glassmorphism (translucent backdrops) for overlay modules.

### Pages & Layouts to Generate:

1. **LANDING PAGE (Index)**
   - **Hero Section**: Catchy title ("Your Journey to Excellence Begins Here"), supporting copy, and prominent "Apply Now" and "Check Status" call-to-action buttons.
   - **Quick Stats Panel**: Three elegant counters (e.g., "50+ Courses", "10,000+ Active Students", "48hr Average Processing Time").
   - **Course Highlights Grid**: Cards showcasing featured courses with names, duration, fees, and a quick "Register to Apply" button.

2. **STUDENT REGISTRATION & LOGIN**
   - **Split Screen Design**: Left side with a motivational university campus graphic or premium abstract art, right side with the form.
   - **Forms**: Clean input fields with floating labels. 
     - *Registration Fields*: First Name, Last Name, Email, Password, Phone, DOB, Gender (Dropdown/Pills), Address, City, State, and Pincode.
     - *Login Fields*: Username/Email and Password, with a "Forgot Password?" link and "Remember me" checkbox.

3. **STUDENT DASHBOARD & STEPPER**
   - **Overview Dashboard**: Left sidebar for navigation (Dashboard, Apply, Document Upload, Status, Profile). Main panel showing a greeting card and a summary of active applications.
   - **Interactive Stepper / Timeline**: Visual progress tracker for applications showing current state (Submitted -> Under Review -> Decision Pending -> Final Verdict).
   - **Quick Action Cards**: Two large call-to-action cards: "Apply for a New Course" and "Upload Required Documents".

4. **COURSE APPLICATION FORM (Apply)**
   - **Course Selection Grid**: Dynamic card selector displaying course codes, names, duration (years), fees, and description. Clicking a card selects it with a highlighted border.
   - **Submission Confirmation**: A clean review step where the student confirms their personal details before clicking "Submit Application".

5. **DOCUMENT UPLOAD PORTAL**
   - **File Dropzones**: Five dedicated upload zones with drag-and-drop support:
     1. Passport Photo (Image format)
     2. Signature Scan (Image/PDF format)
     3. 10th Grade Marksheet (PDF/Image)
     4. 12th Grade Marksheet (PDF/Image)
     5. Government Issued ID Proof (PDF/Image)
   - **State Feedback**: Show upload progress bars, green checkmarks for uploaded files, and action buttons to view or delete documents.

6. **REAL-TIME STATUS TRACKER**
   - **Timeline Logs**: An elegant vertical feed of the application's lifecycle showing decision history (e.g., "Application Received on June 2, 2026", "Status Updated from Pending to Under Review by Admissions Officer Raghav").
   - **Live Indicator**: A pulse animation indicating real-time status updates (WebSockets active).

7. **ADMIN PORTAL (Dashboard & Reviews)**
   - **Admin Layout**: Dark navigation sidebar. Main dashboard displaying:
     - *KPI Cards*: Total Applications, Pending Reviews, Approved, and Rejected counts.
     - *Filtering panel*: Inline search bar, course dropdown filter, and status filter (All, Pending, Approved, Rejected).
     - *Applications Table*: Rows showing Student Name, Course Code, Status Badge (colored pill), Submission Date, and a "Review" button. Includes pagination controls.
   - **Application Detail & Decision View (Double Pane)**:
     - *Left Pane*: Comprehensive student profile, address details, and interactive file previewers for the five uploaded documents.
     - *Right Pane*: Decision Card containing:
       - Transition options (Approve / Reject buttons with confirmation).
       - A multiline text area for adding "Remarks" or feedback.
       - A summary list showing previous transition logs and which admin made the decision.

8. **ADMIN REPORTS & ANALYTICS**
   - **Analytics Charts**: Modern dashboard charts including:
     - A bar chart showing application distribution across courses.
     - A pie chart showing application status percentage.
     - A line graph showing application submission volume trend over the last 30 days.
     - "Export CSV/PDF" buttons.
```
