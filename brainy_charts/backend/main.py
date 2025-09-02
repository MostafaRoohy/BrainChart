# This is the entry point for the FastAPI application,
# where the app is initialized, middleware is configured,
# and all the API endpoints from routes.py are included.
###################################################################################################
###################################################################################################
###################################################################################################
#
from pathlib import Path

from fastapi                 import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
# from fastapi.responses       import FileResponse, JSONResponse
from fastapi.staticfiles     import StaticFiles
#
###################################################################################################
###################################################################################################
###################################################################################################
#
from .routes   import router
from .models   import Base
from .database import engine
#
###################################################################################################
###################################################################################################
###################################################################################################
#
app = FastAPI(title="BrainyCharts Backend")
app.include_router(router)
Base.metadata.create_all(bind=engine)
#
###################################################################################################
###################################################################################################
###################################################################################################
#
BACKEND_DIR    = Path(__file__).resolve().parent                 # brainy_charts/backend
PKG_DIR        = BACKEND_DIR.parent                              # brainy_charts
ROOT_DIR       = PKG_DIR.parent                                  # project root (BrainyCharts/)
FRONTEND_DIR   = PKG_DIR / "frontend" / "chart_widget"           # brainy_charts/frontend/widget/
TV_LIB_DIR     = ROOT_DIR / "charting_library"                   # charting_library/
DATAFEEDS_DIR  = TV_LIB_DIR / "datafeeds"                        # charting_library/datafeeds/

app.mount("/charting_library", StaticFiles(directory=str(TV_LIB_DIR)   , html=False), name="charting_library")
app.mount("/datafeeds"       , StaticFiles(directory=str(DATAFEEDS_DIR), html=False), name="datafeeds")


# for now i decided to define the entry index.html as mounting static
app.mount("/"                , StaticFiles(directory=str(FRONTEND_DIR) , html=True) , name="frontend")
# @app.get("/")
# def serve_widget_index():
#     index_path = FRONTEND_DIR / "index.html"
#     if not index_path.exists():

#         return JSONResponse(
#             {"error": "index.html not found", "expected": str(index_path)},
#             status_code=500,
#         )
#     #
#     return FileResponse(index_path)
# #
###################################################################################################
###################################################################################################
###################################################################################################
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)
#
###################################################################################################
###################################################################################################
###################################################################################################
#