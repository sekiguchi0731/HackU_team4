import React, { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import "./ReservePage.css";

type Seat = {
  id: number;
  name: string;
  capacity: number;
};

const ReservePage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const shopId = searchParams.get("shop_id");
  const navigate = useNavigate();  // useNavigate フックの追加

  const [shopName, setShopName] = useState("");
  const [seats, setSeats] = useState<Seat[]>([]);
  const [selectedSeatId, setSelectedSeatId] = useState<string>("");
  const [message, setMessage] = useState("");

  // 座席情報取得
  useEffect(() => {
    const fetchSeats = async () => {
      if (!shopId) return;

      try {
        const res = await fetch(
          `http://localhost:5050/reserve_data?shop_id=${shopId}`
        );
        const data = await res.json();

        if (res.ok) {
          setShopName(data.shop_name);
          setSeats(data.seats);
        } else {
          setMessage(data.error || "エラーが発生しました。");
        }
      } catch (error) {
        console.error("通信エラー:", error);
        setMessage("通信エラーが発生しました。");
      }
    };

    fetchSeats();
  }, [shopId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSeatId || !shopName) {
      setMessage("席を選択してください。");
      return;
    }

    const formData = new URLSearchParams();
    formData.append("seat_id", selectedSeatId);
    formData.append("shop_name", shopName);

    try {
      const res = await fetch("http://localhost:5050/reserve", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      });

      if (res.ok) {
        setMessage("予約が完了しました！");
      } else {
        setMessage("予約に失敗しました。");
      }
    } catch (error) {
      console.error("通信エラー:", error);
      setMessage("通信エラーが発生しました。");
    }
  };

  // 戻るボタンのクリックイベント
  const handleBack = () => {
    navigate(-1);  // 前のページに戻る
  };

  return (
    <div className="container py-5">
      <h1 className="mb-4 text-center">予約ページ</h1>
      <p className="text-center">
        選択したお店: <strong>{shopName}</strong>
      </p>

      {seats.length > 0 ? (
        <form onSubmit={handleSubmit}>
          <h3 className="mt-4 available-seats">利用可能な席</h3>
          <ul className="list-group">
            {seats.map((seat) => (
              <li className="list-group-item" key={seat.id}>
                <input
                  type="radio"
                  name="seat"
                  id={`seat-${seat.id}`}
                  value={seat.id}
                  checked={selectedSeatId === String(seat.id)}
                  onChange={(e) => setSelectedSeatId(e.target.value)}
                />
                <label htmlFor={`seat-${seat.id}`} className="ms-2">
                  <strong>席名:</strong> {seat.name} /{" "}
                  <strong>収容人数:</strong> {seat.capacity}
                </label>
              </li>
            ))}
          </ul>
          <div className="text-center mt-4">
            <button type="submit" className="btn-orange">
              予約を確定する
            </button>
          </div>
        </form>
      ) : (
        <p className="text-center mt-4">現在、利用可能な席はありません。</p>
      )}

      {message && <p className="text-center mt-3 message-success">{message}</p>}

      <div className="text-center mt-4">
        <button type="button" className="btn-orange" onClick={handleBack}>
          前のページに戻る
        </button>
      </div>
    </div>
  );
};

export default ReservePage;
