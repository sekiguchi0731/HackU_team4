import React, { useState, useEffect } from "react";
import "./App.css"; // CSS を読み込む

const App = () => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    setTimeout(() => {
      setVisible(true);
    }, 500); // 0.5秒後にフェードイン開始
  }, []);

  return (
    <div className="app-container">
      <h1 className={`app-title ${visible ? "fade-in" : ""}`}>マッチングアプリ</h1>
    </div>
  );
};

export default App;
