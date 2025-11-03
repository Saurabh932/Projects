from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.app import Contactbook

router = APIRouter()
contact = Contactbook()

templates = Jinja2Templates(directory="app/templates/")

@router.get("/", response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("index.html", {"request":request, "contact_data":contact.view_contact()})\
        

@router.post("/add_contact", response_class=HTMLResponse)
def add_contact(request : Request,
                name : str = Form(...),
                phone_number : int = Form(...),
                email : str = Form(...),
                address : str = Form(...)):
    
    contact.create_contact(name, phone_number, email, address)
    return templates.TemplateResponse("index.html", {"request":request, "contact_data":contact.view_contact()})


@router.post("/search_contact", response_class=HTMLResponse)
def search_contacts(request : Request,
                    name : str = Form(...)):
    
    result = contact.search_contact(name)
    return templates.TemplateResponse("index.html", {"request": request, "search_result": result, "contact_data": contact.view_contact()})


@router.post("/update_contact", response_class=HTMLResponse)
def update_contacts(request:Request,
                    name : str = Form(...),
                    phone_number : int = Form(...),
                    email : str = Form(...),
                    address : str = Form(...)):
    
    contact.update_contact(name, phone_number, email, address)
    return templates.TemplateResponse("index.html", {"request":request, "contact_data":contact.view_contact()})


@router.post("/delete_contact", response_class=HTMLResponse)
def delete_contacts(request:Request,
                    name : str = Form(...)):
    
    contact.delete_contact(name)
    return templates.TemplateResponse("index.html", {"request":request, "contact_data":contact.view_contact()})