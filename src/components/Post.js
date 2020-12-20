import React from "react";
import { Link } from "react-router-dom";
import PDFViewer from "./PDFViewer";
import Tags from "./Tags";

const Post = props => {
  const { title, school, courseid, desc, file_url, tags, hash, setCurrentTag } = props.data;
  const base = "https://hackumass2020.s3-us-west-1.amazonaws.com/"
  const aws_url = base + hash + ".pdf";  // file_url = hackumass2020/hash.pdf

  const sortedTags = () => {
    let sortable = [];
    for (let item in tags) {
      sortable.push([item, tags[item]]);
    }

    sortable.sort(function(a, b) {
      return b[1] - a[1];
    });
    return sortable;
  }

  let taglist = sortedTags().filter(item => item[1] >= 0.5);

  return (
    <div className="card rec-card">
      <div className="">
        <h5 className="card-header">{school} - {courseid}</h5>
        <h3 className="card-title">{title}</h3>
        <div className="card-text">
          {desc}
        </div>
        <a href={aws_url} target="_blank" className="pdf-anchor d-flex justify-content-center pdf-preview">
          <PDFViewer
            pdfURL={aws_url}
          />
        </a>
        <div className="card-text">
          <Tags 
            setCurrentTag={(tag) => setCurrentTag(tag)}
            taglist={taglist} 
          />
        </div>
      </div>
    </div>
  )
}

export default Post;
