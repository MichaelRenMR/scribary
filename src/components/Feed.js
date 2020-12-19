import React from "react";
import Post from "./Post";

const dummy_data = [
  {
    title: "Notes from CS220",
    school: "UMass Amherst",
    course: "CS220",
    description: "Notes from my poggers course",
    pdfURL: "https://vadimdez.github.io/ng2-pdf-viewer/assets/pdf-test.pdf"
  },
  {
    title: "Notes from CS220",
    school: "UMass Amherst",
    course: "CS220",
    description: "Notes from my poggers course",
    pdfURL: "https://vadimdez.github.io/ng2-pdf-viewer/assets/pdf-test.pdf"
  },
  {
    title: "Notes from CS220",
    school: "UMass Amherst",
    course: "CS220",
    description: "Notes from my poggers course",
    pdfURL: "https://vadimdez.github.io/ng2-pdf-viewer/assets/pdf-test.pdf"
  },
  {
    title: "Notes from CS220",
    school: "UMass Amherst",
    course: "CS220",
    description: "Notes from my poggers course",
    pdfURL: "https://vadimdez.github.io/ng2-pdf-viewer/assets/pdf-test.pdf"
  },
  {
    title: "Notes from CS220",
    school: "UMass Amherst",
    course: "CS220",
    description: "Notes from my poggers course",
    pdfURL: "https://vadimdez.github.io/ng2-pdf-viewer/assets/pdf-test.pdf"
  },
]

const Feed = props => {
  return (
    <div className="outer-container">
      <div className="row">
        <div className="card-columns">
          {dummy_data.map(data => {
              return (
                <Post
                 data={data}
                />
              );
            }
          )}
        </div>
      </div>
    </div>
  );
}

export default Feed;
