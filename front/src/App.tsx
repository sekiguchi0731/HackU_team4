// src/App.tsx
import React from 'react'
import './App.css'
import GenresPage from './GenresPage'

const App: React.FC = () => {
  return (
    <div className="App">
      <GenresPage /> {/* GenresPageコンポーネントを表示 */}
    </div>
  )
}

export default App
