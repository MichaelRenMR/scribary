import React, { useState } from "react";
import axios from "axios";
import bsCustomFileInput from "bs-custom-file-input"
import { Button, Form } from "react-bootstrap";


const Upload = (props) => {
  const [filename, setFilename] = useState("");
  const [title, setTitle] = useState("");
  const [school, setSchool] = useState("");
  const [course, setCourse] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = async event => {
    const data = new FormData();

    const dataTitle = event.target[0].value;
    const dataSchool = event.target[1].value;
    const dataCourse = event.target[2].value;
    const dataDescription = event.target[3].value;
    const dataFile = event.target[4].files[0];

    data.append('title', dataTitle)
    data.append('school', dataSchool)
    data.append('course', dataCourse)
    data.append('description', dataDescription)
    data.append('file', dataFile)

    const requestOptions = {
      method : 'POST',
      body: data
    }

    setFilename("");
    setTitle("");
    setSchool("");
    setCourse("");
    setDescription("");

  fetch('/upload', requestOptions)
    .then(res => console.log(res))

  event.preventDefault();
  event.stopPropagation();
}
  return (
    <div>
      <Form onSubmit={handleSubmit} >
        <Form.Group controlId="exampleForm.ControlInput1">
          <Form.Label>Title</Form.Label>
          <Form.Control
            type="text"
            placeholder="Intro to Discrete Math notes"
            value={title}
            onChange={e => setTitle(e.target.value)}
          />
        </Form.Group>
        <Form.Group controlId="exampleForm.ControlInput1">
          <Form.Label>School</Form.Label>
          <Form.Control
            type="text"
            placeholder="UMass Amherst"
            value={school}
            onChange={e => setSchool(e.target.value)}
          />
        </Form.Group>
        <Form.Group controlId="exampleForm.ControlInput1">
          <Form.Label>Course ID</Form.Label>
          <Form.Control
            type="text"
            placeholder="CS250"
            value={course}
            onChange={e => setCourse(e.target.value)}
          />
        </Form.Group>
        <Form.Group controlId="exampleForm.ControlTextarea1">
          <Form.Label>Description</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            value={description}
            onChange={e => setDescription(e.target.value)}
          />
        </Form.Group>
        <Form.Group controlId="exampleForm.ControlTextarea1">
          <Form.Label>Upload your PDF notes</Form.Label>
          <Form.File
              id="custom-file"
              label={filename}
              onChange={e => setFilename(e.target.files[0].name)}
              custom
            />
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </div>
  )
}

export default Upload;
