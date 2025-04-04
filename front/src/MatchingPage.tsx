import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./MatchingPage.css";

type Item = {
  id: number;
  shop_id: number;
  name: string;
  description: string;
  image: string;
};

const MatchingPage: React.FC = () => {
  const location = useLocation(); // useLocationを使用してデータを受け取る
  const navigate = useNavigate();

  // recommendationsを受け取る
  const items: Item[] = location.state?.recommendations || [];
  const [currentIndex, setCurrentIndex] = useState(0);

  const handleSwipe = (direction: "left" | "right") => {
    const currentItem = items[currentIndex];
    if (currentItem) {
      console.log(`現在の要素 - ID: ${currentItem.id}, 店名: ${currentItem.name}`);
    }
    if (direction === "right") {
      navigate(`/reserve?shop_id=${currentItem.shop_id}`);
    } else {
      if (currentIndex < items.length - 1) {
        setCurrentIndex((prev) => prev + 1);
      } else {
        alert("もうカードはありません");
      }
    }
  };

  const currentItem = items[currentIndex];

  return (
    <div className="matching-container">
      {currentItem && (
        <div className="card">
          <div className="card-container">
            <img
              src={currentItem.image}
              alt={currentItem.name}
              className="card-image"
            />
            <h2>{currentItem.name}</h2>
            <p>{currentItem.description}</p>
            <div className="button-container">
              <button
                className="nope-button"
                onClick={() => handleSwipe("left")}
              >
                👎 Nope
              </button>
              <button
                className="like-button"
                onClick={() => handleSwipe("right")}
              >
                ❤️ Like
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MatchingPage;