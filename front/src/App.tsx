// src/App.tsx
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import DefaultPage from "./DefaultPage";
import GenresPage from "./GenresPage";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DefaultPage />} />
        <Route path="/genres" element={<GenresPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
