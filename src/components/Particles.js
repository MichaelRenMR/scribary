import Particles from 'react-particles-js';
import React from 'react';

const BGParticles = props => {
  return (
    <Particles
        params={{
            "particles": {
                "number": {
                    "value": 160,
                    "density": {
                        "enable": false
                    }
                },
                "size": {
                    "value": 10,
                    "random": true
                },
                "move": {
                    "direction": "bottom",
                    "out_mode": "out"
                },
                "line_linked": {
                    "enable": false
                }
            },
            "interactivity": {
                "events": {
                    "onclick": {
                        "enable": true,
                        "mode": "remove"
                    }
                },
                "modes": {
                    "remove": {
                        "particles_nb": 10
                    }
                }
            }
        }}
    style={{
      width: '100%',
      height: '100%',
      left: 0,
      top: 0,
      position: "absolute",
      zIndex: -1,
    }}
    />
  )
}

export default BGParticles;
