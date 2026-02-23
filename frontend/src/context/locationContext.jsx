import React, { createContext, useContext, useState, useEffect } from 'react'

export const locationContext = createContext({
    lat: "",
    lon: ""
})
export const useLocationContext = () => useContext(locationContext)

const LocationContext = ({ children }) => {

    const [location, setLocation] = useState({
        lat: "",
        lon: ""
    })

    useEffect(() => {
        if (location.lat !== "") {
            return
        }

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    setLocation({
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    })
                },
                error => {
                    console.error("Error getting location:", error.message);
                }
            );
        } else {
            alert("Kindly allow location on your device and browser!")
        }
    }, [location])

    return (
        <locationContext.Provider value={{ location, setLocation }}>
            {children}
        </locationContext.Provider>
    )
}

export default LocationContext
