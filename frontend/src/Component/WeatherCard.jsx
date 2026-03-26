import React, { useEffect, useState } from 'react';
import { useLocationContext } from '../context/locationContext';

const WeatherCard = () => {
  const { location } = useLocationContext();
  const OPENWEATHERAPI = import.meta.env.VITE_OPENWEATHERAPI;

  const [data, setData] = useState({});

  useEffect(() => {
    const fetchWeather = async () => {
      if (!location.lat || !location.lon || !OPENWEATHERAPI) return;

      try {
        const res = await fetch(
          `https://api.openweathermap.org/data/2.5/weather?lat=${location.lat}&lon=${location.lon}&appid=${OPENWEATHERAPI}&units=metric`
        );
        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error(err);
      }
    };

    fetchWeather();
  }, [location, OPENWEATHERAPI]);

  return (
    <div className="grid grid-cols-2 gap-3">
      
      <div className="bg-gray-50 p-3 rounded-xl text-center">
        <p className="text-xl font-bold">
          {data.main ? `${data.main.temp}°C` : "--"}
        </p>
        <p className="text-xs">Temp</p>
      </div>

      <div className="bg-gray-50 p-3 rounded-xl text-center">
        <p className="text-xl font-bold">
          {data.main ? `${data.main.humidity}%` : "--"}
        </p>
        <p className="text-xs">Humidity</p>
      </div>

      <div className="bg-gray-50 p-3 rounded-xl text-center">
        <p className="text-xl font-bold">
          {data.clouds ? `${data.clouds.all}%` : "--"}
        </p>
        <p className="text-xs">Rain</p>
      </div>

      <div className="bg-gray-50 p-3 rounded-xl text-center">
        <p className="text-xl font-bold">
          {data.wind ? `${(data.wind.speed * 3.6).toFixed(1)} km/h` : "--"}
        </p>
        <p className="text-xs">Wind</p>
      </div>

      <div className="bg-gray-50 p-3 rounded-xl text-center col-span-2">
        <p className="text-xl font-bold">
          {data.main ? `${data.main.pressure} hPa` : "--"}
        </p>
        <p className="text-xs">Pressure</p>
      </div>

    </div>
  );
};

export default WeatherCard;