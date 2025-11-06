class Grade:
    def __init__(self):
        self.record = []  # list of dicts

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

        return {"average": round(average, 2), "grade": grade}

    def create(self, name: str, total_marks: int, total_sub: int):
        # avoid duplicates by name (case-insensitive)
        if any(s["name"].lower() == name.lower() for s in self.record):
            return {"error": "Student already exists."}

        grades = self._compute_grade(total_marks, total_sub)
        rec = {
            "name": name,
            "total_marks": total_marks,
            "total_sub": total_sub,
            **grades
        }
        self.record.append(rec)
        return rec

    def update(self, name: str, total_marks: int | None = None, total_sub: int | None = None):
        for student in self.record:
            if student["name"].lower() == name.lower():
                # update only provided fields
                if total_marks is not None:
                    if total_marks < 0:
                        return {"error": "total_marks must be >= 0"}
                    student["total_marks"] = total_marks
                if total_sub is not None:
                    if total_sub <= 0:
                        return {"error": "total_sub must be > 0"}
                    student["total_sub"] = total_sub

                # recompute grade using current values
                student.update(self._compute_grade(student["total_marks"], student["total_sub"]))
                return student

        return {"error": "Student not found."}

    def delete(self, name: str):
        for student in self.record:
            if student["name"].lower() == name.lower():
                self.record.remove(student)
                return {"message": "Deleted successfully."}
        return {"error": "Student not found."}

    def search(self, name: str):
        for student in self.record:
            if student["name"].lower() == name.lower():
                return student
        return {"error": "Student not found."}

    def view(self):
        # if not self.record:
        #     return []
        return list(self.record)  # return a copy to avoid external modification


# Example usage
# if __name__ == "__main__":
#     g = Grade()
#     print(g.create("Saurabh", 450, 5))
#     print(g.create("Ravi", 300, 5))
#     print(g.update("Ravi", total_marks=380, total_sub=5))
#     print(g.search("Saurabh"))
#     print(g.delete("Ravi"))
#     print(g.view())
