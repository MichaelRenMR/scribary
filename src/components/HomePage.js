import React from "react";
import { Link } from "react-router-dom";
import Upload from "./Upload"
import { Button } from "react-bootstrap";
import BGParticles from "./Particles";
import Logo from "../Assets/logo.png"

const HomePage = props => {
  return (
    <div>
      <div className="container">
        <div className="home-page h-100 row">
          <div className="col-3" />
          <div className="col-6 d-flex align-items-center">
            <div className="card home-container">
              <div id="welcome">
                Scribary
              </div>
              <p className="description p-4 text-sm-left">
                Having trouble attending synchronous lectures due to time zone problems? Looking for some notes for your remote courses?
              </p>
              <img className="logo mx-auto" src={Logo} alt="" />
              <p className="description p-3 text-sm-center">
                Check out a set of notes out at your local Scribary!
              </p>
              <div>
                <Link className="btn mx-2 btn-info" to="/submit">Submit your notes!</Link>
                <Link className="btn mx-2 btn-danger" to="/notes">Browse notes!</Link>
              </div>
            </div>
          </div>
          <div className="col-3" />
        </div>
      </div>
      <BGParticles />
    </div>
  )
}

export default HomePage;
