import React from "react";
import style from './menu.module.css';

function Menu() {

    return (
        <nav id={style.bigContainer}>
        <ul id={style.smallContainer}>
          <li className={style.elementC}><a className={style.elementS} href="/">Home</a></li>
          <li className={style.elementC}><a className={style.elementS} href="/login">Sign In</a></li>
          <li className={style.elementC}><a className={style.elementS} href="/signup">Sign Up</a></li>
          <li className={style.elementC}><a className={style.elementS} href="/resetRequest">Reset Password</a></li>
          <li className={style.elementC}><a className={style.elementS} href="#">About us</a></li>
        </ul>
      </nav>
    );
}

export default Menu;