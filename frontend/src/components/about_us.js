import React from 'react';
import style from './aboutus.module.css'
import Menu from './menu'

function About () {
    return (
        <div className={style.largeContainer}>
            <Menu />
            <div className={style.container}></div>
            <div className={style.text}>
                <h2>Background</h2>
                <div>Understanding and analyzing big data is a daunting task that can be seen as expensive, foreign, and time-consuming by data users. Especially when those data-users may not have complete visibility in data transformations and may therefore lack the ability to contextualize and analyze those data outputs. By developing an intuitive user interface that allows users to detect anomalies across the data transformation process, this project aims to increase the accessibility for data users to highlight irregularities in the context of financial transactions, such as financial fraud detection.</div>
                <h2>Target</h2>
                <ul>
                    <li>Create data pipeline from data source</li>
                    <li>ML mechanism to determine key stages in the data pipeline that have high potential for creating anomalies</li>
                    <li>ML anomaly detection model for each key stage of the data pipeline</li>
                    <li>Allows users to run selected anomaly detection on a selected data pipeline</li>
                    <li>Interface clearly show the anomalies that were observed</li>
                    <li>User should get alert when the anomalies appear in real time and get relevant information of the anomalies</li>
                    <li>Allows users to accept or ignore anomalies and provide feedback to the ML application</li>
                    <li>Allows users to train / retrain a model for a data pipeline</li>
                    <li>Allows new users to signup and create a secure account</li>
                    <li>Allows users to sign in and sign out of their created account</li>
                    <li>Allows users to reset their password</li>
                    <li>Provides customisation for users based on preferences</li>
                </ul>
                <h2>Members</h2>
                <ul>
                    <li>Yuchi Zhang, z5359871@ad.unsw.edu.au, z5359871, ML, scrum master</li>
                    <li>Rory Maclean, z5363662@ad.unsw.edu.au, z5363662, backend, scrum team</li>
                    <li>Henry Bojia Zhang, z5363805@ad.unsw.edu.au, z5363805, ML, scrum team</li>
                    <li>Zhou Yu, z5371570@ad.unsw.edu.au, z5371570, backend, scrum team</li>
                    <li>Junkai Wu, z5237250@ad.UNSW.edu.au, z5237250, frontend, scrum team</li>
                    <li>Jason Guo, z5114601@ad.unsw.edu.au, z5114601, frontend, scrum team</li>
                </ul>
            </div>
        </div>
    );
}

export default About;