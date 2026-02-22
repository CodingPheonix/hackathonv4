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
      <Header />


      <main classNameName="flex-grow flex flex-col items-center justify-center text-center px-6">

        <span classNameName="bg-green-100 text-green-600 text-sm font-semibold px-4 py-1 rounded-full mb-6">
          ● NOW IN EARLY ACCESS
        </span>

        <h2 classNameName="text-4xl md:text-6xl font-extrabold text-gray-900 leading-tight">
          Cultivating the Future <br />
          <span classNameName="text-green-500">with AgriSmart AI</span>
        </h2>

        <p classNameName="text-gray-600 text-lg mt-6 max-w-xl">
          Precision farming powered by intelligent insights.
          Join the revolution today.
        </p>

        <button onclick="openModal()"
          classNameName="mt-10 bg-green-500 hover:bg-green-600 text-white font-semibold px-10 py-4 rounded-xl shadow-lg transition transform hover:scale-105">
          Register Now →
        </button>

        <div classNameName="flex space-x-8 mt-10 text-gray-500 text-sm">
          <span>📊 Smart Insights</span>
          <span>🎯 Precision Tools</span>
          <span>🌱 Sustainable</span>
        </div>

      </main>




      <Footer />

      {/* <div id="modal"
        className="fixed inset-0 bg-black bg-opacity-60 hidden items-center justify-center z-50 transition">

        <div className="bg-[#111] border border-gray-700 rounded-2xl p-8 w-[90%] max-w-md relative transform scale-95 opacity-0 transition-all duration-300"
          id="modalContent">


          <button onclick="closeModal()"
            className="absolute top-3 right-4 text-gray-400 hover:text-white text-xl">
            ✕
          </button>

          <h3 className="text-white text-xl font-semibold text-center mb-6">
            Login / Register
          </h3>


          <input type="email" placeholder="Enter your email"
            className="w-full mb-5 px-4 py-3 rounded-lg bg-[#1a1a1a] border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-green-500" />


          <button
            className="w-full border border-gray-500 text-white py-3 rounded-lg mb-4 hover:bg-gray-800 transition">
            Log in with Email
          </button>

          <button
            className="w-full border border-gray-500 text-white py-3 rounded-lg hover:bg-gray-800 transition">
            Log in with Google
          </button>

        </div>
      </div > */}


      {/* <script>
        function openModal() {
      const modal = document.getElementById("modal");
        const content = document.getElementById("modalContent");
        modal.classNameList.remove("hidden");

      setTimeout(() => {
          content.classNameList.remove("scale-95", "opacity-0");
        content.classNameList.add("scale-100", "opacity-100");
      }, 10);
    }

        function closeModal() {
      const modal = document.getElementById("modal");
        const content = document.getElementById("modalContent");

        content.classNameList.remove("scale-100", "opacity-100");
        content.classNameList.add("scale-95", "opacity-0");

      setTimeout(() => {
          modal.classNameList.add("hidden");
      }, 300);
    }
      </script> */}


    </>


  );
}

export default App
