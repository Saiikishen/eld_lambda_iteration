
import pandas as pd

def load_and_preprocess_data(filepath):

    data = pd.read_excel(filepath)
    
    # print(data.info())
    # print(data.head())


    data['Date'] = data['Date'].ffill()
    
    try:
        data['Date'] = pd.to_datetime(data['Date'], format='%d.%m.%Y')
        
        data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S').dt.time
        
        data['Timestamp'] = data.apply(
            lambda row: pd.Timestamp.combine(row['Date'], row['Time']),
            axis=1
        )
        
    except Exception as e:
        print(f"Error during datetime conversion: {e}")
        raise
    
    data = data.drop(columns=['Date', 'Time'])
    

    data = data.sort_values('Timestamp')
    

    data = data.reset_index(drop=True)
    

    # print(data.info())
    # print(data.head())
    
    return data

