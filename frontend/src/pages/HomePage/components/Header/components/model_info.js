import React, { useState } from "react";
import { Button, ListGroup, ListGroupItem, Modal, Tab, Tabs } from "react-bootstrap";
import { BsInfoCircle } from "react-icons/bs";
import style from "../header.module.css";

const ModelInfo = () => {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <Button variant="outline-info" onClick={handleShow}>
        <BsInfoCircle className={style.icon}></BsInfoCircle>
        Model Info
      </Button>

      {/** popup that shows info about each implemented model */}
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Model Performance</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Tabs
            defaultActiveKey="XG"
            className="mb-3"
          >
            <Tab eventKey="XG" title="XGBoost">
              <ListGroup>
                <ListGroupItem>Gradient boosted ensemble model using decision trees</ListGroupItem>
                <ListGroupItem>Prediction using probabilities</ListGroupItem>
                <ListGroupItem variant="success">Best performance in general</ListGroupItem>
                <ListGroupItem variant="success">Fast training speed: 15-20s</ListGroupItem>
                <ListGroupItem variant="primary">
                  Test Performance:
                  <div>- Recall: 78%</div>
                  <div>- Precision: 82%</div>
                </ListGroupItem>
              </ListGroup>
            </Tab>
            <Tab eventKey="IF" title="Isolation Forest">
              <ListGroup>
                <ListGroupItem>Unsupervised Tree Based Model</ListGroupItem>
                <ListGroupItem>Better for detecting anomalies in unseen data</ListGroupItem>
                <ListGroupItem>Prediction using outlier detection</ListGroupItem>
                <ListGroupItem variant="success">The 'safest' model - least likely to miss an anomaly</ListGroupItem>
                <ListGroupItem variant="success">Fast training speed: 25-30s</ListGroupItem>
                <ListGroupItem variant="primary">
                  Test Performance:
                  <div>- Recall: 90%</div>
                  <div>- Precision: 60%</div>
                </ListGroupItem>
              </ListGroup>
            </Tab>
            <Tab eventKey="NN" title="Neural Network">
              <ListGroup>
                <ListGroupItem>Neural Network with 5 hidden layers</ListGroupItem>
                <ListGroupItem>Prediction using multiple layers and validation</ListGroupItem>
                <ListGroupItem variant="success">The 'most conservative' model - makes safest predictions</ListGroupItem>
                <ListGroupItem variant="danger">Slow training speed: 3-5mins</ListGroupItem>
                <ListGroupItem variant="primary">
                  Test Performance:
                  <div>- Recall: 61%</div>
                  <div>- Precision: 90%</div>
                </ListGroupItem>
              </ListGroup>
            </Tab>
          </Tabs>
        </Modal.Body>
      </Modal>
    </>
  )
}

export default ModelInfo;
