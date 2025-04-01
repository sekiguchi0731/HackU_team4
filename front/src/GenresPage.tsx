import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // ← 追加
import "./GenresPage.css";

const GenresPage: React.FC = () => {
  const [search, setSearch] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("");
  const [categories, setCategories] = useState<{ name: string }[]>([]);

  const navigate = useNavigate(); // ← これで遷移関数を取得！

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

  // カテゴリクリック時に遷移
  const handleCategoryClick = (categoryName: string) => {
    setSelectedCategory(categoryName);
    navigate("/match"); // ← 遷移！
  };

  return (
    <div className="container">
      <div className="search-container">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="場所を検索..."
          className="search-bar"
        />
        <button className="search-button" onClick={() => navigate("/match")}>
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
            onClick={() => handleCategoryClick(category.name)} // ← ここで遷移
          >
            <p>{category.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default GenresPage;
