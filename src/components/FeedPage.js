import React from "react";
import Feed from "./Feed";

const FeedPage = props => {
  return (
    <div className="container">
      <div className="h-100 row">
        <div className="col-2" />
        <div className="col d-flex align-items-center">
          <Feed />
        </div>
        <div className="col-2" />
      </div>
    </div>
  )
}

export default FeedPage;
