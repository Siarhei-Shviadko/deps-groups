from pydantic import BaseModel

__all__ = ["ConfiguredResponseSerializer", "ConfiguredRequestSerializer"]


class ConfiguredRequestSerializer(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        smart_union = True
        anystr_strip_whitespace = True
        use_enum_values = True


class ConfiguredResponseSerializer(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        smart_union = True
        use_enum_values = True
