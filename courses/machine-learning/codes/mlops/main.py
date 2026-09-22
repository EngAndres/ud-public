import pickle
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

with open('my_scaler.udscaler', 'rb') as f:
    my_scaler = pickle.load(f)

with open('my_model.ud', 'rb') as f:
    my_model = pickle.load(f)

@app.post('/my_model/predictions')
def predict(request):
    new_possum = pd.DataFrame({
        'site': [int(request['site'])],       # Site location
        'Pop': [int(request['Pop'])],        # Population 
        'sex': [int(request['sex'])],        # Male (0) / Female (1)
        'hdlngth': [int(request['hdlngth'])],   # Head length
        'skullw': [int(request['skullw'])],    # Skull width
        'totlngth': [int(request['totlngth'])],  # Total length
        'taill': [int(request['taill'])],     # Tail length
        'footlgth': [int(request['footlgth'])],  # Foot length
        'earconch': [int(request['earconch'])],  # Ear conch length
        'eye': [int(request['eye'])],       # Eye measurement
        'chest': [int(request['chest'])],     # Chest measurement
        'belly': [int(request['belly'])]      # Belly measurement
    })

    # Scale the new data using the same scaler
    new_data = my_scaler.transform(new_possum)

    # Predict age
    return my_model.predict(new_data)
