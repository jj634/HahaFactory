import React from 'react';
import axios from 'axios';

// css files 
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/main.css';
import './css/App.css';

// images, lists
import logo from './images/operator.png';

// components
import Form from './components/Form'
import JokeResults from './components/JokeResults';

import { Row, Col } from 'react-bootstrap'
import { Dimmer, Loader, Container, Button } from 'semantic-ui-react'

class App extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    console.log("APP Render")
      return (
        <div>
          <div >
            <Button style={{ margin: '10px' }} onClick={() => window.open("http://hahafactory-og.herokuapp.com/", "_blank")}> First Prototype </Button>
            <Button style={{ margin: '10px' }} onClick={() => window.open("http://hahafactory-v2.herokuapp.com/", "_blank")}> Second Prototype </Button>
          </div>
          <div style={{ alignItems: 'center', justify: 'center', maxWidth: '50%', left: '25%', position: 'absolute' }}>
            <Container>
              <Row className="justify-content-md-center">
                <Col>
                  <header className="App-header">
                    <h1>HahaFactory:</h1>
                    <h2>Finding Hilarious Jokes for You</h2>
                    <img src={logo} className="App-logo" alt="logo" />
                  </header>
                  <Form/> 
                </Col>
              </Row>
              <Row>
                <Col className="jokes-col">
                  <JokeResults />   
                </Col>
              </Row>
            </Container >
          </div>
        </div>
      )
  }
}

export default App;