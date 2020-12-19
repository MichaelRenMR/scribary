import React from "react";
import { Link } from "react-router-dom";
import PDFViewer from "./PDFViewer"

const Post = props => {
  const { title, school, course, description, fileurl, tags } = props.data;
  return (
    <a href={fileurl} target="_blank" className="pdf-anchor card rec-card">
      <div className="">
        <h5 class="card-header">{school} - {course}</h5>
        <h3 class="card-title">{title}</h3>
        <div class="card-text">
          {description}
        </div>
        <div className="d-flex justify-content-center pdf-preview">
          <PDFViewer
            pdfURL={fileurl}
          />
        </div>
      </div>
    </a>
  )
}

export default Post;
