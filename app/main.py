from .routers import users,admin
from .dependencies import *

origins = ["*"]
app = FastAPI()
app.include_router(users.router)
app.include_router(admin.router)
app.mount("/Static",StaticFiles(directory="./Static") , name="images")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods here (e.g., ["GET", "POST"])
    allow_headers=["*"],  # You can specify specific HTTP headers here
)

    

   
@app.get("/")
async def root():
    return{'message':'Hellow CMFRS Application'}