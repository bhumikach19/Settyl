from fastapi import FastAPI, Request
from pydantic import BaseModel
from hsn_agent import HSNCodeAgent

app = FastAPI()
agent = HSNCodeAgent(r"C:\Users\BHUMIKA\Desktop\Settyl\HSN_SAC.xlsx")

@app.post("/webhook")
async def validate_hsn(request: Request):
    try:
        req_data = await request.json()
        print("Received request data:", req_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"fulfillment_response": {"messages": [{"text": {"text": ["Internal error: " + str(e)]}}]}}

    # Extract HSN codes from ADK parameter format
    codes = []
    try:
        codes = req_data["sessionInfo"]["parameters"].get("hsn_code", [])
        if isinstance(codes, str):
            codes = [codes]
    except Exception:
        return {"fulfillment_response": {"messages": [{"text": {"text": ["Invalid request format."]}}]}}

    # Validate using your agent
    response = agent.handle_input(" ".join(codes))

    return {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [response]
                    
                    }}]}}


# To run this FastAPI app, use the command:
# uvicorn hsn_webhook_api:app --reload