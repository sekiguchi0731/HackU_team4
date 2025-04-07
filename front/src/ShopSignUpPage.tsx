import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const ShopSignUpPage: React.FC = () => {
  const { owner_id } = useParams();
  const navigate = useNavigate();
  const apiUrl = import.meta.env.VITE_API_URL;

  const [form, setForm] = useState({
    name: "",
    category: "",
    address: "",
    phone: "",
    opening_time: "",
    closing_time: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const res = await fetch(`${apiUrl}/shops`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        ...form,
        owner_id: owner_id || "",
      }),
    });

    if (res.ok) {
      navigate(`/owner/${owner_id}/`);
    } else {
      alert("店舗登録に失敗しました");
    }
  };

  return (
    <div className="container py-5">
      <h2 className="text-center mb-4">店舗登録</h2>
      <form
        onSubmit={handleSubmit}
        className="mx-auto"
        style={{ maxWidth: 600 }}
      >
        <div className="mb-3">
          <label className="form-label">店舗名</label>
          <input
            type="text"
            name="name"
            value={form.name}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">カテゴリ</label>
          <input
            type="text"
            name="category"
            value={form.category}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">住所</label>
          <input
            type="text"
            name="address"
            value={form.address}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">電話番号</label>
          <input
            type="text"
            name="phone"
            value={form.phone}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">開店時間（例: 10:00）</label>
          <input
            type="text"
            name="opening_time"
            value={form.opening_time}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">閉店時間（例: 22:00）</label>
          <input
            type="text"
            name="closing_time"
            value={form.closing_time}
            onChange={handleChange}
            className="form-control"
            required
          />
        </div>
        <div className="d-grid mb-2">
          <button type="submit" className="btn btn-sign-up">
            登録
          </button>
        </div>

        {/* 前に戻るボタン */}
        <div className="d-grid">
          <button
            type="button"
            className="btn btn-back"
            onClick={() => navigate(-1)}
          >
            前に戻る
          </button>
        </div>
      </form>
    </div>
  );
};

export default ShopSignUpPage;
