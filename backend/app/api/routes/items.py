from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()

# In-memory storage for demo purposes
items_db = {}
item_counter = 0


@router.get("/", response_model=List[Item])
async def get_items(skip: int = 0, limit: int = 10):
    """Get all items with pagination"""
    items_list = list(items_db.values())
    return items_list[skip : skip + limit]


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return items_db[item_id]


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """Create a new item"""
    global item_counter
    item_counter += 1
    new_item = Item(id=item_counter, **item.dict())
    items_db[item_counter] = new_item
    return new_item


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    """Update an existing item"""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    stored_item = items_db[item_id]
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item.copy(update=update_data)
    items_db[item_id] = updated_item
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """Delete an item"""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    del items_db[item_id]
    return None
