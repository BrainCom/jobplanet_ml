import os
import pandas as pd
from surprise import dump
from .surprise_base import SurpriseBase
 
class SurpriseSimBase(SurpriseBase):

    def predict(
        self,
        id: str,
        k: int):

            result = self.model.get_neighbors(id, k=k)

            return result