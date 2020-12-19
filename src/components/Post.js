import React from "react";
import PDFViewer from "./PDFViewer"

const Post = props => {
  let data = props.data;
  let defaultImage = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fdominionmartialarts.com%2Fhome%2Fdefault-image%2F&psig=AOvVaw0ll0Q0ZavJkg5DUzRdpmFa&ust=1608433613595000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCNDX0aOI2e0CFQAAAAAdAAAAABAD"
  return (
    <div className="card rec-card">
      <div className="">
        <h5 class="card-title">{data.title}</h5>
        <div className="d-flex justify-content-center pdf-preview">
          <PDFViewer
            pdfURL={data.pdfURL}
          />
        </div>
      </div>
    </div>
  )
}

export default Post;
