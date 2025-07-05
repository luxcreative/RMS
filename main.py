from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from rms import models, schemas, database, auth
from rms.auth import get_current_user, get_db, create_access_token, authenticate_user, get_password_hash

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Rental Management System")

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/users", response_model=schemas.ClientRead)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = models.User(username=user_in.username, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# InventoryItem CRUD
@app.post("/inventory", response_model=schemas.InventoryItemRead)
def create_item(item: schemas.InventoryItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_item = models.InventoryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/inventory", response_model=List[schemas.InventoryItemRead])
def list_items(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.InventoryItem).all()

@app.get("/inventory/{item_id}", response_model=schemas.InventoryItemRead)
def get_item(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.InventoryItem).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/inventory/{item_id}", response_model=schemas.InventoryItemRead)
def update_item(item_id: int, item: schemas.InventoryItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_item = db.query(models.InventoryItem).get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    for k, v in item.dict().items():
        setattr(db_item, k, v)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/inventory/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_item = db.query(models.InventoryItem).get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"ok": True}

# Client CRUD
@app.post("/clients", response_model=schemas.ClientRead)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients", response_model=List[schemas.ClientRead])
def list_clients(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Client).all()

@app.get("/clients/{client_id}", response_model=schemas.ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    client = db.query(models.Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@app.put("/clients/{client_id}", response_model=schemas.ClientRead)
def update_client(client_id: int, client: schemas.ClientCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_client = db.query(models.Client).get(client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    for k, v in client.dict().items():
        setattr(db_client, k, v)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.delete("/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    client = db.query(models.Client).get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"ok": True}

# Job CRUD
@app.post("/jobs", response_model=schemas.JobRead)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs", response_model=List[schemas.JobRead])
def list_jobs(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Job).all()

@app.get("/jobs/{job_id}", response_model=schemas.JobRead)
def get_job(job_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    job = db.query(models.Job).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.put("/jobs/{job_id}", response_model=schemas.JobRead)
def update_job(job_id: int, job: schemas.JobCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_job = db.query(models.Job).get(job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    for k, v in job.dict().items():
        setattr(db_job, k, v)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_job = db.query(models.Job).get(job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(db_job)
    db.commit()
    return {"ok": True}

# Quote CRUD
@app.post("/quotes", response_model=schemas.QuoteRead)
def create_quote(quote: schemas.QuoteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_quote = models.Quote(**quote.dict())
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote

@app.get("/quotes", response_model=List[schemas.QuoteRead])
def list_quotes(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Quote).all()

@app.get("/quotes/{quote_id}", response_model=schemas.QuoteRead)
def get_quote(quote_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    quote = db.query(models.Quote).get(quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote

@app.put("/quotes/{quote_id}", response_model=schemas.QuoteRead)
def update_quote(quote_id: int, quote: schemas.QuoteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_quote = db.query(models.Quote).get(quote_id)
    if not db_quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    for k, v in quote.dict().items():
        setattr(db_quote, k, v)
    db.commit()
    db.refresh(db_quote)
    return db_quote

@app.delete("/quotes/{quote_id}")
def delete_quote(quote_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_quote = db.query(models.Quote).get(quote_id)
    if not db_quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    db.delete(db_quote)
    db.commit()
    return {"ok": True}

# QuoteItem CRUD
@app.post("/quote-items", response_model=schemas.QuoteItemRead)
def create_quote_item(item: schemas.QuoteItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_item = models.QuoteItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/quote-items", response_model=List[schemas.QuoteItemRead])
def list_quote_items(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.QuoteItem).all()

@app.get("/quote-items/{item_id}", response_model=schemas.QuoteItemRead)
def get_quote_item(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.QuoteItem).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Quote item not found")
    return item

@app.put("/quote-items/{item_id}", response_model=schemas.QuoteItemRead)
def update_quote_item(item_id: int, item: schemas.QuoteItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_item = db.query(models.QuoteItem).get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Quote item not found")
    for k, v in item.dict().items():
        setattr(db_item, k, v)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/quote-items/{item_id}")
def delete_quote_item(item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_item = db.query(models.QuoteItem).get(item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Quote item not found")
    db.delete(db_item)
    db.commit()
    return {"ok": True}

# AI suggestion endpoint
@app.post("/ai/suggest-gear")
def suggest_gear(job: schemas.JobCreate, current_user: models.User = Depends(get_current_user)):
    # Placeholder for AI integration
    return {"recommended_items": [], "message": f"AI suggestions for {job.name} will appear here."}
