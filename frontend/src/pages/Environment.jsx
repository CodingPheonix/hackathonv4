import React, { useEffect, useState } from 'react'
import { useLocationContext } from '../context/locationContext'
import supabase from '../utils/supabase/supabase';
import Header from '../Component/Header';
import Footer from '../Component/Footer';

const Environment = () => {

  const { location } = useLocationContext();
  const OPENWEATHERAPI = import.meta.env.VITE_OPENWEATHERAPI;

  const [locationData, setLocationData] = useState({});

  console.log(OPENWEATHERAPI)
  console.log(location)
  console.log(locationData)

  useEffect(() => {
    const openWeatherRequest = async () => {
      if (!location.lat || !location.lon || !OPENWEATHERAPI) return;

      try {
        const response = await fetch(
          `https://api.openweathermap.org/data/2.5/weather?lat=${location.lat}&lon=${location.lon}&appid=${OPENWEATHERAPI}&units=metric`
        );

        const res = await response.json();
        console.log(res);

        setLocationData(res);

      } catch (error) {
        console.error("Error fetching weather:", error);
      }
    };

    openWeatherRequest();
  }, [location.lat, location.lon, OPENWEATHERAPI]);


  return (
    <div className="bg-gray-50 min-h-screen">

      <Header />

      <div className="max-w-7xl mx-auto px-6 py-8">

        {/* Title */}
        <h1 className="text-4xl font-bold text-gray-900">Farmer Dashboard</h1>
        <p className="text-gray-500 mt-2">
          {locationData.name
            ? `📍 ${locationData.name}, ${locationData.sys?.country}`
            : "Fetching location..."}
        </p>

        {/* Weather Alert */}
        <div className="flex justify-between items-center bg-orange-50 border-l-4 border-orange-400 rounded-lg p-5 mt-6">
          <div className="flex items-center gap-4">
            <div className="text-orange-500 text-2xl">⚠️</div>
            <div>
              <h3 className="font-semibold text-gray-800">
                Weather Alert: Heavy Rain Expected
              </h3>
              <p className="text-gray-500 text-sm">
                Flood risk in low-lying areas. Secure equipment by 4:00 PM.
              </p>
            </div>
          </div>

          <button className="bg-gray-900 text-white px-5 py-2 rounded-lg text-sm">
            Action Plan
          </button>
        </div>

        {/* Weather Stats */}
        <div className="grid grid-cols-4 gap-6 mt-8">

          {/* Temperature */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <p className="text-gray-400 text-sm">TEMPERATURE</p>
            <h2 className="text-3xl font-bold mt-2">
              {locationData.main
                ? `${locationData.main.temp}°C`
                : "--"}
            </h2>
          </div>

          {/* Humidity */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <p className="text-gray-400 text-sm">HUMIDITY</p>
            <h2 className="text-3xl font-bold mt-2">
              {locationData.main
                ? `${locationData.main.humidity}%`
                : "--"}
            </h2>
          </div>

          {/* Rainfall (Cloud %) */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <p className="text-gray-400 text-sm">RAINFALL PROB.</p>
            <h2 className="text-3xl font-bold mt-2">
              {locationData.clouds
                ? `${locationData.clouds.all}%`
                : "--"}
            </h2>
          </div>

          {/* Wind Speed */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <p className="text-gray-400 text-sm">WIND SPEED</p>
            <h2 className="text-3xl font-bold mt-2">
              {locationData.wind
                ? `${(locationData.wind.speed * 3.6).toFixed(1)} km/h`
                : "--"}
            </h2>
          </div>

        </div>

        {/* Bottom Section */}
        <div className="grid grid-cols-3 gap-8 mt-10">

          {/* Recommended Section */}
          <div className="col-span-2">

            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Recommended for You</h2>
              <button className="text-green-600 text-sm">View All →</button>
            </div>

            <div className="grid grid-cols-2 gap-6">

              {/* Rice Card */}
              <div className="bg-white rounded-xl shadow-sm overflow-hidden">
                <img
                  src="https://images.unsplash.com/photo-1536657464919-892534f60d6e"
                  className="h-40 w-full object-cover"
                />

                <div className="p-5">
                  <div className="flex justify-between items-center">
                    <h3 className="font-semibold text-lg">
                      Rice (Oryza sativa)
                    </h3>
                    <span className="text-green-600 text-xs bg-green-100 px-3 py-1 rounded-full">
                      READY TO PLANT
                    </span>
                  </div>

                  <p className="text-green-600 text-sm mt-2">
                    Optimal Matching: 95%
                  </p>

                  <p className="text-gray-500 text-sm mt-3">
                    High soil moisture and upcoming rainfall make this the
                    perfect window for transplanting rice seedlings.
                  </p>

                  <button className="bg-green-500 text-white w-full mt-4 py-2 rounded-lg">
                    View Planting Guide
                  </button>
                </div>
              </div>

              {/* Maize Card */}
              <div className="bg-white rounded-xl shadow-sm overflow-hidden">
                <img
                  src="https://images.unsplash.com/photo-1601597111158-2fceff292cdc"
                  className="h-40 w-full object-cover"
                />

                <div className="p-5">
                  <div className="flex justify-between items-center">
                    <h3 className="font-semibold text-lg">Maize (Corn)</h3>
                    <span className="text-gray-600 text-xs bg-gray-100 px-3 py-1 rounded-full">
                      WAIT 3 DAYS
                    </span>
                  </div>

                  <p className="text-yellow-500 text-sm mt-2">
                    Optimal Matching: 70%
                  </p>

                  <p className="text-gray-500 text-sm mt-3">
                    High humidity detected — avoid planting today to prevent
                    fungal diseases. Wait for drier conditions.
                  </p>

                  <button className="bg-gray-200 text-gray-700 w-full mt-4 py-2 rounded-lg">
                    Setup Reminder
                  </button>
                </div>
              </div>

            </div>
          </div>

          {/* Farm Feed */}
          <div>

            <h2 className="text-xl font-semibold mb-4">Farm Feed</h2>

            <div className="space-y-4">

              <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded">
                <p className="text-red-600 text-xs font-bold">CRITICAL UPDATE</p>
                <p className="text-sm font-semibold">
                  Heavy rain expected tomorrow morning.
                </p>
                <p className="text-gray-500 text-xs">
                  Delay fertilizer application to prevent nutrient runoff.
                </p>
              </div>

              <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded">
                <p className="text-green-600 text-xs font-bold">SOIL HEALTH</p>
                <p className="text-sm font-semibold">
                  Nitrogen levels optimal in Block A.
                </p>
                <p className="text-gray-500 text-xs">
                  Great conditions for leafy greens this week.
                </p>
              </div>

              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                <p className="text-yellow-600 text-xs font-bold">MARKET WATCH</p>
                <p className="text-sm font-semibold">
                  Maize market prices up by 5%.
                </p>
                <p className="text-gray-500 text-xs">
                  Consider harvesting early if crop is mature.
                </p>
              </div>

              <div className="bg-gray-50 border p-4 rounded">
                <p className="text-gray-600 text-xs font-bold">MAINTENANCE</p>
                <p className="text-sm font-semibold">
                  Irrigation pump service due.
                </p>
                <p className="text-gray-500 text-xs">
                  Scheduled for Thursday at 10:00 AM.
                </p>
              </div>

              <button className="w-full border-2 border-dashed border-gray-300 py-3 rounded-lg text-gray-500">
                + Add Custom Note
              </button>

            </div>
          </div>

        </div>

        <Footer />

      </div>

    </div>
  )
}

export default Environment