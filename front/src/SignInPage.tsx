import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./SignInPage.css";

const SignInPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const apiUrl = import.meta.env.VITE_API_URL;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const res = await fetch(`${apiUrl}/signed_in`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (res.ok && data.status === "ok") {
      if (data.role === "customer") {
        navigate("/genres"); // お客さん用ページに遷移
      } else if (data.role === "owner") {
        navigate(`/owner/${data.owner_id}`); // 店主用ページに遷移
      }
    } else {
      alert(data.message || "ログイン失敗...");
    }
  };


  return (
    <div className="container py-5 bg-light min-vh-100">
      <h1 className="mb-4 text-center">ログイン画面</h1>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">

          <label className="form-label">登録メールアドレスを入力</label>

          <input
            type="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">

          <label className="form-label">パスワードを入力</label>

          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="btn-group">
          <button type="submit" className="btn-sign-in">
            ログイン
          </button>
          <div className="text-center">
            <button
              type="button"
              className="btn-secondary"
              onClick={() => navigate("/")}
            >
              前の画面に戻る
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default SignInPage;
