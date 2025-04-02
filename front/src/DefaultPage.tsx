// src/DefaultPage.tsx
import React from "react";
import { useNavigate } from "react-router-dom";
import "./DefaultPage.css"

const DefaultPage: React.FC = () => {
  const title = "NijiMatch".split("");
  const navigate = useNavigate();

  const handleSignIn = () => {
    navigate("/sign_in"); // React 内で画面遷移！
  };

  const handleSignUp = () => {
    navigate("/sign_up"); // React 内で画面遷移！
  };

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

      <div className="button-group">
        <button onClick={handleSignUp}>新規登録</button>
        <button onClick={handleSignIn}>サインイン</button>
      </div>
    </div>
  );
};

export default DefaultPage;
