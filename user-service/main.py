from fastapi import FastAPI, APIRouter

app = FastAPI(title="User service")
api_router = APIRouter()


@api_router.get('/')
def root() -> str:
    return 'Root'


app.include_router(api_router)
