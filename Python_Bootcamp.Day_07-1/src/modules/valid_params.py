from pydantic import BaseModel, Field
from typing_extensions import Annotated


class BiologicalParametres(BaseModel):
    """
    Restrain from adding unnormal biological params

    :param respiration: Amount of breathes in and osygen per minute.
    :type respiration: int
    :param heart_rate: Number of contractions of the heart per minute.
    :type paramheart_rate: int
    :param blushing_level: Degree of reddening of a person's face. 
    :type blushing_level: int
    :param pupillary_dilation: Current pupil size.
    :type pupillary_dilation: int
    """
    respiration: Annotated[int, Field(ge=10, le=18)]
    heart_rate: Annotated[int, Field(ge=50, le=120)]
    blushing_level: Annotated[int, Field(ge=0, le=5)]
    pupillary_dilation: Annotated[int, Field(ge=2, le=8)]
