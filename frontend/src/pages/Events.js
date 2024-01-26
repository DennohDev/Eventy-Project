import React from 'react'
import EventList from '../components/EventCard'
import BookedEventList from '../components/BookedEvents'

function Events() {
  return (
    <div>
      <h2 className='text-center mt-5'>Select an Event to Attend</h2>
      <EventList/>
      <h2 className='text-center mt-5'>Booked Events</h2>
      <BookedEventList/>
    </div>
  )
}

export default Events