import { useEffect, useState } from 'react'
import Header from '../Component/Header'
import Footer from '../Component/Footer'
import { signInWithGoogle, signInWithOtp } from '../utils/supabase/auth'
import OTPInput from '../Component/OTP'
import { useNavigate } from 'react-router'
import { UseUserContext } from '../context/authContext'

function Home() {
  const [isOpen, setIsOpen] = useState(false)
  /////////////////////////////////////////////////////////////////////////////

  const [email, setEmail] = useState('')
  const [otp, setOtp] = useState('')
  const [showOtpSection, setShowOtpSection] = useState(false)
  const [error, setError] = useState('')

  /////////////////////////////////////////////////////////////////////////////

  const navigate = useNavigate();
  const session = UseUserContext();

  const openModal = () => setIsOpen(true)
  const closeModal = () => {
    setIsOpen(false)
    setEmail('')
    setOtp('')
    setShowOtpSection(false)
    setError('')
  }

  ///////////////////////////////////////////////////////////////////////////

  const handleEmailSubmit = async () => {

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    if (!emailPattern.test(email)) {
      setError("Please enter a valid email")
      return
    }

    console.log(email)

    const { data, error } = await signInWithOtp({ email: email })

    console.log(data)

    if (data.session === null && data.user === null) {
      setShowOtpSection(true)
    }

    // setError("")

    // const generatedOtp = Math.floor(1000 + Math.random() * 9000)
    // setOtp(generatedOtp)

    // setShowOtpSection(true)
  }

  const handleGoogleSubmit = async () => {
    const { data, error } = await signInWithGoogle();

    console.log(data, error)
  }

  useEffect(() => {
    if (session !== null) {
      navigate('/environment')
    }
  }, [session])


  return (
    // <>
    //   <Header />

    //   <main className="grow flex flex-col items-center justify-center text-center px-6">

    //     <span className="bg-green-100 text-green-600 text-sm font-semibold px-4 py-1 rounded-full mb-6">
    //       ● NOW IN EARLY ACCESS
    //     </span>

    //     <h2 className="text-4xl md:text-6xl font-extrabold text-gray-900 leading-tight">
    //       Cultivating the Future <br />
    //       <span className="text-green-500">with AgriSmart AI</span>
    //     </h2>

    //     <p className="text-gray-600 text-lg mt-6 max-w-xl">
    //       Precision farming powered by intelligent insights.
    //       Join the revolution today.
    //     </p>

    //     <button onClick={openModal}
    //       className="mt-10 bg-green-500 hover:bg-green-600 text-white font-semibold px-10 py-4 rounded-xl shadow-lg transition transform hover:scale-105">
    //       Register Now →
    //     </button>

    //     <div className="flex space-x-8 mt-10 text-gray-500 text-sm">
    //       <span>📊 Smart Insights</span>
    //       <span>🎯 Precision Tools</span>
    //       <span>🌱 Sustainable</span>
    //     </div>

    //   </main>


    //   {isOpen && (
    //     <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">

    //       <div className="bg-[#111] border border-gray-700 rounded-2xl p-8 w-[90%] max-w-md relative transform transition-all duration-300 scale-100 opacity-100">

    //         {/* Close Button */}
    //         <button
    //           onClick={closeModal}
    //           className="absolute top-3 right-4 text-gray-400 hover:text-white text-xl"
    //         >
    //           ✕
    //         </button>

    //         <h3 className="text-white text-xl font-semibold text-center mb-6">
    //           Login / Register
    //         </h3>

    //         <input
    //           type="email"
    //           placeholder="Enter your email"
    //           value={email}
    //           onChange={(e) => setEmail(e.target.value)}
    //           className="w-full mb-2 px-4 py-3 rounded-lg bg-[#1a1a1a] border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-green-500"
    //         />

    //         {error && (
    //           <p className="text-red-500 text-sm mb-3">{error}</p>
    //         )}

    //         <button
    //           onClick={handleEmailSubmit}
    //           className="w-full border border-gray-500 text-white py-3 rounded-lg mb-4 hover:bg-gray-800 transition"
    //         >
    //           Log in with Email
    //         </button>

    //         <button
    //           onClick={handleGoogleSubmit}
    //           className="w-full border border-gray-500 text-white py-3 rounded-lg hover:bg-gray-800 transition">
    //           Log in with Google
    //         </button>

    //       </div>
    //     </div>
    //   )}

    //   <Footer />

    //   {/*  OTP SECTION */}
    //   {showOtpSection && (
    //     // <div className="mt-6 border-t border-gray-700 pt-5 text-center">

    //     //   <h4 className="text-green-400 font-semibold mb-2">
    //     //     Your 4 Digit OTP
    //     //   </h4>

    //     //   <div className="text-3xl font-bold tracking-widest text-white bg-black py-3 rounded-lg">
    //     //     {otp}
    //     //   </div>

    //     // </div>

    //     <OTPInput />
    //   )}

    // </>


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
                         hover:bg-gray-100 transition"
              onClick={handleGoogleSubmit}>



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

export default Home
