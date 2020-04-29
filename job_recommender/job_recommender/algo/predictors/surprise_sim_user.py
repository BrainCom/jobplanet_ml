import os
import pandas as pd
from surprise import dump
from .surprise_sim_base import SurpriseSimBase

class SurpriseSimUser(SurpriseSimBase):

	def predict(
	    self,
	    id: str,
	    k: int):

	        result = self.model.get_neighbors(id, k=k)

	        return result