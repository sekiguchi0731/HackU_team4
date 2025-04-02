// src/App.tsx
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import DefaultPage from "./DefaultPage";
import GenresPage from "./GenresPage";
import MatchingPage from "./MatchingPage";
import SignInPage from "./SignInPage";
import SignUpPage from "./SignUpPage";
import OwnerDashboard from "./OwnerDashboard";
import ShopSignUpPage from "./ShopSignUpPage";
import SeatRegisterPage from "./SeatRegisterPage";

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DefaultPage />} />
        <Route path="/sign_in" element={<SignInPage />} />
        <Route path="/sign_up" element={<SignUpPage />} />
        <Route path="/genres" element={<GenresPage />} />
        <Route path="/match" element={<MatchingPage />} />
        <Route path="/owner/:owner_id" element={<OwnerDashboard />} />
        <Route path="/owner/:owner_id/shop_sign_up" element={<ShopSignUpPage />} />
        <Route path="/owner/:owner_id/seats" element={<SeatRegisterPage />} />        <Route path="/reserve" element={<div>予約ページへようこそ！</div>} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
