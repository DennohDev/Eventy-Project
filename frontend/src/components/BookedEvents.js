// EventList.js
import React from 'react';
import { useEvents } from '../context/EventsContext';
import { Link } from 'react-router-dom';

const BookedEventList = () => {
  const { booked, loading } = useEvents([]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mt-4">
      <div className="row">
        {booked && booked.map(event => (
          <div key={event.id} className="col-md-4 mb-4">
            <div className="card">
              <Link to={`/events/${event.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                {/* Clickable title */}
                <div className="card-header">
                  <h5 className="card-title">{event.title}</h5>
                </div>
              </Link>
                <img src={event.image_url} className="card-img-top" alt={event.title} width="400px" height="200px" />
                <div className="card-body">
                  <p className="card-text">{event.description}</p>
                  <p className="card-text">Start Time: {event.start_time}</p>
                  <p className="card-text">End Time: {event.end_time}</p>
                </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BookedEventList;
