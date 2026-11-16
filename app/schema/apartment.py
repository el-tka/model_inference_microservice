""" The schema for apartment."""

from datetime import date

from pydantic import BaseModel, Field


class Apartment(BaseModel):
    """
        Arartment schema.
    
        area - Apartment area
        constraction_year - Apartment construction year
        bedrooms = Number of bedrooms
        garden - Garden existance
        balcony_yes - Balcony existance
        parking_yes - Parking existance
        furnished_yes - Furniture existance
        garage_yes - Garage existance
        storage_yes - Storage existance
        """

    area: int = Field(gt=0)
    constraction_year: int = Field(ge=1800, le=2100)
    bedrooms: int = Field(ge=0)
    garden: int = Field(ge=0, le=1)
    balcony_yes: int = Field(ge=0, le=1)
    parking_yes: int = Field(ge=0, le=1)
    furnished_yes: int = Field(ge=0, le=1)
    garage_yes: int = Field(ge=0, le=1)
    storage_yes: int = Field(ge=0, le=1)

