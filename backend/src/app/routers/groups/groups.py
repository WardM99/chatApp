"""Router groups"""
from fastapi import APIRouter, Depends
group_router = APIRouter(prefix="/groups")

@group_router.post("")
async def make_group():
    print("HALLO")