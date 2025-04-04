import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./GenresPage.css";

const GenresPage: React.FC = () => {
  const [search, setSearch] = useState(""); // 住所
  const [selectedCategory, setSelectedCategory] = useState<string>(""); // 選択されたカテゴリ
  const [categories, setCategories] = useState<{ name: string }[]>([]);

  const navigate = useNavigate();

  useEffect(() => {
    // ジャンルを取得
    fetch("http://localhost:5050/genres")
      .then((res) => res.json())
      .then((data: string[]) => {
        const formatted = data.map((name) => ({ name }));
        setCategories(formatted);
        console.log("取得したカテゴリ:", formatted);
      })
      .catch((err) => {
        console.error("ジャンル取得エラー:", err);
      });
  }, []);

  // カテゴリクリック時にrecommendエンドポイントにリクエストを送信
  const handleCategoryClick = (categoryName: string) => {
    setSelectedCategory(categoryName);
  
    // 固定時刻を設定
    const fixedTime = "15:00";
  
    // recommendエンドポイントにリクエストを送信
    fetch(
      `http://localhost:5050/recommend?user_lat=35.6895&user_lng=139.6917&preferred_category=${categoryName}&current_time=${fixedTime}`,
      {
        method: "GET",
      }
    )
      .then((res) => {
        console.log("レスポンスステータス:", res.status);
        return res.json();
      })
      .then((data) => {
        console.log("推薦結果:", data);
        // 推薦結果を次のページに渡す（例: /match ページに遷移）
        navigate("/match", { state: { recommendations: data.recommendations } });
      })
      .catch((err) => {
        console.error("推薦エラー:", err);
      });
  };

  return (
    <div className="container">
    
      <h2 className="search-title">お店の条件を入力</h2>


      <div className="search-container">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="場所を検索..."
          className="search-bar"
        />
        <button
          className="search-button"
          onClick={() => handleCategoryClick(selectedCategory)}
        >
          検索
        </button>
      </div>

      <div className="category-grid">
        {categories.map((category) => (
          <div
            key={category.name}
            className={`category-button ${
              selectedCategory === category.name ? "selected" : ""
            }`}
            onClick={() => handleCategoryClick(category.name)}
          >
            <p>{category.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default GenresPage;