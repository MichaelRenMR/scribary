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
  const [ currentTag, setCurrentTag ] = useState(""); 
  const tags = ['Health', 'Games', 'News', 'Science', 'Sports']

  const requestOptions = {
    method : 'GET',
  }

  const parse_tags = (obj) => {
    obj.forEach(item => {
      item['tags'] = JSON.parse(item['tags']);
    });
  }

  const fetchData = (setData) => {
    fetch('/fetch', requestOptions)
      .then(response => response.json())
      .then(data => {
        parse_tags(data);
        setData(data);
      });
  }

  fetchData(setData);

  let filteredData = data.filter((item) => {
    return currentTag === "" || (item['tags'].hasOwnProperty(currentTag) && item['tags'][currentTag] >= 0.5); 
  });

  const reset = () => {
    setCurrentTag("");
  }

  return (
    <div className="outer-container overflow-auto">
      <div className="row">
        <div id="welcome">
          Scribary
        </div>
      </div>
      <div className = "row mx-3">
        <div className="btn-group tagButtons" style={{"margin-bottom": "20px"}}>
          {tags.map(tag => {
            return (
              <button type="button" className="btn btn-info tag-button" onClick={() => setCurrentTag(tag)}>{tag}</button>
            );
          })}
          <button className="btn mx-2 btn-danger tag-button" onClick={reset}>Reset filters</button>
        </div>
      </div>
      <div className="row">
        <div className="card-columns">
          {filteredData.map(item => {
              return (
                <Post
                 setCurrentTag={(tag) => setCurrentTag(tag)}
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
