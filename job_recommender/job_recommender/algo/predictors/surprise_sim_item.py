import os
import pandas as pd
from surprise import dump
from .surprise_sim_base import SurpriseSimBase
 
class SurpriseSimItem(SurpriseSimBase):

    def predict(
        self,
        company_id: str,
        k: int):
    
            all_instances = self.model.trainset.all_items

            others = [(x, self.model.sim[company_id, x]) for x in all_instances() if x != company_id]
            others.sort(key=lambda tple: tple[1], reverse=True)
            result = [{'company_id': i, 'score': j} for (i, j) in others[:k]]

            return result