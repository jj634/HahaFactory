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
import { Dimmer, Loader, Container} from 'semantic-ui-react'

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      isLoaded: false,
      jokes: [],

      categories: [],
      score: '',
      search: '', 
      length: ''    
    }
  }

  componentDidMount() {
    this.fetchResults()
  }

  fetchResults(){ 
    const URLParams = new URLSearchParams(window.location.search)

    const category_param = URLParams.getAll("categories")
    const score_param = URLParams.get("score")
    const search_param = URLParams.get("search")
    const size_param = URLParams.get("size")

    axios({
      method: 'GET',
      url: `http://localhost:5000/api/search`,
      params: URLParams
    })
      .then((response) => {
        this.setState({
          isLoaded: true,
          jokes: response.data.jokes,

          categories: category_param,
          score: score_param,
          search: search_param, 
          size: size_param
        })
      })
      .catch(err =>
        console.log(err)
      );
  }

  static getDerivedStateFromProps(nextProps, prevState) {
    const URLParams = new URLSearchParams(nextProps.location.search)

    const category_param = URLParams.getAll("categories")
    const score_param = URLParams.get("score")
    const search_param = URLParams.get("search")
    const size_param = URLParams.get("size")

    const cat_updated = category_param.sort().toString() !== (prevState.categories).sort().toString()
    return cat_updated || score_param !== prevState.score || search_param !== prevState.search || size_param !== prevState.size
      ? { isLoaded: false }
      : null
  }

  componentDidUpdate(prevProps) {
    if (this.state.isLoaded === false) {
      this.fetchResults();
    }
  }

  render() {
    if (this.state.isLoaded) {return (
      <Container>
        <Row className="justify-content-md-center">
          <Col>
            <header className="App-header">
              <h1>HahaFactory</h1>
              <img src={logo} className="App-logo" alt="logo" />
            </header>

          <Form score = {this.state.score} categories = {this.state.categories} search = {this.state.search} size = {this.state.size}/>

          </Col>
        </Row>
        <Row>
          <Col className="jokes-col">
             <JokeResults jokes={this.state.jokes}/>
          </Col>
        </Row>
      </Container >
      )
   }
   else return (
      <Dimmer active inverted>
        <Loader size="large" >Loading</Loader>
      </Dimmer>
      )
   }
}

export default App;