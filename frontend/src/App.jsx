import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Header from './Component/header'
import Footer from './Component/Footer'

function App() {
  const [isOpen, setIsOpen] = useState(false)

  const openModal = () => setIsOpen(true)
  const closeModal = () => {
    setIsOpen(false)
    setEmail('')
    setOtp('')
    setShowOtpSection(false)
    setError('')
  }



  return (

    <>
      <Header />


      {/*                           page1 design                                       */}

      <main className="flex-grow flex flex-col items-center justify-center text-center px-6">

        <span className="bg-green-100 text-green-600 text-sm font-semibold px-4 py-1 rounded-full mb-6">
          ● NOW IN EARLY ACCESS
        </span>

        <h2 className="text-[30px] md:text-6xl font-extrabold text-gray-900 leading-tight">
          Cultivating the Future <br />
          <span className=" bg-gradient-to-r 
               from-[#02fa0b] 
               to-[#025905] 
               bg-clip-text 
               text-transparent text-[63px]">with AgriSmart AI</span>
        </h2>

        <p className="text-gray-600 text-lg mt-2 max-w-xl">
          Precision farming powered by intelligent insights.<br />
          Join the revolution today.
        </p>

        <button onClick={openModal}
          className="mt-10 bg-[#02e60a] hover:bg-[#05cd0c] text-black font-semibold px-10 py-4 rounded-xl shadow-lg transition transform hover:scale-105">
          Register  Now →
        </button>

        <div className="flex space-x-8 mt-10 text-gray-500 text-sm">
          <span>📊 Smart Insights</span>
          <span>🎯 Precision Tools</span>
          <span>🌱 Sustainable</span>
        </div>

      </main>

      {/*                                     popup design                                            */}

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center 
                  bg-black/40 backdrop-blur-sm">

          {/* Modal Card */}
          <div className="relative w-[380px] bg-white rounded-2xl 
                    shadow-2xl p-8">

            {/* Close Button */}
            <button
              onClick={closeModal}
              className="absolute top-4 right-4 text-gray-400 
                   hover:text-gray-600 text-xl"
            >
              ✕
            </button>

            {/* Title */}
            <h2 className="text-2xl font-semibold text-center text-gray-900">
              Welcome Back
            </h2>

            {/* Subtitle */}
            <p className="text-center text-gray-500 mt-2 mb-6">
              Log in to manage your AI-powered crops
            </p>

            {/* Google Button */}
            <button className=" w-full flex items-center justify-center gap-3 
                         border border-gray-300 rounded-lg py-3 
                         hover:bg-gray-100 transition">

              <img
                src="https://www.svgrepo.com/show/475656/google-color.svg"
                alt="google"
                className="w-5 h-5"
              />

              <span className="font-medium text-gray-700">
                Log in with Google
              </span>
            </button>

            {/* Links */}
            <div className="mt-6 text-center space-y-3">
              <p className="text-green-500 hover:underline cursor-pointer">
                Forgot your password?
              </p>

              <p className="text-gray-500">
                Don't have an account?{" "}
                <span className="text-green-500 font-medium hover:underline cursor-pointer">
                  Sign up for free
                </span>
              </p>
            </div>

          </div>
        </div>
      )}

      <Footer />




    </>



  );
}

export default App
