from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID
import logging

from src.db.db import get_session
from src.db.models import Student, SubjectMarks
from src.auth.dependencies import get_current_user
from src.ai.service import AIService
from src.ai.schema import AISummaryResponse

ai_router = APIRouter(prefix="/ai", tags=["ai"])
ai_service = AIService()

logger = logging.getLogger(__name__)


@ai_router.get(
    "/student-summary/{student_uid}",
    response_model=AISummaryResponse
)
async def generate_student_summary(
    student_uid: UUID,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
):
    try:
        # Authorization
        if current_user.role != "admin":
            if (
                not current_user.student_profile
                or current_user.student_profile.uid != student_uid
            ):
                raise HTTPException(status_code=403, detail="Unauthorized")

        # Fetch student
        result = await session.execute(
            select(Student).where(Student.uid == student_uid)
        )
        student = result.scalar_one_or_none()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Fetch subjects
        result = await session.execute(
            select(SubjectMarks).where(SubjectMarks.student_uid == student.uid)
        )
        subjects = result.scalars().all()

        subject_lines = [
            f"- {s.subject_name}: {s.marks_obtain}/{s.max_marks}"
            for s in subjects
        ]

        summary = await ai_service.generate_student_summary({
            "name": student.name,
            "average": student.average,
            "grade": student.grade,
            "subjects": "\n".join(subject_lines),
        })

        return {"summary": summary}

    except Exception as e:
        logger.exception("AI summary generation failed")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
