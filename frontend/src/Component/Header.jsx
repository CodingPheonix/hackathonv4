import React from 'react'
import { Link } from 'react-router-dom';

const Header = () => {
  return (

    <header className="flex justify-between items-center px-8 py-5">
      <div className="flex items-center space-x-2">
        <div className="bg-green-500 p-2 rounded-md">
          <span className="text-white text-lg font-bold">🚜</span>
        </div>
        <h1 className="text-xl font-bold text-gray-800">AgriSmart.AI</h1>
      </div>

      <nav className="hidden md:flex items-center space-x-8 text-gray-700 font-medium">
        <Link to="/" className="hover:text-green-600 transition">
          Home
        </Link>
        <a href="#" className="hover:text-green-600 transition">Solutions</a>
        <a href="#" className="hover:text-green-600 transition">About</a>
        <Link
          to="/agent"
          className="bg-[#02e60a] hover:bg-[#05cd0c] px-5 py-2 rounded-full transition text-black"
        >
          New Project
        </Link>
        <button className="border px-5 py-2 rounded-lg hover:bg-gray-100 transition">
          Login
        </button>
      </nav>
    </header>
  )
}

export default Header
