from fastapi import APIRouter, Request
from app.models import generate_response, ChatRequest, generate_disease_description
from app.utils import load_symptom_data, get_disease_description

router = APIRouter()
symptom_data = load_symptom_data("disease symptom prediction/symptom_Description.csv")

@router.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.input
    response = generate_response(user_input)
    return {"response": response}

@router.get("/disease/{disease_name}")
async def get_disease_info(disease_name: str):
    description = get_disease_description(disease_name, symptom_data)
    if description:
        return {"disease": disease_name, "description": description}
    else:
        prompt = f"Explain the disease called {disease_name}' in a informative and detailed way"
        result = generate_disease_description(prompt)
        return {"disease": disease_name, "description": result}
