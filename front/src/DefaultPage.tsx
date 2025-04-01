// src/DefaultPage.tsx
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./DefaultPage.css"

const DefaultPage: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/genres"); // 指定秒数後に遷移
    }, 5000); // ← 5秒後に遷移（1000ms = 1秒）

    return () => clearTimeout(timer); // クリーンアップ
  }, [navigate]);

  const title = "Nijimatch".split("");

  return (
    <div className="default-page">
      <h1>Welcome!</h1>
      <h2 className="nijimatch">
        {title.map((char, index) => (
          <span key={index} style={{ animationDelay: `${index * 0.1}s` }}>
            {char}
          </span>
        ))}
      </h2>
      <p>Now loading genres...</p>
    </div>
 
      );
};

export default DefaultPage;
