// adapted from: https://pusher.com/tutorials/consume-restful-api-react

import React from 'react'
import axios from 'axios'
import { withRouter } from 'react-router-dom'

import { Icon, Label, Popup} from 'semantic-ui-react'
import Highlighter from "react-highlight-words";
import Rating from '@material-ui/lab/Rating';
import { Doughnut } from 'react-chartjs-2';
import PiChart from './PiChart'


class JokeResults extends React.Component {
  // constructor(props){
  //   super(props)
  //   this.state = {
  //     isLoaded: false, 
  //     jokes: [], typo: false, 
  //     typo_query: '', 
  //     search_query: '',
  //     query: []
  //   }
  // }
  
  // componentDidMount(){
  //   const URLParams = new URLSearchParams(this.props.location.search)
  //   const search_param = URLParams.get("search")

  //   axios({
  //     method: 'GET',
  //     // url: `/api/search`,
  //     url: `http://localhost:5000/api/search`,
  //     params: URLParams
  //   })
  //     .then((response) => {
  //       this.setState({
  //         isLoaded: true,
  //         jokes: response.data.jokes,
  //         typo: response.data.typo,
  //         typo_query: response.data.typo_query,
  //         search_query: search_param,
  //         query: response.data.query,
  //       })
  //     })
  //     .catch(err =>
  //       console.log(err)
  //     );
  // }

  render() {

    const {jokes, query} = this.props
    if (jokes.length === 0) {
      return (
        <React.Fragment>
        </React.Fragment>
      )
    }
    else
    return (
      <React.Fragment>
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
      </React.Fragment>
    )
  }
}

export default withRouter(JokeResults);