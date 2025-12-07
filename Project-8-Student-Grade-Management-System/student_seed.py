import uuid
import random
import asyncio
from typing import List

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import async_session_maker
from src.db.models import User, Student, SubjectMarks


# ===============================
# CONFIGURATION (Editable Section)
# ===============================
ADMIN_EMAIL = "mandhalkarsaurabh09@gmail.com"
STUDENT_PASSWORD = "test12"  # Only for reference in seeding output

NUM_STUDENTS = 15  # How many fake students to create

# Fake name datasets Realistic Indian names)
FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Riya", "Ishika",
    "Kunal", "Sneha", "Rahul", "Ananya", "Kabir",
    "Saanvi", "Neha", "Arjun", "Mira", "Dev"
]

LAST_NAMES = [
    "Sharma", "Patel", "Verma", "Rao", "Iyer",
    "Nair", "Joshi", "Gupta", "Khan", "Singh"
]

# Subjects that are assigned randomly to students
SUBJECTS = [
    "Mathematics", "Science", "English",
    "Computer Science", "History", "Geography"
]

# Random teachers for subject allocation
TEACHERS = [
    "Mr. Sharma", "Ms. Gupta", "Mrs. Iyer",
    "Mr. Nair", "Ms. Verma", "Mr. Singh"
]


# ===============================
# Compute Grade Helper
# ===============================
def compute_grade_from_percentage(percent: float) -> str:
    if percent >= 90:
        return "A"
    if percent >= 75:
        return "B"
    if percent >= 45:
        return "C"
    return "F"


# =================================================
# Generate random subject marks for each student 
# =================================================
def generate_marks_for_student() -> List[SubjectMarks]:
    num_subjects = random.randint(3, 5)  # Random 3–5 subjects per student
    chosen_subjects = random.sample(SUBJECTS, num_subjects)

    subjects: List[SubjectMarks] = []
    for subj in chosen_subjects:
        max_mark = 100
        score = random.randint(35, 100)  # Score between 35–100 → Pass/Fail realistic

        subjects.append(
            SubjectMarks(
                uid=uuid.uuid4(),
                subject_name=subj,
                marks_obtain=score,
                max_marks=max_mark,
                teacher_name=random.choice(TEACHERS),
            )
        )
    return subjects


# ===============================
# Main SEED LOGIC 
# ===============================
async def seed_students():
    async with async_session_maker() as session:  # DB session

        # Fetch admin user to reuse the password hash 
        result = await session.execute(select(User).where(User.email == ADMIN_EMAIL))
        admin = result.scalars().first()

        if not admin:
            raise RuntimeError(
                f"Admin user '{ADMIN_EMAIL}' not found. "
                f"Start your app once so it auto-creates the admin."
            )

        print(f"Admin found: {admin.email}")
        print("Using admin password hash for student accounts...")

        count = 0

        for i in range(NUM_STUDENTS):
            # Generate realistic full name
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            full_name = f"{first} {last}"

            email = f"{first.lower()}.{last.lower()}{i+1}@schoolmgmt.com"

            # Prevent duplication if script rerun
            existing = await session.execute(select(User).where(User.email == email))
            if existing.scalars().first():
                print(f"⚠ Already exists: {email}")
                continue

            # Create user (role: student)
            user = User(
                email=email,
                password_hash=admin.password_hash,  # same password for demo
                role="student",
                first_name=first,
                last_name=last,
                is_verified=True
            )
            session.add(user)
            await session.flush()

            # Create linked student profile 👨‍🎓
            student = Student(
                uid=uuid.uuid4(),
                name=full_name,
                user_uid=user.uid,
            )
            session.add(student)
            await session.flush()

            # Assign random subjects & calculate grade
            subjects = generate_marks_for_student()
            total_score = sum(sm.marks_obtain for sm in subjects)
            total_max = sum(sm.max_marks for sm in subjects)

            for sm in subjects:
                sm.student_uid = student.uid
                session.add(sm)

            percent = total_score / total_max * 100
            student.average = round(percent, 2)
            student.grade = compute_grade_from_percentage(percent)

            print(f"🎓 {full_name} → Grade {student.grade} | Avg {student.average}%")

            count += 1

        # Commit all changes once!
        await session.commit()
        print("\n SEEDING COMPLETE ")
        print(f" Students Created: {count}")
        print(f" Default Password (all students): {STUDENT_PASSWORD}")


# ===============================
# Execute when run directly
# ===============================
if __name__ == "__main__":
    asyncio.run(seed_students())
