import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Header from './Component/header'
import Footer from './Component/Footer'

function App() {
  const [count, setCount] = useState(0)

  return (

    <>
      <Header/>
    

      <main className="flex-grow flex flex-col items-center justify-center text-center px-6">

        <span className="bg-green-100 text-green-600 text-sm font-semibold px-4 py-1 rounded-full mb-6">
          ● NOW IN EARLY ACCESS
        </span>

        <h2 className="text-4xl md:text-6xl font-extrabold text-gray-900 leading-tight">
          Cultivating the Future <br />
            <span className="text-green-500">with AgriSmart AI</span>
        </h2>

        <p className="text-gray-600 text-lg mt-6 max-w-xl">
          Precision farming powered by intelligent insights.
          Join the revolution today.
        </p>

        <button onclick="openModal()"
          className="mt-10 bg-green-500 hover:bg-green-600 text-white font-semibold px-10 py-4 rounded-xl shadow-lg transition transform hover:scale-105">
          Register Now →
        </button>

        <div className="flex space-x-8 mt-10 text-gray-500 text-sm">
          <span>📊 Smart Insights</span>
          <span>🎯 Precision Tools</span>
          <span>🌱 Sustainable</span>
        </div>

      </main>
  


  
      <Footer/>
    </>


  );
}

export default App
