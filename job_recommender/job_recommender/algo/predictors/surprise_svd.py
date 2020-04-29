import os
import pandas as pd
from surprise import dump
from .surprise_base import SurpriseBase
 
class SurpriseSvd(SurpriseBase):

    def predict(
        self,
        user_id: str,
        k: int):

            df = pd.DataFrame(self.predictions, columns=['uid','iid','rui','est','details'])
            df = df[df['uid']==user_id].sort_values(by='est', ascending=False)[:k]
            result = df.loc[:,['iid','est']] \
                       .rename(columns={"iid": "company_id", "est": "score"}) \
                       .to_dict('records')

            return result