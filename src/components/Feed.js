import React from "react";
import Post from "./Post";

const dummy_data = [
  {
    title: "Notes from CS220",
    school: "UMass Amherst",
    course: "CS220",
    description: "Notes from my poggers course, I took it with Marius and Jaime in F20 and they may have changed the course material since",
    fileurl: "https://vadimdez.github.io/ng2-pdf-viewer/assets/pdf-test.pdf",
    tags: [{
      tagname: "computer science",
      confidence: 1
    }]
  },
  {
    title: "Notes from CS220",
    school: "UMass Amherst",
    course: "CS220",
    description: "Notes from my poggers course",
    fileurl: "https://vadimdez.github.io/ng2-pdf-viewer/assets/pdf-test.pdf",
    tags: [{
      tagname: "computer science",
      confidence: 1
    }]
  },
  {
    title: "Notes from CS220",
    school: "UMass Amherst",
    course: "CS220",
    description: "Notes from my poggers course",
    fileurl: "https://vadimdez.github.io/ng2-pdf-viewer/assets/pdf-test.pdf",
    tags: [{
      tagname: "computer science",
      confidence: 1
    }]
  },
  {
    title: "Notes from CS220",
    school: "UMass Amherst",
    course: "CS220",
    description: "Notes from my poggers course",
    fileurl: "https://vadimdez.github.io/ng2-pdf-viewer/assets/pdf-test.pdf",
    tags: [{
      tagname: "computer science",
      confidence: 1
    }]
  },
  {
    title: "Notes from CS220",
    school: "UMass Amherst",
    course: "CS220",
    description: "Notes from my poggers course",
    fileurl: "https://vadimdez.github.io/ng2-pdf-viewer/assets/pdf-test.pdf",
    tags: [{
      tagname: "computer science",
      confidence: 1
    }]
  },
]

const Feed = props => {
  return (
    <div className="outer-container overflow-auto">
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
