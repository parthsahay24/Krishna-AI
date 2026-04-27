from fastapi import FastAPI
from modules import config, llm_handler, memory_manager

app = FastAPI(title="Krishna AI")

# ROUTE 1: Status Check (Uses the static config name)
@app.get("/")
def home():
    return {
        "status": "Krishna is online", 
        "user_in_env": config.USER_NAME,
        "message": f"Namaste!" 
    }

# ROUTE 2: The Actual Chat (Uses the dynamic learned name)
@app.get("/chat")
def chat(message: str):
    """
    This is where the magic happens. 
    Krishna will check his memory to see if he knows you.
    """
    response = llm_handler.get_krishna_response(message)
    return {"krishna": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=config.SERVER_PORT, reload=True)
