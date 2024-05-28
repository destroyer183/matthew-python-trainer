import tkinter as tk 
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


class GlobalState():

    __INSTANCE = None 
    static_var: str = "hello world"

    @staticmethod 
    def get_instance():
        """ Static access method. """
        if GlobalState.__INSTANCE == None:
            GlobalState()

        return GlobalState.__INSTANCE

    def __init__(self):
        """ Virtually private constructor. """

        self.test_var = "hello world"

        if GlobalState.__INSTANCE != None:
            raise Exception("This class is a singleton!")

        GlobalState.__INSTANCE = self



app = FastAPI()


origins = [
    "http://localhost:722",
    "localhost:722",
    "0.0.0.0:722",
]

app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/hello")
async def hello():

    # GlobalState.get_instance().test_var = "this has changed"
    print(GlobalState.static_var)


def tk_main():

    ROOT = tk.Tk()

    GlobalState.static_var = "this has changed"

    ROOT.mainloop()

if __name__ == "__main__":


    import threading

    threading.Thread(target=tk_main).start()

    import uvicorn 
    uvicorn.run(app, host="0.0.0.0", port=3000)


