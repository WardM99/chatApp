"""Router groups"""
from fastapi import APIRouter
group_router = APIRouter(prefix="/groups")

@group_router.post("")
async def make_group():
    """Make a group"""
    print("HALLO")
