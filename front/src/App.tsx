// src/App.tsx
import React from 'react'
import './App.css'
import MatchingPage from './MatchingPage' // MatchingPageコンポーネントをインポート

const App: React.FC = () => {
  return (
    <div className="App">
      <MatchingPage /> {/* MatchingPageコンポーネントを表示 */}
    </div>
  )
}

export default App
