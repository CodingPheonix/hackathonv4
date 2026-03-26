import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Environment from './pages/Environment'
import Agent from './pages/Agent'

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/environment" element={<Environment />} />
        <Route path='/agent' element={<Agent />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
