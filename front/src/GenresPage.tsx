// src/GenresPage.tsx
import React, { useState, useEffect } from "react";
import './GenresPage.css'; // スタイルシートのインポート

const GenresPage: React.FC = () => {
  const [search, setSearch] = useState(""); // 検索バーの状態
  const [selectedCategory, setSelectedCategory] = useState<string>(""); // 選ばれたカテゴリ
  const [categories, setCategories] = useState<{ name: string }[]>([]); // APIから取得するカテゴリ

  // 初回マウント時にAPIからジャンルを取得
  useEffect(() => {
    fetch("http://localhost:5050/genres")
      .then((res) => res.json())
      .then((data: string[]) => {
        // APIのレスポンス（例: ["居酒屋", "カフェ", ...]）を [{name: "..."}] の形式に変換
        const formatted = data.map((name) => ({ name }));
        setCategories(formatted);
        console.log("取得したカテゴリ:", formatted); // ← console.log もここで！
      })
      .catch((err) => {
        console.error("ジャンル取得エラー:", err);
      });
  }, []);

  return (
    <div className="container">
      {/* 検索バー */}
      <input
        type="text"
        value={search}
        onChange={(e) => setSearch(e.target.value)} // 検索の入力
        placeholder="場所を検索..."
        className="search-bar"
      />
      
      {/* カテゴリーボタン */}
      <div className="category-grid">
        {categories.map((category) => (
          <div
            key={category.name}
            className={`category-button ${selectedCategory === category.name ? "selected" : ""}`}
            onClick={() => setSelectedCategory(category.name)} // クリック時にカテゴリを選択
          >
            <p>{category.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default GenresPage;
