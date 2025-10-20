from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()

# In-memory storage for demo purposes
users_db = {}
user_counter = 0


@router.get("/", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 10):
    """Get all users with pagination"""
    users_list = list(users_db.values())
    return users_list[skip : skip + limit]


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a specific user by ID"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return users_db[user_id]


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user"""
    global user_counter
    user_counter += 1
    new_user = User(id=user_counter, **user.dict())
    users_db[user_counter] = new_user
    return new_user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    """Update an existing user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    stored_user = users_db[user_id]
    update_data = user.dict(exclude_unset=True)
    updated_user = stored_user.copy(update=update_data)
    users_db[user_id] = updated_user
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """Delete a user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    del users_db[user_id]
    return None
