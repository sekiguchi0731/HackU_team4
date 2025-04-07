import React, { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

const OwnerPage: React.FC = () => {
  const { owner_id } = useParams();
  const navigate = useNavigate();
  const apiUrl = import.meta.env.VITE_API_URL;

  useEffect(() => {
    const checkShop = async () => {
      const res = await fetch(
        `${apiUrl}/owner/${owner_id}/check_shop`
      );
      const data = await res.json();

      if (data.has_shop) {
        navigate(`/owner/${owner_id}/seats`); // 席登録ページへ
      } else {
        navigate(`/owner/${owner_id}/shop_sign_up`); // 店舗登録ページへ
      }
    };

    checkShop();
  }, [owner_id, navigate]);

  return <div>店舗情報を確認中...</div>; // チェック中の間だけ表示
};

export default OwnerPage;
