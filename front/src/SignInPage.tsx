import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const SignInPage: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const res = await fetch("http://localhost:5050/signed_in", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (res.ok && data.status === "ok") {
      if (data.role === "customer") {
        navigate("/search"); // お客さん用ページに遷移
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
          <label className="form-label">登録メールアドレス</label>
          <input
            type="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">パスワード</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100">
          ログイン
        </button>
        <div className="text-center mt-4">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate("/")}
          >
            前の画面に戻るよ
          </button>
        </div>
      </form>
    </div>
  );
};

export default SignInPage;
