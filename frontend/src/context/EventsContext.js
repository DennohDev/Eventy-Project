// EventsContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserContext } from './UserContext';
const EventsContext = createContext();

const EventsProvider = ({ children }) => {
  const [events, setEvents] = useState([]);
  const [booked, setBooked] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch the current users token from the User context
  const { authToken } = useContext(UserContext);

  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      Authorization: `Bearer ${authToken}`,
    },
  }
  
  console.log("authtoken: ",authToken)

  // Fetch events data when the component mounts
  useEffect(() => {
    const fetchBookedEvents = async () => {
      try {
        const response = await fetch('https://eventy-project.onrender.com/authenticated_user', requestOptions);
        const data = await response.json();
        setBooked(data.events);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching events:', error);
        setLoading(false);
      }
    };

    fetchBookedEvents();
    // eslint-disable-next-line
  }, []);
  console.log("booked events", booked)
  // Fetch events data when the component mounts
  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch('https://eventy-project.onrender.com/events');
        const data = await response.json();
        setEvents(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching events:', error);
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);
  console.log(events)

  return (
    <EventsContext.Provider value={{ events, loading, authToken, booked
     }}>
      {children}
    </EventsContext.Provider>
  );
};

const useEvents = () => {
  const context = useContext(EventsContext);
  if (!context) {
    throw new Error('useEvents must be used within an EventsProvider');
  }
  return context;
};

export { EventsProvider, useEvents };
