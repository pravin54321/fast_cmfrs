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
#----- default exception handler------------
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
@app.exception_handler(RequestValidationError)#this is use for  request validation error
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)
@app.exception_handler(ResponseValidationError)# this use for response validation error
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=500)

    

   
@app.get("/")
async def root():
    return{'message':'Hellow CMFRS Application'}