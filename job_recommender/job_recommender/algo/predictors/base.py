import re

class Base(object):

  def __init__(self, model_path: str):
    self.model_path = model_path
    self._load_model()

  def _load_model(self):
    pass

  def _find_model(self):
    pass

  def predict(
    self,
    id: int,
    k: int):
    pass