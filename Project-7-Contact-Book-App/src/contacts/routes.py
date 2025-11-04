"""
This file defines all FastAPI routes for the Contact Book.
Each route corresponds to a CRUD operation (Create, Read, Update, Delete).
"""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.contacts.service import ContactService

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")
contact_service = ContactService()


# 🧠 VIEW ALL CONTACTS (Homepage)
@router.get("/", response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = Depends(get_session)):
    """
    Displays all contacts in the table on the home page.
    """
    contacts = await contact_service.view_contact(session)
    return templates.TemplateResponse("index.html", {"request": request, "contacts": contacts})


# ➕ ADD NEW CONTACT
@router.post("/add_contact", response_class=HTMLResponse)
async def add_contact(
    request: Request,
    name: str = Form(...),
    phone_number: int = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    """
    Adds a new contact to the database.
    """
    await contact_service.create_contact(name, phone_number, email, address, session)
    contacts = await contact_service.view_contact(session)
    success_message = f"✅ Contact '{name}' added successfully!"
    return templates.TemplateResponse("index.html", {"request": request, "contacts": contacts, "message": success_message})


# 🔍 SEARCH CONTACT
@router.post("/search_contact", response_class=HTMLResponse)
async def search_contacts(
    request: Request,
    name: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    """
    Searches for a contact by name (case-insensitive).
    """
    found = await contact_service.search_contact(name, session)
    all_contacts = await contact_service.view_contact(session)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "search_result": found, "contacts": all_contacts}
    )


# 📝 UPDATE CONTACT
@router.post("/update_contact", response_class=HTMLResponse)
async def update_contacts(
    request: Request,
    name: str = Form(...),
    phone_number: int = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    """
    Updates contact info if it exists.
    """
    await contact_service.update_contact(name, phone_number, email, address, session)
    contacts = await contact_service.view_contact(session)
    success_message = f"✏️ Contact '{name}' updated successfully!"
    return templates.TemplateResponse("index.html", {"request": request, "contacts": contacts, "message": success_message})


# ❌ DELETE CONTACT
@router.post("/delete_contact", response_class=HTMLResponse)
async def delete_contacts(
    request: Request,
    name: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    """
    Deletes a contact by name if it exists.
    """
    await contact_service.delete_contact(name, session)
    contacts = await contact_service.view_contact(session)
    success_message = f"🗑️ Contact '{name}' deleted successfully!"
    return templates.TemplateResponse("index.html", {"request": request, "contacts": contacts, "message": success_message})
