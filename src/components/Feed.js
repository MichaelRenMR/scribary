import React, { useState } from "react";
import Post from "./Post";

// const dummy_data = [
//   {
//     title: "Notes from CS220",
//     school: "UMass Amherst",
//     course: "CS220",
//     description: "Notes from my poggers course, I took it with Marius and Jaime in F20 and they may have changed the course material since",
//     file_url: "https://hackumass2020.s3-us-west-1.amazonaws.com/9db3b66632f250efbd61ad43130cf966.pdf",
//     tags: [{
//       tagname: "computer science",
//       confidence: 1
//     }]
//   },
//   {
//     title: "Notes from CS220",
//     school: "UMass Amherst",
//     course: "CS220",
//     description: "Notes from my poggers course",
//     file_url: "https://hackumass2020.s3-us-west-1.amazonaws.com/9db3b66632f250efbd61ad43130cf966.pdf",
//     tags: [{
//       tagname: "computer science",
//       confidence: 1
//     }]
//   },
//   {
//     title: "Notes from CS220",
//     school: "UMass Amherst",
//     course: "CS220",
//     description: "Notes from my poggers course",
//     file_url: "https://hackumass2020.s3-us-west-1.amazonaws.com/9db3b66632f250efbd61ad43130cf966.pdf",
//     tags: [{
//       tagname: "computer science",
//       confidence: 1
//     }]
//   },
//   {
//     title: "Notes from CS220",
//     school: "UMass Amherst",
//     course: "CS220",
//     description: "Notes from my poggers course",
//     file_url: "https://hackumass2020.s3-us-west-1.amazonaws.com/9db3b66632f250efbd61ad43130cf966.pdf",
//     tags: [{
//       tagname: "computer science",
//       confidence: 1
//     }]
//   },
//   {
//     title: "Notes from CS220",
//     school: "UMass Amherst",
//     course: "CS220",
//     description: "Notes from my poggers course",
//     file_url: "https://hackumass2020.s3-us-west-1.amazonaws.com/9db3b66632f250efbd61ad43130cf966.pdf",
//     tags: [{
//       tagname: "computer science",
//       confidence: 1
//     }]
//   },
// ]


const Feed = props => {

  const [ data, setData ] = useState([]);

  const requestOptions = {
    method : 'GET',
  }

  const fetchData = (setData) => {
    fetch('/fetch', requestOptions)
      .then(response => response.json())
      .then(data => setData(data));
  }

  fetchData(setData);

  return (
    <div className="outer-container overflow-auto">
      <div className="row">
        <div className="card-columns">
          {data.map(item => {
              return (
                <Post
                 data={item}
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
