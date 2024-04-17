import React from 'react';
import style from './coverstyle.module.css';
import video from './assets/background1.mp4';
import Menu from './menu'

function Cover() {

  return (
    <div className={style.bigContainer}>
        <video src={video} autoPlay loop muted />
        <div className={style.container}>
            <Menu/>
            <h1>Anomaly Detection across Data Pipelines</h1>
            <a className={style.link} href="/login">Start Now</a>
        </div>
    </div>
  );
}

export default Cover;