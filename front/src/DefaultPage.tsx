// src/DefaultPage.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import "./DefaultPage.css";
import logo from "./assets/logo.png";

const DefaultPage: React.FC = () => {
  const title = "NijiMatch".split("");
  const navigate = useNavigate();

  const handleSignIn = () => {
    navigate("/sign_in");
  };

  const handleSignUp = () => {
    navigate("/sign_up");
  };

  return (
    <div className="default-page">
      {/* NijiMatch アニメーションタイトル */}
      <h2 className="nijimatch">
        {title.map((char, index) => (
          <span key={index} style={{ animationDelay: `${index * 0.1}s` }}>
            {char}
          </span>
        ))}
      </h2>

      {/* ロゴ画像 */}
      <div className="header-logo">
        <img src={logo} alt="NijiMatch Logo" className="logo-image" />
      </div>

      {/* ボタン群 */}
      <div className="button-group">
        <button onClick={handleSignUp}>新規登録</button>
        <button onClick={handleSignIn}>サインイン</button>
      </div>
    </div>
  );
};

export default DefaultPage;
