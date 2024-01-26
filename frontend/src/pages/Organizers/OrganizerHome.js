import React, {useState, useEffect} from 'react';
import Swal from 'sweetalert2';
import { useAuth } from '../../context/AuthContext';


export default function OrganizerHome() {

  const [title, setTitle]= useState()
  const [description, setDescription]= useState()
  const [image_url, setImage_url]= useState()
  const [start_time, setStart_time]= useState()
  const [end_time, setEnd_time] = useState()
  const [category_id, setCategory_id] = useState()
  const [organizer_id, setOrganizer_id] = useState()

  const [categories, setCategories] = useState([])

  const { authToken, logout } = useAuth();

  console.log(authToken)
  useEffect(()=>{
    fetch("http://127.0.0.1:5000/authenticated_organizer",{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${authToken}`

      }
    })
    .then(r => r.json())
    .then(data => setOrganizer_id(data.id))


  }, [])
  console.log("id", organizer_id)

  useEffect(() => {
    fetch("http://127.0.0.1:5000/categories")
    .then(r => r.json())
    .then(data => setCategories(data))
  }, [])
  console.log("categories",categories)
 

 // console.log(brand)
  function handleSubmit(e){
    e.preventDefault()
    
    const event0bj={
      title: title,
      description: description,
      image_url: image_url,
      start_time: start_time,
      end_time: end_time,
      category_id: category_id,
      organizer_id: organizer_id,
    }

    fetch("http://127.0.0.1:5000/events", {
      method: "POST",
      headers:{
        "Content-Type" : "application/json",
        "Accept" : "application/json"
      },
      body: JSON.stringify(event0bj)
    })
    .then(r => r.json())
    .then(data => {
      console.log("success")

      Swal.fire({
        position: "center",
        icon: "success",
        title: "Event successfully Uploaded",
        showConfirmButton: false,
        timer: 1500
      });
    })
    .catch((error) =>{
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: "Check your internet connection and try again!"
      });

    })

    setTitle("")
    setDescription("")
    setImage_url("")
    setStart_time("")
    setEnd_time("")
    setCategory_id("")
    setOrganizer_id("")
   
  }


  return (
    <div id="organizerhome" className='container row mt-5 mb-5'>
      <div className='col-md-6'>
        <h1 className='text-danger'>Advertise Here!</h1>
        <p className='text-secondary'>Want to advertise your Event!?, Worry no more! Just fill the form 
          alongside and the event will be advertised</p>
      </div>
      <div className='col-md-6'>
       <form onSubmit={handleSubmit}>
       <div className="mb-3">
                <label className="form-label">Title</label>
                <input type="text" value={title} onChange={e=>setTitle(e.target.value)} className="form-control" required />
            </div>
            <div className="mb-3">
                <label className="form-label">Description</label>
                <input type="text" value={description}  onChange={e=>setDescription(e.target.value)} className="form-control" required />
            </div>
            <div className="mb-3">
                <label className="form-label">Image_url</label>
                <input type="text" value={image_url}  onChange={e=>setImage_url(e.target.value)} className="form-control" required />
            </div>
            <div className="mb-3">
                <label className="form-label">Start Time</label>
                <input type="text" value={start_time}  onChange={e=>setStart_time(e.target.value)} className="form-control" required />
            </div>
            <div className="mb-3">
                <label className="form-label">End Time</label>
                <input type="text" value={end_time}  onChange={e=>setEnd_time(e.target.value)} className="form-control" required />
            </div>
            <div className="mb-3">
                <label className="form-label">Category</label>
                <select
          id="category_id"
          name="category_id"
          value={category_id}
          onChange={(e) => setCategory_id(e.target.value)}
        >
          <option value="">Select a category</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
                
            </div>
          <button type="submit" class="btn btn-success">Submit</button>
       </form>
        <div>
          <button className='btn btn-danger m-5' onClick={()=>logout()}>Logout as an Organizer</button>
        </div>
      </div>

    </div>
  )
}
