# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 16:13:15 2021

@author: 아빠
"""

from dataclasses import dataclass
from typing import List

@dataclass
class Sale:
    quantity: int

@dataclass
class Product:
    id: str
    name: str
    sales: List[Sale]
    
    