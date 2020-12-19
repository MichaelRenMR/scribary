import React from "react";
import axios from "axios";
import { Button, Form } from "react-bootstrap";

const handleSubmit = async event => {
  const data = new FormData();

  const title = event.target[0].value;
  const school = event.target[1].value;
  const cid = event.target[2].value;
  const desc = event.target[3].value;
  const file = event.target[4].files[0];

  console.log(title, school, cid)
  console.log(file)

  data.append('title', title)
  data.append('school', school)
  data.append('cid', cid)
  data.append('desc', desc)
  data.append('file', file)

  const requestOptions = {
    method : 'POST',
    body: data
  }

  fetch('/upload', requestOptions)
    .then(res => console.log(res))

  event.preventDefault();
  event.stopPropagation();
}

const Upload = (props) => {
  return (
    <div>
      <Form onSubmit={handleSubmit} >
        <Form.Group controlId="exampleForm.ControlInput1">
          <Form.Label>Title</Form.Label>
          <Form.Control type="text" placeholder="name@example.com" />
        </Form.Group>
        <Form.Group controlId="exampleForm.ControlInput1">
          <Form.Label>School</Form.Label>
          <Form.Control type="text" placeholder="name@example.com" />
        </Form.Group>
        <Form.Group controlId="exampleForm.ControlInput1">
          <Form.Label>Course ID</Form.Label>
          <Form.Control type="text" placeholder="name@example.com" />
        </Form.Group>
        <Form.Group controlId="exampleForm.ControlTextarea1">
          <Form.Label>Description</Form.Label>
          <Form.Control as="textarea" rows={3} />
        </Form.Group>
        <Form.Group controlId="exampleForm.ControlTextarea1">
          <Form.Label>Upload your notes PDF</Form.Label>
          <Form.File
              id="custom-file"
              label="Custom file input"
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
