'use client';
import { useState } from 'react';

export default function Home() {
  // useStateを使った値（状態）管理
  const [movieTitle, setMovieTitle] = useState('');
  const [movieInfo, setMovieInfo] = useState('');
  const [error, setError] = useState('');

  // FastAPIのエンドポイント設定
  const handleSearchMovie = async () => {
    if (!movieTitle){
      setError('映画のタイトルを入力してください');
      return;
    }
    setError('');
    try {
      const response = await fetch(`http://localhost:8000/api/movie?title=${encodeURIComponent(movieTitle)}`);
      if (!response.ok){
        throw new Error('映画情報が取得できませんでした');
      }
      const data = await response.json();
      setMovieInfo(data);
    } catch (error) {
      setError(error.message);
      setMovieInfo(null);
    }
  };

  // ユーザーインターフェースの構築
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">映画情報検索アプリ</h1>
      <div className="space-y-8">
        {/* 映画タイトル入力 */}
        <section>
          <h2 className="text-xl font-bold mb-4">映画のタイトルを入力してください</h2>
          <div className="flex gap-2">
            <input
              type="text"
              value={movieTitle}
              onChange={(e) => setMovieTitle(e.target.value)}
              className="border rounded px-2 py-1 w-64"
              placeholder="映画タイトルを入力"
            />
            <button
              onClick={handleSearchMovie}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
            >
              検索
            </button>
          </div>
          {error && <p className="mt-2 text-red-500">{error}</p>}
        </section>

        {/* 取得した映画情報の表示 */}
        {movieInfo && (
          <section>
            <h2 className="text-xl font-bold mb-4">映画情報</h2>
            <div className="border p-4 rounded">
              <h3 className="text-lg font-bold">オリジナルタイトル : {movieInfo.original_title} </h3>
              <h4 className="text-lg font-bold">概要：{movieInfo.overview} </h4>
            </div>
          </section>
          )}
      </div>
    </div>
  );
} 