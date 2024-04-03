import React from 'react';
import video from './assets/background1.mp4'

const VideoComponent = () => {
  return (
    <div>
      <video autoPlay loop muted>
        <source src={video} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default VideoComponent