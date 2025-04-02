// src/OwnerDashboard.tsx
import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

type Shop = {
  id: number;
  name: string;
  category: string;
  address: string;
};

const OwnerDashboard: React.FC = () => {
  const { owner_id } = useParams();
  const navigate = useNavigate();
  const [shops, setShops] = useState<Shop[]>([]);

  useEffect(() => {
    const fetchShops = async () => {
      const res = await fetch(
        `http://localhost:5050/shops_by_owner/${owner_id}`
      );
      const data = await res.json();
      if (res.ok && data.shops) {
        setShops(data.shops);
      }
    };
    fetchShops();
  }, [owner_id]);

  return (
    <div className="container py-5">
      <h2 className="text-center mb-4">店舗一覧（店主ID: {owner_id}）</h2>

      <div className="text-end mb-4">
        <button
          className="btn btn-success"
          onClick={() => navigate(`/owner/${owner_id}/shop_sign_up`)}
        >
          ＋ 新規店舗を追加
        </button>
      </div>

      {shops.length === 0 ? (
        <p>まだ店舗が登録されていません。</p>
      ) : (
        <ul className="list-group">
          {shops.map((shop) => (
            <li
              key={shop.id}
              className="list-group-item d-flex justify-content-between align-items-center"
            >
              <div>
                <strong>{shop.name}</strong>（{shop.category}）
                <br />
                住所: {shop.address}
              </div>
              <button
                className="btn btn-primary"
                onClick={() =>
                  navigate(`/owner/${owner_id}/seats?shop_id=${shop.id}`)
                }
              >
                席を追加
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default OwnerDashboard;
