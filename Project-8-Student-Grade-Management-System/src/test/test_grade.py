import pytest


@pytest.mark.asyncio
async def test_add_subject_marks(client):
    # Admin login
    login = await client.post(
        "/auth/login",
        json={
            "email": "admin@example.com",
            "password": "admin123",
        },
    )

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get students
    students = await client.get("/students", headers=headers)
    student_uid = students.json()[0]["uid"]

    response = await client.post(
        f"/grade/{student_uid}/subject",
        json={
            "subject_name": "Maths",
            "marks_obtain": 90,
            "max_marks": 100,
            "teacher_name": "Mr. Singh",
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["subject_name"] == "Maths"
