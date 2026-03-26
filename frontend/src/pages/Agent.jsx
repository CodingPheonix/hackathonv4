import React, { useState } from 'react';
import Header from '../Component/Header';
import WeatherCard from '../Component/WeatherCard';

const AgriSmartUI = () => {
  const [messages, setMessages] = useState([
    { type: 'ai', text: 'Hello, John. Based on soil sensors in Sector 4, moisture dropped to 18%. Irrigation recommended.' },
    { type: 'user', text: 'Start irrigation in Sector 4 for 2 hours. What\'s the nutrient outlook for this week?' },
    { type: 'ai', text: 'I\'ve scheduled irrigation. Here is your nutrient recommendation for the next 7 days:' }
  ]);

  const [input, setInput] = useState('');

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages([...messages, { type: 'user', text: input }]);
    setInput('');
  };

  return (
    <div className="h-screen w-full bg-[#f5f7f6] flex flex-col">
      <Header />

      <div className="flex flex-1 overflow-hidden">

        {/* LEFT PANEL */}
        <div className="w-[320px] bg-white border-r p-4 overflow-y-auto hidden lg:block">
          <h2 className="font-semibold text-gray-700 mb-4">Crop Log & History</h2>

          <div className="space-y-5">

            <div className="bg-gray-50 rounded-xl p-3 shadow-sm">
              <img
                src="https://images.pexels.com/photos/8992138/pexels-photo-8992138.jpeg"
                className="rounded-lg h-28 w-full object-cover"
              />
              <p className="mt-2 font-medium">Nitrogen Check</p>
              <span className="text-green-600 text-xs font-semibold">OPTIMAL</span>
            </div>

            <div className="bg-gray-50 rounded-xl p-3 shadow-sm">
              <img
                src="https://images.pexels.com/photos/33995964/pexels-photo-33995964.jpeg"
                className="rounded-lg h-28 w-full object-cover"
              />
              <p className="mt-2 font-medium">Fungal Detection</p>
              <span className="text-yellow-500 text-xs font-semibold">WARNING</span>
            </div>

            <div className="bg-gray-50 rounded-xl p-3 shadow-sm">
              <p className="font-medium">Soil pH Test</p>
              <p className="text-sm text-gray-500">pH: 6.4 recorded in Sector C</p>
            </div>

            <button className="w-full mt-4 border rounded-lg py-2 text-sm">Export Report</button>
          </div>
        </div>

        {/* CENTER CHAT */}
        <div className="flex-1 flex flex-col">

          {/* Chat Header */}
          <div className="p-4 bg-white border-b flex justify-between items-center">
            <div>
              <h2 className="font-semibold text-gray-700">AI Farming Advisor</h2>
              <p className="text-xs text-green-500">● Online & Monitoring</p>
            </div>
            <button className="bg-green-500 text-white px-4 py-1 rounded-full text-sm">New Session</button>
          </div>

          {/* Messages */}
          <div className="flex-1 p-6 space-y-4 overflow-y-auto">
            {messages.map((msg, index) => (
              <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-lg px-5 py-3 rounded-2xl text-sm shadow ${msg.type === 'user' ? 'bg-green-500 text-white' : 'bg-white text-gray-700'}`}>
                  {msg.text}
                </div>
              </div>
            ))}

            
          </div>

          {/* Input */}
          <div className="p-4 bg-white border-t flex gap-3">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask AgriSmart about your crops..."
              className="flex-1 border rounded-full px-4 py-2"
            />
            <label className="cursor-pointer bg-gray-100 px-3 py-2 rounded-full">📷
              <input type="file" hidden />
            </label>
            <button onClick={sendMessage} className="bg-green-500 text-white px-4 py-2 rounded-full">➤</button>
          </div>
        </div>

        {/* RIGHT PANEL */}
        <div className="w-[320px] bg-white border-l p-4 overflow-y-auto hidden xl:block">
          <h2 className="font-semibold text-gray-700 mb-4">Plant Status</h2>

          <div className="mb-4">
            <p className="text-sm">Growth Stage</p>
            <div className="w-full bg-gray-200 h-2 rounded-full mt-1">
              <div className="bg-green-500 h-2 rounded-full w-[60%]"></div>
            </div>
            <p className="text-xs text-green-600 mt-1">Vegetative</p>
          </div>

          <h3 className="font-medium mt-6 mb-2">Environment</h3>

          {/* <div className="grid grid-cols-2 gap-3">
            <div className="bg-gray-50 p-3 rounded-xl text-center">
              <p className="text-xl font-bold">28°C</p>
              <p className="text-xs">Temp</p>
            </div>
            <div className="bg-gray-50 p-3 rounded-xl text-center">
              <p className="text-xl font-bold">64%</p>
              <p className="text-xs">Humidity</p>
            </div>
            <div className="bg-gray-50 p-3 rounded-xl text-center">
              <p className="text-sm font-bold">1012 hPa</p>
              <p className="text-xs">Pressure</p>
            </div>
            <div className="bg-gray-50 p-3 rounded-xl text-center">
              <p className="text-sm font-bold">12 km/h</p>
              <p className="text-xs">Wind</p>
            </div>
          </div> */}


          

          <WeatherCard />

          <div className="mt-6">
            <h3 className="font-medium mb-2">Rain Forecast</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span>Tomorrow</span><span>24°C</span></div>
              <div className="flex justify-between"><span>Wednesday</span><span>21°C</span></div>
            </div>
          </div>

          <div className="mt-6">
            <h3 className="font-medium mb-2">Soil Analytics</h3>
            <p className="text-sm">Moisture Content</p>
            <div className="w-full bg-gray-200 h-2 rounded-full mt-1">
              <div className="bg-green-500 h-2 rounded-full w-[42%]"></div>
            </div>
            <p className="text-xs text-green-600 mt-1">Healthy</p>

            <div className="flex justify-between mt-4 text-sm">
              <div>
                <p className="text-gray-500">pH</p>
                <p className="font-semibold">6.5</p>
              </div>
              <div>
                <p className="text-gray-500">Nitrogen</p>
                <p className="font-semibold">82%</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default AgriSmartUI;
