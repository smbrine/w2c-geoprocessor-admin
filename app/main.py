import uuid
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqladmin import Admin, ModelView

from app.db import SessionLocal, engine

# from admin import db as models
from app import settings
from db import models
from geoutils import CoordinatesProcessor

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)


admin = Admin(app, engine)


class CompanyAdmin(ModelView, model=models.Company):
    name_plural = "Companies"
    column_list = [
        key
        for key in models.Company.__dict__.keys()
        if not any(
            [
                key.startswith("_"),
                key in ["id", "created_at", "logo"],
            ]
        )
    ]
    form_excluded_columns = [
        models.Company.id,
        models.Company.created_at,
    ]

    async def on_model_change(self, data, model, is_created, request):
        if is_created:
            data["id"] = str(uuid.uuid4())
            data["created_at"] = datetime.now()


class CafeAdmin(ModelView, model=models.Cafe):
    name_plural = "Cafes"
    column_list = [
        key
        for key in models.Cafe.__dict__.keys()
        if not any(
            [
                key.startswith("_"),
                key.endswith("id"),
                key in ["created_at"],
            ]
        )
    ]
    form_excluded_columns = [
        models.Cafe.id,
        models.Cafe.created_at,
    ]

    async def on_model_change(self, data, model, is_created, request):
        if is_created:
            data["id"] = str(uuid.uuid4())
            data["created_at"] = datetime.now()


class GeodataAdmin(ModelView, model=models.Geodata):
    name_plural = "Geodata"
    column_list = [
        key
        for key in models.Geodata.__dict__.keys()
        if not any(
            [
                key.startswith("_"),
                key
                in [
                    "id",
                    "created_at",
                    "latitude",
                    "longitude",
                    "get_all",
                ],
                key.endswith("_id"),
            ]
        )
    ]

    form_excluded_columns = [
        models.Geodata.id,
        models.Geodata.created_at,
        models.Geodata.latitude,
        models.Geodata.longitude,
    ]

    async def on_model_change(self, data, model, is_created, request):
        data["latitude"], data["longitude"] = (
            await CoordinatesProcessor.address_to_coordinates(
                data["address"]
            )
        )
        print(data["latitude"], data["longitude"])
        data["address"] = (
            await CoordinatesProcessor.coordinates_to_address(
                data["latitude"],
                data["longitude"],
            )
        )
        print(data["address"])
        if is_created:
            data["id"] = str(uuid.uuid4())
            data["created_at"] = datetime.now()


class ReviewAdmin(ModelView, model=models.Review):
    name_plural = "Reviews"
    column_list = [
        key
        for key in models.Review.__dict__.keys()
        if not any(
            [
                key.startswith("_"),
                key.endswith("id"),
                key in ["created_at"],
            ]
        )
    ]

    form_excluded_columns = [
        models.Review.id,
        models.Review.created_at,
    ]

    async def on_model_change(self, data, model, is_created, request):
        if is_created:
            data["id"] = str(uuid.uuid4())
            data["created_at"] = datetime.now()


class MenuAdmin(ModelView, model=models.Menu):
    name_plural = "Menus"
    column_list = [
        key
        for key in models.Menu.__dict__.keys()
        if not any(
            [
                key.startswith("_"),
                key.endswith("id"),
                key in ["created_at"],
            ]
        )
    ]

    form_excluded_columns = [
        models.Menu.id,
        models.Menu.created_at,
    ]

    async def on_model_change(self, data, model, is_created, request):
        if is_created:
            data["id"] = str(uuid.uuid4())
            data["created_at"] = datetime.now()


class MenuEntryAdmin(ModelView, model=models.MenuEntry):
    name_plural = "Menus' entries"
    column_list = [
        key
        for key in models.MenuEntry.__dict__.keys()
        if not any(
            [
                key.startswith("_"),
                key.endswith("id"),
                key in ["created_at"],
            ]
        )
    ]

    form_excluded_columns = [
        models.MenuEntry.id,
        models.MenuEntry.created_at,
    ]

    async def on_model_change(self, data, model, is_created, request):
        if is_created:
            data["id"] = str(uuid.uuid4())
            data["created_at"] = datetime.now()


class CountryAdmin(ModelView, model=models.Country):
    name_plural = "Countries"
    column_list = [
        key
        for key in models.Country.__dict__.keys()
        if not any(
            [
                key.startswith("_"),
                key.endswith("id"),
                key in ["created_at", "geodata"],
            ]
        )
    ]
    form_include_pk = True

    async def on_model_change(self, data, model, is_created, request):
        if is_created:
            data["created_at"] = datetime.now()


class CityAdmin(ModelView, model=models.City):
    name_plural = "Cities"
    column_list = [
        key
        for key in models.City.__dict__.keys()
        if not any(
            [
                key.startswith("_"),
                key.endswith("id"),
                key in ["created_at", "geodata"],
            ]
        )
    ]
    form_include_pk = True
    form_excluded_columns = [models.City.country_id]

    async def on_model_change(self, data, model, is_created, request):
        if is_created:
            data["created_at"] = datetime.now()


class CurrencyAdmin(ModelView, model=models.Currency):
    name_plural = "Currencies"
    column_list = [
        key
        for key in models.Currency.__dict__.keys()
        if not any(
            [
                key.startswith("_"),
                key.endswith("id"),
                key in ["created_at", "entries"],
            ]
        )
    ]
    form_include_pk = True

    async def on_model_change(self, data, model, is_created, request):
        if is_created:
            data["created_at"] = datetime.now()


admin.add_view(CompanyAdmin)
admin.add_view(CafeAdmin)
admin.add_view(GeodataAdmin)
admin.add_view(ReviewAdmin)
admin.add_view(MenuAdmin)
admin.add_view(MenuEntryAdmin)
admin.add_view(CountryAdmin)
admin.add_view(CityAdmin)
admin.add_view(CurrencyAdmin)


@app.get("/healthz")
def healthz():
    return JSONResponse(status_code=200, content={"health": "ok"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "admin.main:app",
        host="0.0.0.0",
        port=9094,
        reload=settings.DEBUG,
        log_level="info",
        use_colors=True,
    )
