import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./GenresPage.css";

const GenresPage: React.FC = () => {
  const [search, setSearch] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("");
  const [categories, setCategories] = useState<{ name: string }[]>([]);
  const searchInputRef = useRef<HTMLInputElement>(null);

  const navigate = useNavigate();

  useEffect(() => {
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

  const handleCategoryClick = async (categoryName: string) => {
    if (!search) {
      alert("検索バーに住所を入力してください。");
      setTimeout(() => {
        searchInputRef.current?.focus();
      }, 0);
      return;
    }
    setSelectedCategory(categoryName);
  
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const currentTime = `${hours}:${minutes}`;
  
    try {
      const encodedAddress = encodeURIComponent(search);
      const response = await fetch(
        `http://localhost:5050/recommend?user_pos=${encodedAddress}&preferred_category=${categoryName}&current_time=${currentTime}`
      );
  
      console.log("レスポンスステータス:", response.status);
      const data = await response.json();
  
      console.log("推薦結果:", data);
      navigate("/match", { state: { recommendations: data.recommendations } });
  
    } catch (err) {
      console.error("推薦リクエストエラー:", err);
    }
  };


  return (
    <div className="container">
      <div className="search-container">
        <input
          ref={searchInputRef}
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="場所を検索..."
          className="search-bar"
        />
        <button
          className="search-button"
          // onClick={handleSearchClick}
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
