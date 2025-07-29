from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Python MinHex",
        description="Minimal Hexagonal Architecture in Python",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(router)
    
    @app.get("/")
    async def root():
        return {"message": "Python MinHex - Minimal Hexagonal Architecture"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    return app