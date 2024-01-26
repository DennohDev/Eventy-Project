import "./App.css";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import Events from "./pages/Events";
import Organizers from "./pages/Organizers/Organizers";
import Layout from "./layout/Layout";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import UserProvider from "./context/UserContext";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { EventsProvider } from './context/EventsContext';
import EventDetails from './pages/EventDetails';
import OrganizerRegister from "./pages/Organizers/OrganizerRegister";
import OrganizerLogin from "./pages/Organizers/OrganizerLogin";
import OrganizerHome from "./pages/Organizers/OrganizerHome";

function App() {
  return (
    <BrowserRouter>
      <UserProvider>
        <EventsProvider>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="Events" element={<Events />} />
            <Route path="Organizers" element={<Organizers />} />
            <Route path="Profile" element={<Profile />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="/events/:id" element={<EventDetails />}/>
            <Route path="organizers/register"  element={<OrganizerRegister />}/>
            <Route path="organizers/login"  element={<OrganizerLogin />}/>
            <Route path="organizers/home"  element={<OrganizerHome />}/>
          </Route>
        </Routes>
        </EventsProvider>
      </UserProvider>
    </BrowserRouter>
  );
}

export default App;
