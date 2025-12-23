# Student Grade Management System

## 🚀 Overview
The **Student Grade Management System** is a role-based academic management backend built using FastAPI.  
It supports **Admin** and **Student** workflows, enabling secure grade management, subject-wise evaluation, and real-time academic insights.

Admins can manage students, approve accounts, and assign subject marks, while students can securely view their own grades, averages, and subject performance.

This project is designed with **production practices** in mind, including authentication, authorization, async database access, realistic data seeding, and cloud deployment readiness.

---

## 🛠 Tech Stack
- **Backend Framework:** FastAPI (Async)
- **Database:** MySQL (SQLModel + Async SQLAlchemy)
- **Authentication:** JWT (Access Tokens)
- **Authorization:** Role-Based Access Control (RBAC)
- **Containerization:** Docker
- **Cloud Deployment:** AWS EC2
- **ORM:** SQLModel
- **Language:** Python 3.10+

---

## 🔑 Key Features
- **JWT Authentication:** Secure login using access tokens.
- **Role-Based Access Control (RBAC):**
  - Admin: Full access to students, subjects, and approvals.
  - Student: Access only to their own academic data.
- **Student Isolation:** Students can only view their own grades using `/grade/me`.
- **Admin Workflows:**
  - Student approval
  - Add / update / delete subject marks
  - View any student’s academic profile
- **Automated Grade Calculation:** Grades and averages computed dynamically based on subject marks.
- **Async Backend:** Non-blocking database operations using async SQLAlchemy.
- **Realistic Seed Data:** Script to populate student accounts, subjects, and marks for demos.

---

## 🗂 Database Design
- **User**
  - Authentication and role management
- **Student**
  - One-to-one mapping with User
- **SubjectMarks**
  - One-to-many mapping with Student

Relationships are enforced using foreign keys and ORM-level constraints.

---

## 🏗 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/student-grade-management-system.git
cd student-grade-management-system
`