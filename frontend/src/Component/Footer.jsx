import React from 'react'

const Footer = () => {

  return (
    
    <footer className="flex flex-col md:flex-row justify-between items-center px-8 py-6 text-gray-500 text-sm border-t">
      <p>© 2024 AgriSmart AI. Empowering global agriculture.</p>
      <div class="flex space-x-6 mt-3 md:mt-0">
        <a href="#">Terms of Service</a>
        <a href="#">Privacy Policy</a>
        <a href="#">Contact</a>
      </div>
    </footer>
  )
}

export default Footer
