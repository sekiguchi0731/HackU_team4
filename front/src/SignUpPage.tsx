import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./SingUpPage.css";

const SignUpPage: React.FC = () => {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "",
  });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const res = await fetch("http://localhost:5050/signed_up", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    });

    const data = await res.json();
    if (res.ok) {
      setMessage("登録が完了しました！");
      setForm({ name: "", email: "", password: "", role: "" });
      setTimeout(() => {
        navigate("/sign_in"); // サインインページに遷移
      }, 1000);
    } else {
      setMessage(data.message || "登録に失敗しました。");
      console.error("登録エラー：", data)
    }
  };

  return (
    <div className="container py-5">
      <h2 className="text-center mb-4 signup-title">ユーザ登録画面</h2>
      <form onSubmit={handleSubmit} className="mx-auto" style={{ maxWidth: 600 }}>
        <div className="mb-3">
          <label className="form-label">名前</label>
          <input
            type="text"
            className="form-control"
            name="name"
            value={form.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">メールアドレス</label>
          <input
            type="email"
            className="form-control"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">パスワード</label>
          <input
            type="password"
            className="form-control"
            name="password"
            value={form.password}
            onChange={handleChange}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">お店かお客か選んでください</label>
          <select
            className="form-select"
            name="role"
            value={form.role}
            onChange={handleChange}
            required
          >
            <option value="" disabled>
              どちらか選んでください
            </option>
            <option value="お客">お客</option>
            <option value="店主">店主</option>
          </select>
        </div>
        <div className="d-grid">
          <button type="submit" className="btn btn-primary">
            登録
          </button>
        </div>
        {/* 登録完了メッセージ */}
        {message && <p className="mt-3 text-center">{message}</p>}
      </form>
    </div>
  );
};

export default SignUpPage;
