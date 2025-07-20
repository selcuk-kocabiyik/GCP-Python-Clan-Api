from fastapi import FastAPI
from controller.clan_controller import router as clan_router

app = FastAPI()

# Tüm router'ları ekliyoruz
app.include_router(clan_router)
