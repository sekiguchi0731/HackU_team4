import React, { useState } from "react";
import './GenresPage.css'; // スタイルシートのインポート

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

const GenresPage: React.FC = () => {
  const [search, setSearch] = useState<string>(""); // 検索バーの状態
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null); // 選ばれたカテゴリ

  // 検索ボタンを押したときの処理
  const handleSearch = () => {
    console.log(`検索ワード: ${search}`);
    alert(`検索ワード: ${search}`); // とりあえずアラートで確認（後でAPI連携などに変更可能）
  };

  return (
    <div className="container">
      {/* 検索エリア */}
      <div className="search-container">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="場所を検索..."
          className="search-bar"
        />
        <button className="search-button" onClick={handleSearch}>
          検索
        </button>
      </div>

      {/* カテゴリーボタン */}
      <div className="category-grid">
        {categories.map((category) => (
          <div
            key={category.name}
            className={`category-button ${selectedCategory === category.name ? "selected" : ""}`}
            onClick={() => setSelectedCategory(category.name)}
          >
            <p>{category.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default GenresPage;
