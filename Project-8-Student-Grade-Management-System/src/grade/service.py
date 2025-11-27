from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from .model import Student
from .schema import StudentCreateModel, StudentUpdateModel

class Grade:
    '''
        Computing Grades
    '''

    def _compute_grade(self, total_marks: int, total_sub: int):
        # validate inputs
        if total_sub <= 0:
            raise ValueError("total_sub must be > 0")
        if total_marks < 0:
            raise ValueError("total_marks must be >= 0")

        average = total_marks / total_sub  # float average

        # grade boundaries (inclusive, clear)
        if average >= 90:
            grade = "A"
        elif average >= 75:   # 75 <= avg < 90
            grade = "B"
        elif average >= 45:   # 45 <= avg < 75
            grade = "C"
        else:
            grade = "F"

        return round(average, 2), grade
    
    
    
    '''
        Creating new student and calcuating average and grades.
    '''
    async def create(self, student_data : StudentCreateModel, session : AsyncSession):
        
        # avoid duplicates by name (case-insensitive)
        query = select(Student).where(Student.name.ilike(student_data.name))
        result = await session.execute(query)
        exisitng = result.scalar_one_or_none()
        
        if exisitng:
            return {"error": "Student with this name already exists."}
        
        average, grade = self._compute_grade(student_data.total_marks, student_data.total_sub)
        
        student_dict = student_data.model_dump()
        
        student_dict['average'] = average
        student_dict['grade'] = grade
        
        new_student = Student(**student_dict)

        
        session.add(new_student)
        await session.commit()
        await session.refresh(new_student)
        return new_student
    
    
    
    """
        Fetching/Searching student by name
    """
    async def get_student_by_name(self, name : str, session : AsyncSession):
        query = select(Student).where(Student.name.ilike(name))
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    

    """
        Updating the existing student details
    """
    async def update(self, name: str, student_data: StudentUpdateModel, session: AsyncSession):

        try:
            student = await self.get_student_by_name(name, session)
            if not student:
                return {"error": "Student not found"}

            if student_data.name is not None:
                student.name = student_data.name

            if student_data.total_marks is not None:
                student.total_marks = student_data.total_marks

            if student_data.total_sub is not None:
                student.total_sub = student_data.total_sub

            average, grade = self._compute_grade(student.total_marks, student.total_sub)
            student.average = average
            student.grade = grade

            session.add(student)
            await session.commit()
            await session.refresh(student)
            return student

        except Exception as e:
            print("🔥 ERROR DURING UPDATE:", e)
            raise e



    
    """
        Deleting Student details
    """
    async def delete(self, name: str, session:AsyncSession):
        student = await self.get_student_by_name(name, session)
        
        if not student:
            return {"error":"Student not found"}
        
        await session.delete(student)
        await session.commit()
        return {"message": f"Student '{name}' deleted successfully."}


    """
        Viewing all details
    """
    async def view(self, session:AsyncSession):
        query = select(Student)
        result = await session.execute(query)
        return result.scalars().all()
