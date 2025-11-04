"""
Serive Layer - handles database operations for Contact
"""

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.contacts.models import Contact

class ContactService:

    async def create_contact(self, name:str,
                       phone_number:int,
                       email:str,
                       address:str,
                       session:AsyncSession):
        
        result = await session.execute(select(Contact).where(Contact.name == name))
        existing = result.scalar_one_or_none()
        
        if existing:
            return "Contact already exists."
        
        new_contact = Contact(
            name=name,
            phone_number=phone_number,
            email=email,
            address=address
        )

        session.add(new_contact)
        
        await session.commit()
        await session.refresh(new_contact)
        
        return new_contact
    

    async def update_contact(self, name:str,
                       phone_number:int,
                       email:str,
                       address:str,
                       session:AsyncSession):
        
        result = await session.execute(select(Contact).where(Contact.name == name))
        contact = result.scalar_one_or_none()

        if not contact:
            return "Contact not found."

        contact.phone_number = phone_number
        contact.email = email
        contact.address = address

        await session.commit()
        await session.refresh(contact)
        return contact


    async def delete_contact(self, 
                             name: str, 
                             session: AsyncSession):
        
        result = await session.execute(select(Contact).where(Contact.name == name))
        contact = result.scalar_one_or_none()

        if not contact:
            return "Contact not found."

        await session.delete(contact)
        await session.commit()
        return "Deleted successfully."
    

    async def search_contact(self, 
                             name: str, 
                             session: AsyncSession):
        
        result = await session.execute(select(Contact).where(Contact.name.ilike(f"%{name}%")))
        found = result.scalars().all()
        return found if found else "Contact not found."


    async def view_contact(self, session: AsyncSession):
        result = await session.execute(select(Contact))
        return result.scalars().all()

