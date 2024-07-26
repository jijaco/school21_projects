from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Spaceship(_message.Message):
    __slots__ = ("Alignment", "name", "length", "Class", "size", "armed_status", "officers")
    class AlignmentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ALLY: _ClassVar[Spaceship.AlignmentType]
        ENEMY: _ClassVar[Spaceship.AlignmentType]
    ALLY: Spaceship.AlignmentType
    ENEMY: Spaceship.AlignmentType
    class ClassType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CORVETTE: _ClassVar[Spaceship.ClassType]
        FRIGATE: _ClassVar[Spaceship.ClassType]
        CRUISER: _ClassVar[Spaceship.ClassType]
        DESTROYER: _ClassVar[Spaceship.ClassType]
        CARRIER: _ClassVar[Spaceship.ClassType]
        DREADNOUGHT: _ClassVar[Spaceship.ClassType]
    CORVETTE: Spaceship.ClassType
    FRIGATE: Spaceship.ClassType
    CRUISER: Spaceship.ClassType
    DESTROYER: Spaceship.ClassType
    CARRIER: Spaceship.ClassType
    DREADNOUGHT: Spaceship.ClassType
    class Officer(_message.Message):
        __slots__ = ("first_name", "last_name", "rank")
        FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
        LAST_NAME_FIELD_NUMBER: _ClassVar[int]
        RANK_FIELD_NUMBER: _ClassVar[int]
        first_name: str
        last_name: str
        rank: str
        def __init__(self, first_name: _Optional[str] = ..., last_name: _Optional[str] = ..., rank: _Optional[str] = ...) -> None: ...
    ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    CLASS_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    ARMED_STATUS_FIELD_NUMBER: _ClassVar[int]
    OFFICERS_FIELD_NUMBER: _ClassVar[int]
    Alignment: Spaceship.AlignmentType
    name: str
    length: float
    Class: Spaceship.ClassType
    size: int
    armed_status: bool
    officers: _containers.RepeatedCompositeFieldContainer[Spaceship.Officer]
    def __init__(self, Alignment: _Optional[_Union[Spaceship.AlignmentType, str]] = ..., name: _Optional[str] = ..., length: _Optional[float] = ..., Class: _Optional[_Union[Spaceship.ClassType, str]] = ..., size: _Optional[int] = ..., armed_status: bool = ..., officers: _Optional[_Iterable[_Union[Spaceship.Officer, _Mapping]]] = ...) -> None: ...

class Coordinate(_message.Message):
    __slots__ = ("right_ascension_hours", "right_ascension_minutes", "right_ascension_seconds", "declination_degrees", "declination_minutes", "declination_seconds")
    RIGHT_ASCENSION_HOURS_FIELD_NUMBER: _ClassVar[int]
    RIGHT_ASCENSION_MINUTES_FIELD_NUMBER: _ClassVar[int]
    RIGHT_ASCENSION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    DECLINATION_DEGREES_FIELD_NUMBER: _ClassVar[int]
    DECLINATION_MINUTES_FIELD_NUMBER: _ClassVar[int]
    DECLINATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    right_ascension_hours: float
    right_ascension_minutes: float
    right_ascension_seconds: float
    declination_degrees: float
    declination_minutes: float
    declination_seconds: float
    def __init__(self, right_ascension_hours: _Optional[float] = ..., right_ascension_minutes: _Optional[float] = ..., right_ascension_seconds: _Optional[float] = ..., declination_degrees: _Optional[float] = ..., declination_minutes: _Optional[float] = ..., declination_seconds: _Optional[float] = ...) -> None: ...

class RequestedSpaceship(_message.Message):
    __slots__ = ("coordinate", "spaceship")
    COORDINATE_FIELD_NUMBER: _ClassVar[int]
    SPACESHIP_FIELD_NUMBER: _ClassVar[int]
    coordinate: Coordinate
    spaceship: _containers.RepeatedCompositeFieldContainer[Spaceship]
    def __init__(self, coordinate: _Optional[_Union[Coordinate, _Mapping]] = ..., spaceship: _Optional[_Iterable[_Union[Spaceship, _Mapping]]] = ...) -> None: ...

class Spaceships(_message.Message):
    __slots__ = ("spaceship",)
    SPACESHIP_FIELD_NUMBER: _ClassVar[int]
    spaceship: _containers.RepeatedCompositeFieldContainer[Spaceship]
    def __init__(self, spaceship: _Optional[_Iterable[_Union[Spaceship, _Mapping]]] = ...) -> None: ...

class SpaceshipLocationDatabase(_message.Message):
    __slots__ = ("requestedspaceship",)
    REQUESTEDSPACESHIP_FIELD_NUMBER: _ClassVar[int]
    requestedspaceship: _containers.RepeatedCompositeFieldContainer[RequestedSpaceship]
    def __init__(self, requestedspaceship: _Optional[_Iterable[_Union[RequestedSpaceship, _Mapping]]] = ...) -> None: ...

class StringSpaceshipsRepresentation(_message.Message):
    __slots__ = ("spaceships",)
    SPACESHIPS_FIELD_NUMBER: _ClassVar[int]
    spaceships: str
    def __init__(self, spaceships: _Optional[str] = ...) -> None: ...
