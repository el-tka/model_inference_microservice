""" The schema for apartment."""

from pydantic import BaseModel


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
    storage_yes - Storage existance
    """

    area: int
    constraction_year: int
    bedrooms: int
    garden: int
    balcony_yes: int
    parking_yes: int
    furnished_yes: int
    garage_yes: int
    storage_yes: int
