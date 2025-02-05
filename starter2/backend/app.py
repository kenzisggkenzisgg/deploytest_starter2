from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
import difflib
import uvicorn
from fastapi import FastAPI

app = FastAPI()

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# CORSの設定 フロントエンドからの接続を許可する部分
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# データのスキーマを定義するためのクラス
class EchoMessage(BaseModel):
    message: str | None = None
    
@app.get("/")
def index():
    return {"message": "FastAPI top page!"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

@app.get("/api/movie")
def get_movie_info(title: str = Query(..., description="映画のタイトル")):
    search_url = "https://api.themoviedb.org/3/search/movie"
    search_params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "include_adult": "false",
        "language": "ja",
    }
        # APIを呼び出す(映画ID取得用)
    search_response = requests.get(search_url, params=search_params)
    if search_response.status_code == 200:
        search_data = search_response.json()

        # タイトルの類似度を評価して最も近い映画を選択
        def get_title_similarity(s1, s2):
            return difflib.SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

        most_similar_movie = max(
            search_data["results"],
            key=lambda movie: get_title_similarity(movie["title"], title)
        )
        movie_id = most_similar_movie["id"]

        # 映画詳細情報の取得
        detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        detail_params = {"api_key": TMDB_API_KEY, "language": "ja"}
        detail_response = requests.get(detail_url, params=detail_params)
        if detail_response.status_code == 200:
            detail_data = detail_response.json()
            
    return {
        "tmdb_id": movie_id,
        "title": detail_data['title'],
        "original_title": detail_data['original_title'],
        "overview": detail_data['overview']
        }