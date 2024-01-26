import { createContext, useContext, useState } from 'react';
import Swal from 'sweetalert2';
import { UserContext } from '../context/UserContext';
import {useNavigate} from "react-router-dom"



const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authToken, setAuthToken] = useState(
    () => sessionStorage.getItem('authToken') || null
  );

  const updateAuthToken = (token) => {
    setAuthToken(token);
    sessionStorage.setItem('authToken', token);
  };
  const {setCurrentUser} = useContext(UserContext)
  const navigate = useNavigate()
  function logout()
  {
      sessionStorage.removeItem("authToken");
      setCurrentUser(null)
      navigate("/")

      Swal.fire({
          position: "center",
          icon: "success",
          title: "Logout success",
          showConfirmButton: false,
          timer: 1000
          });

  }

  return (
    <AuthContext.Provider value={{ authToken, updateAuthToken, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
