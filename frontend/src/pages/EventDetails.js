// EventDetails.js
import React from 'react';
import { useParams } from 'react-router-dom';
import { useEvents } from '../context/EventsContext';

const EventDetails = () => {
  const { id } = useParams();
  const { events } = useEvents();

  // Find the event with the matching id
  const event = events.find(e => e.id.toString() === id);

  if (!event) {
    return <div>Event not found</div>;
  }

  return (
    <div className="container mt-4">
      <div className="card">
        <img src={event.image_url} className="card-img-top" alt={event.title} />
        <div className="card-body">
          <h5 className="card-title">{event.title}</h5>
          <p className="card-text">{event.description}</p>
          <p className="card-text">Start Time: {event.start_time}</p>
          <p className="card-text">End Time: {event.end_time}</p>
          {/* Add more details as needed */}
        </div>
      </div>
    </div>
  );
};

export default EventDetails;
