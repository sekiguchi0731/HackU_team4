import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "./SeatRegisterPage.css";

type Shop = {
  id: number;
  name: string;
};

const SeatRegisterPage: React.FC = () => {
  const { owner_id } = useParams();
  const navigate = useNavigate();

  const [shops, setShops] = useState<Shop[]>([]);
  const [selectedShopId, setSelectedShopId] = useState<string>("");
  const [seatName, setSeatName] = useState("");
  const [capacity, setCapacity] = useState<string>("1");
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchShops = async () => {
      const res = await fetch(
        `http://localhost:5050/shops_by_owner/${owner_id}`
      );
      const data = await res.json();

      if (res.ok && data.shops && data.shops.length > 0) {
        setShops(data.shops);
        setSelectedShopId(data.shops[0].id.toString());
      } else {
        alert("店舗が見つかりませんでした。");
        navigate(`/owner/${owner_id}/shop_sign_up`);
      }
    };

    fetchShops();
  }, [owner_id, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const parsedCapacity = parseInt(capacity, 10);

    if (isNaN(parsedCapacity) || parsedCapacity < 1) {
      setMessage("収容人数は1以上の数字を入力してください。");
      return;
    }

    const res = await fetch("http://localhost:5050/seats_register", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        name: seatName,
        capacity: parsedCapacity.toString(),
        shop_id: selectedShopId,
      }),
    });

    if (res.ok) {
      setMessage("席を登録しました！");
      setSeatName("");
      setCapacity("1");
    } else {
      setMessage("登録に失敗しました。");
    }
  };

  return (
    <div className="container">
      <h2 className="title">席の登録</h2>

      <form onSubmit={handleSubmit} className="mx-auto" style={{ maxWidth: 600 }}>
        <div className="mb-3">
          <label className="form-label">店舗を選択</label>
          <select
            className="form-select"
            value={selectedShopId}
            onChange={(e) => setSelectedShopId(e.target.value)}
            required
          >
            {shops.map((shop) => (
              <option key={shop.id} value={shop.id}>
                {shop.name}
              </option>
            ))}
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">席の名前</label>
          <input
            type="text"
            className="form-control"
            value={seatName}
            onChange={(e) => setSeatName(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">収容人数</label>
          <input
            type="number"
            className="form-control"
            value={capacity}
            onChange={(e) => setCapacity(e.target.value)}
            min={1}
            required
          />
        </div>

        <div className="d-grid">
          <button type="submit" className="orange-submit-button">
            登録
          </button>
        </div>

        {message && (
          <div>
            <p className="message">{message}</p>
            {/* 戻るボタンを登録メッセージの下に追加 */}
            <button
              className="back-button"
              type="button"
              onClick={() => navigate(-1)}
            >
              ← 前のページに戻る
            </button>
          </div>
        )}
      </form>
    </div>
  );
};

export default SeatRegisterPage;
