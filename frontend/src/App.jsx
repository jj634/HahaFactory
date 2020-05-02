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
      typo: false, 
      typo_query: '',

      categories: [],
      score: '',
      search: '', 
      sizes: [],    
      maturity: ''
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
    const size_param = URLParams.getAll("sizes")
    const maturity_param = URLParams.get("maturity")

    axios({
      method: 'GET',
      // url: `/api/search`,
      url: `http://localhost:5000/api/search`,
      params: URLParams
    })
      .then((response) => {
        this.setState({
          isLoaded: true,
          jokes: response.data.jokes,
          typo: response.data.typo, 
          typo_query: response.data.typo_query,

          categories: category_param,
          score: score_param,
          search: search_param, 
          sizes: size_param,
          maturity: maturity_param
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
    const size_param = URLParams.getAll("sizes")
    const maturity_param = URLParams.get("maturity")

    const cat_updated = category_param.sort().toString() !== (prevState.categories).sort().toString()
    const size_updated = size_param.sort().toString() !== (prevState.sizes).sort().toString()
    return cat_updated || score_param !== prevState.score || search_param !== prevState.search || size_updated || maturity_param !== prevState.maturity
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
              <h1>HahaFactory:</h1>
              <h2>Finding Hilarious Jokes for You</h2>
              <img src={logo} className="App-logo" alt="logo" />
            </header>

          <Form score = {this.state.score} categories = {this.state.categories} search = {this.state.search} sizes = {this.state.sizes} maturity = {this.state.maturity}/>

          </Col>
        </Row>
        <Row>
          <Col className="jokes-col">
            {this.state.typo & this.state.typo_query === ''
              ? <div>
                <h4> We could not find any results for <b>"{this.state.search}"</b>.</h4>
              </div>
              : null}
             {this.state.typo & this.state.typo_query !=='' 
               ? <div> 
                <h4> Did you mean... <b>"{this.state.typo_query}"</b>? </h4>
                <h4> We are showing results for <b>"{this.state.typo_query}"</b>.</h4>
                </div>
               : null}
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