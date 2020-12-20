import React from "react";
import { Button } from "react-bootstrap";

const Tags = props => {
  const { taglist } = props;
  return (
    <div className="btn-toolbar">
      Tags:
      {taglist.map(tag => {
        return (
          <div className="mx-2 tag btn-link">
            {tag[0]}
          </div>
        );
      })}
    </div>
  );
}

export default Tags;
