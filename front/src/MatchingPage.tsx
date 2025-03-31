// src/MatchingPage.tsx
import React, { useState } from "react";
import './MatchingPage.css'; // スタイルシートのインポート

// カテゴリーデータ
const categories = [
  { name: "居酒屋" },
  { name: "焼肉" },
  { name: "イタリアン" },
  { name: "中華料理" },
  { name: "寿司" },
  { name: "カフェ" },
  { name: "ファミレス" },
  { name: "ファストフード" },
  { name: "韓国料理" }
];

const MatchingPage: React.FC = () => {
  const [search, setSearch] = useState(""); // 検索バーの状態
  const [selectedCategory, setSelectedCategory] = useState<string>(""); // 選ばれたカテゴリ

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

export default MatchingPage;
