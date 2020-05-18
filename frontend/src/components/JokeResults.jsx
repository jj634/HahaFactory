// adapted from: https://pusher.com/tutorials/consume-restful-api-react

import React from 'react'
import axios from 'axios';
import { withRouter } from "react-router";

import { Segment, Loader, Dimmer, Label, Popup} from 'semantic-ui-react'
import Highlighter from "react-highlight-words";
import Rating from '@material-ui/lab/Rating';

import PiChart from './PiChart'

class JokeResults extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      isLoaded: false,
      jokes: [],
      typo: false,
      typo_query: '',
      query: [],

      categories: [],
      score: '',
      search: '',
      sizes: [],
      maturity: '',
      URLParam: null,
    }
  }

  componentDidMount() {
    this.fetchResults()
  }

  fetchResults() {
    const URLParams = new URLSearchParams(this.props.location.search)
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
          query: response.data.query,

          categories: category_param,
          score: score_param,
          search: search_param,
          sizes: size_param,
          maturity: maturity_param,
          URLParam: URLParams
        })
      })
      .catch(err =>
        console.log(err)
      );
  }

  static getDerivedStateFromProps(nextProps, prevState) {
    const newURLParams = new URLSearchParams(nextProps.location.search)
    const oldURLParams = prevState.URLParam || new URLSearchParams()
    newURLParams.sort()
    oldURLParams.sort()
    const new_URL = newURLParams.toString()
    const old_URL = oldURLParams.toString()

    return new_URL !== old_URL
      ? { isLoaded: false }
      : null
  }

  componentDidUpdate(prevProps) {
    if (this.state.isLoaded === false) {
      this.fetchResults();
    }
  }


  render() {
    const {jokes, typo, typo_query, query, search} = this.state
    if (this.state.isLoaded) return ( 
      <div>
        {
          typo & typo_query === ''
          ? <div>
            <h4> We could not find any results for <b>"{search}"</b>.</h4>
          </div>
          : null
        }
        {
          typo & typo_query !== ''
          ? <div>
            <h4> Did you mean... <b>"{typo_query}"</b>? </h4>
            <h4> We are showing results for <b>"{typo_query}"</b>.</h4>
          </div>
          : null
        }
        {jokes.map((joke, index) => (
          (index <= 20) 
          ?<div key = {index}>
            <div className="card">
              <div className="card-body">
                {joke.text.split('\n').map((item, i) => 
                  <h5 key={i}> 
                    <Highlighter
                      highlightClassName="Highlight"
                      searchWords={query}
                      autoEscape={true}
                      textToHighlight={item}/>
                  </h5>)}
                {joke.categories.map((cat, i) => 
                  <Label key = {i}>
                    {cat}
                  </Label>
                )}
              <div>

              <Popup content={joke.score} position='right center' trigger={
                <h6 className="star_hover">
                  <Rating className="rating_stars" name="half-rating-read" defaultValue={parseFloat(joke.score)} precision={0.1} readOnly />
                </h6>
              }/>

              </div>
                <h6 className="sim_sc_display">Similarity Score: {Number((Number(joke.similarity)*100).toFixed(1))+ "%"}</h6>
                <PiChart cos_score = {joke.cos_score} jac_score = {joke.jac_score} sc_score = {joke.sc_score} similarity = {joke.similarity} /> 
              </div>
            </div>
          <br></br>
          </div> 
        : null
        ))}
      </div>
    )
    else return null
  }
}

export default withRouter(JokeResults);