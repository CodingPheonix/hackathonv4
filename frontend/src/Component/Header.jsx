import React from 'react'

const Header = () => {
  return (

    <header class="flex justify-between items-center px-8 py-5">
      <div class="flex items-center space-x-2">
        <div class="bg-green-500 p-2 rounded-md">
          <span class="text-white text-lg font-bold">🚜</span>
        </div>
        <h1 class="text-xl font-semibold text-gray-800">AgriSmart.AI</h1>
      </div>

      <nav class="hidden md:flex items-center space-x-8 text-gray-700 font-medium">
        <a href="#" class="hover:text-green-600 transition">Features</a>
        <a href="#" class="hover:text-green-600 transition">Solutions</a>
        <a href="#" class="hover:text-green-600 transition">About</a>
        <button class="border px-5 py-2 rounded-lg hover:bg-gray-100 transition">
          Login
        </button>
      </nav>
    </header>
  )
}

export default Header
