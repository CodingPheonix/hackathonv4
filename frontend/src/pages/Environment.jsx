import React, { useEffect, useState } from 'react'
import { useLocationContext } from '../context/locationContext'

const Environment = () => {

  const { location } = useLocationContext();

  const OPENWEATHERAPI = import.meta.env.VITE_OPENWEATHERAPI;

  console.log(OPENWEATHERAPI)

  console.log(location)

  useEffect(() => {
    const openWeatherRequest = async () => {
      if (location.lat == '' || location.lon == '' || !OPENWEATHERAPI) return;

      console.log("in request", location)

      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?lat=${location.lat}&lon=${location.lon}&appid=${OPENWEATHERAPI}`
      );

      const res = await response.json();
      console.log(res);
    };

    openWeatherRequest();
  }, [location.lat, location.lon, OPENWEATHERAPI]);



  return (
    <div>
      hello, this is env page
    </div>
  )
}

export default Environment
