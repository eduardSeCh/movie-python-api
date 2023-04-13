from fastapi import APIRouter
from fastapi import Body, Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie
movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def getMovies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.get('/movies/{id}', tags=['movie'], response_model=List[Movie])
def get_movie(id: int = Path(ge=1, le=2000)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Not found'})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5,max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result: 
        return JSONResponse(content={'message': 'Movie not found'}, status_code=404) 
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.post('/movies',tags=['movies'], response_model=dict)
def crate_movie(movie: Movie) -> dict:     
    db = Session()
    # new_movie = MovieModel(**movie.dict()) 
    # db.add(new_movie)
    # db.commit()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Succesfull"}, status_code=201)

@movie_router.put('/movies/{id}', tags=['movie'], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={'message': 'Movie not found'}, status_code=404) 
    MovieService(db).update_movie(id, movie)
    return JSONResponse(content={"message": "movie updated"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
    db = Session()
    result: MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(content={'message': 'Movie not found'}, status_code=404) 
    MovieService(db).delete_movie(id)
    return JSONResponse(content={"message": "movie eliminated"})