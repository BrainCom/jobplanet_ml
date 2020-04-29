import os
import pandas as pd
from surprise import dump
from .base import Base
 
class SurpriseBase(Base):

    def _load_model(self):
        model, predictions = self._find_model()
        self.model = model
        self.predictions = predictions

    def _find_model(self):
        predictions, model = dump.load(self.model_path)

        return model, predictions