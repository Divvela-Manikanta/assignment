from dataclasses import dataclass


@dataclass
class DataToStore:
    deleteitem : str = None


@dataclass
class Student:
    name: str
    roll: str
    stranded : str 
