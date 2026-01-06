from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world"}

if __name__ == "__main__":
    app.run() # wrong idk