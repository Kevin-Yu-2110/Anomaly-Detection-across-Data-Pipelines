import React from "react";
import styled, { keyframes } from "styled-components";

const LoadingSpinner = () => {
  const rotate360 = keyframes`
    from {
      transform: rotate(0deg);
    }

    to {
      transform: rotate(360deg);
    }
  `;

  const Spinner = styled.div`
    margin: auto;
    animation: ${rotate360} 1s linear infinite;
    transform: translateZ(0);
    border-top: 2px solid white;
    border-right: 2px solid white;
    border-bottom: 2px solid white;
    border-left: 4px solid black;
    background: transparent;
    width: 100px;
    height: 100px;
    border-radius: 50%;
  `;

  return (
    <div style={{ padding: "50px" }}>
		  <Spinner />
      <div style={{ textAlign: "center", paddingTop: "10px", fontSize: "150%", fontWeight: "bold" }}>Loading...</div>
	  </div>
  )
}

export default LoadingSpinner;
