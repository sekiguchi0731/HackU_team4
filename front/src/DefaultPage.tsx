// src/DefaultPage.tsx
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const DefaultPage: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/genres"); // 指定秒数後に遷移
    }, 3000); // ← 3秒後に遷移（1000ms = 1秒）

    return () => clearTimeout(timer); // クリーンアップ
  }, [navigate]);

  return (
    <div style={{ textAlign: "center", marginTop: "30vh" }}>
      <h1>Welcome!</h1>
      <p>Now loading genres...</p>
    </div>
  );
};

export default DefaultPage;
