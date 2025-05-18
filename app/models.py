from transformers import pipeline
from pydantic import BaseModel
from app.utils import load_symptom_data, get_disease_description

model = pipeline("text-generation", model="gpt2")

symptom_data = load_symptom_data("disease symptom prediction/symptom_Description.csv")

class ChatRequest(BaseModel):
    input: str

    class Config:
        example = {
            "example": {
                "input": 'What are the symptoms of diabetes?'
            }
        }

def generate_response(user_input):
    user_input_lower = user_input.lower()

    for disease in symptom_data['Disease']:
        if disease.lower() == user_input_lower:
            description = get_disease_description(disease, symptom_data)
            prompt = f"Explain the following disease in simple and exact manner: {description}"
            output = model(prompt, max_length=200, do_sample=True)['generated_text']
            return output
    
    result = model(user_input, max_length=200, do_sample=True)[0]['generated_text']
    return f"I couldn't find that on my database. Here's what i know:\n\n{result}"

def generate_disease_description(prompt):
    result = model(prompt, max_length=200, num_return_sequences=1)
    return result[0]['generated_text']
