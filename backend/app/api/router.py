from fastapi import APIRouter

from app.api.routes import health, jobs, resumes


api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(jobs.router, tags=["jobs"])
api_router.include_router(resumes.router, tags=["resumes"])
