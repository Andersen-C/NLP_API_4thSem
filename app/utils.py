import pandas as pd

def load_symptom_data(file_path):
    df = pd.read_csv(file_path)
    return df

def get_disease_description(disease_name, df):
    description = df[df['Disease'].str.lower() == disease_name.lower()]['Description'].values
    if len(description) > 0:
        return description[0]
    return None
