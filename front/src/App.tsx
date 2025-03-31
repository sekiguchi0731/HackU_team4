// src/App.tsx
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import DefaultPage from "./DefaultPage";
import GenresPage from "./GenresPage";
import MatchingPage from "./MatchingPage";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DefaultPage />} />
        <Route path="/genres" element={<GenresPage />} />
        <Route path="/match" element={<MatchingPage />} />
        <Route path="/reserve" element={<div>予約ページへようこそ！</div>} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
