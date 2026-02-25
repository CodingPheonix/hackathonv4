import React, { useEffect, useState, useContext, createContext } from 'react'
import supabase from '../utils/supabase/supabase'

// move context creation outside component so it can be imported elsewhere
export const UserContext = createContext(null)

export const UseUserContext = () => useContext(UserContext);

const AuthContext = ({ children }) => {

  const [session, setSession] = useState(null)

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {

      if (!session) {
        return;
      }

      setSession(session)
    })
  }, [])

  console.log(session)

  return (
    <UserContext.Provider value={session}>
      {children}
    </UserContext.Provider>
  )
}

export default AuthContext
