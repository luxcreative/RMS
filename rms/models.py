from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base

class ItemStatus(enum.Enum):
    available = "available"
    rented = "rented"
    maintenance = "maintenance"

class JobStatus(enum.Enum):
    planned = "planned"
    in_progress = "in_progress"
    completed = "completed"

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    status = Column(Enum(ItemStatus), default=ItemStatus.available)
    daily_rate = Column(Float, nullable=False)

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_name = Column(String)
    email = Column(String)
    phone = Column(String)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(JobStatus), default=JobStatus.planned)
    notes = Column(String)

    client = relationship('Client')

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, default=0)

    job = relationship('Job')

class QuoteItem(Base):
    __tablename__ = "quote_items"

    id = Column(Integer, primary_key=True, index=True)
    quote_id = Column(Integer, ForeignKey('quotes.id'), nullable=False)
    inventory_item_id = Column(Integer, ForeignKey('inventory_items.id'), nullable=False)
    quantity = Column(Integer, default=1)
    price_per_day = Column(Float, default=0)
    total_price = Column(Float, default=0)

    quote = relationship('Quote')
    inventory_item = relationship('InventoryItem')

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
