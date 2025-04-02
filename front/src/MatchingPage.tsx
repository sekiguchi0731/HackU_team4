// src/MatchingPage.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./MatchingPage.css";

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
    image: "/sushiya.png",
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
      navigate("/reserve");
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
          </div>
          <div className="button-container">
            <button className="nope-button" onClick={() => handleSwipe("left")}>
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
      )}
    </div>
  );
};

export default MatchingPage;