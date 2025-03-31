// src/MatchingPage.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

type Item = {
  id: number;
  name: string;
  description: string;
  image: string;
};

const items: Item[] = [
  {
    id: 1,
    name: "Sushi Restaurant",
    description: "Fresh sushi near the station 🍣",
    image: "https://source.unsplash.com/300x200/?sushi",
  },
  {
    id: 2,
    name: "Ramen Shop",
    description: "Spicy miso ramen available 🍜",
    image: "https://source.unsplash.com/300x200/?ramen",
  },
  {
    id: 3,
    name: "Cafe Latte",
    description: "Cozy cafe with great drinks ☕",
    image: "https://source.unsplash.com/300x200/?cafe",
  },
];

const MatchingPage: React.FC = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const navigate = useNavigate();

  const handleSwipe = (direction: "left" | "right") => {
    if (direction === "right") {
      // Like → reserveページへ遷移
      navigate("/reserve");
    } else {
      // Nope → 次のカードへ
      if (currentIndex < items.length - 1) {
        setCurrentIndex((prev) => prev + 1);
      } else {
        alert("もうカードはありません");
      }
    }
  };

  const currentItem = items[currentIndex];

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      {currentItem && (
        <div
          style={{
            width: 320,
            height: 420,
            border: "1px solid #ccc",
            borderRadius: 16,
            boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
            overflow: "hidden",
            position: "relative",
            textAlign: "center",
            backgroundColor: "#fff",
          }}
        >
          <img
            src={currentItem.image}
            alt={currentItem.name}
            style={{ width: "100%", height: 200, objectFit: "cover" }}
          />
          <h2>{currentItem.name}</h2>
          <p>{currentItem.description}</p>
          <div
            style={{
              display: "flex",
              justifyContent: "space-around",
              position: "absolute",
              bottom: 20,
              width: "100%",
            }}
          >
            <button onClick={() => handleSwipe("left")}>👎 Nope</button>
            <button onClick={() => handleSwipe("right")}>❤️ Like</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default MatchingPage;
