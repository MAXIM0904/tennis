from fastapi import APIRouter
from sqlalchemy.orm import Session
from . import schema
from fastapi import Depends
from sql_app.db import get_db
from .models import Countries, Cities, District
from profile import utils
from profile import authentication


geo = APIRouter()


@geo.get("/")
async def get_city(current_user: dict = Depends(authentication.get_current_user), db: Session = Depends(get_db)):
    """ Получить список стран с городами и районами """
    list_answer = []
    all_country = db.query(Countries).all()

    for i_all_country in all_country:
        country = schema.SchemaCountry(**i_all_country.__dict__).dict()
        cities = db.query(Cities).filter(Cities.country_id == country['id']).all()
        schema_cities = schema.SchemaCity(requests=cities).dict()

        for i_schema_cities in schema_cities['requests']:
            district = db.query(District).filter(District.cityid == i_schema_cities['id']).all()
            schema_district = schema.SchemaListDistrict(requests=district).dict()
            i_schema_cities['district'] = schema_district['requests']

        country['city'] = schema_cities['requests']
        list_answer.append(country)

    return utils.answer_user_data(True, "", list_answer)