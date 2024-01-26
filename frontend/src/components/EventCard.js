import React, { useContext, useState } from 'react';
import { useEvents } from '../context/EventsContext';
import { UserContext } from '../context/UserContext';
import { Link } from 'react-router-dom';

const EventList = () => {
  const { events, loading } = useEvents();
  const { authToken, currentUser } = useContext(UserContext);
  const [refreshPage, setRefreshPage] = useState(false);

  const bookEvent = (eventId) => {
    if (!currentUser) {
      console.error('User not authenticated.');
      return;
    }

    fetch('http://localhost:5000/bookedevents', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`,
      },
      body: JSON.stringify({
        event_id: eventId,
        user_id: currentUser.id,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        // Update the booked events list
        // Trigger a page refresh
        setRefreshPage(true);
      })
      .catch((error) => {
        console.error('Error booking event:', error);
      });
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (refreshPage) {
    setRefreshPage(false);
    window.location.reload();
  }

  return (
    <div className="container mt-4">
      <div className="row">
        {events.map((event) => (
          <div key={event.id} className="col-md-4 mb-4">
            <div className="card">
              <Link to={`/events/${event.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                <div className="card-header">
                  <h5 className="card-title">{event.title}</h5>
                </div>
              </Link>
              <img src={event.image_url} className="card-img-top" alt={event.title} width="400px" height="200px" />
              <div className="card-body">
                <p className="card-text">{event.description}</p>
                <p className="card-text">Start Time: {event.start_time}</p>
                <p className="card-text">End Time: {event.end_time}</p>
                {/* Button to book the event */}
                
                  <button onClick={() => bookEvent(event.id)} className="btn btn-primary">
                    Book Event
                  </button>
                
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventList;
