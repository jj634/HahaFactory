// adapted from: https://pusher.com/tutorials/consume-restful-api-react

import React from 'react'
import { Icon, Label, Popup, Button } from 'semantic-ui-react'
import Highlighter from "react-highlight-words";
import Rating from '@material-ui/lab/Rating';


const JokeResults = ({ jokes, query }) => {
  if (jokes.length === 0) {
    return (
      <React.Fragment>
      </React.Fragment>
    )
  }
  return (
    <React.Fragment>
      <center><h2>Jokes</h2></center>
      {jokes.map((joke, index) => (
        (index <= 20) ?
        <div>
        <div className="card">
          <div className="card-body">
            {joke.text.split('\n').map((item, i) => <h5 key={i}> <Highlighter
              highlightClassName="Highlight"
              searchWords={query}
              autoEscape={true}
              textToHighlight={item}
            /></h5>)}
            
              {joke.categories.map((cat) => <Label>
                {cat}
              </Label>)}
              <div>
              <Popup content={joke.score} position='right center' trigger={
                <h6 className="doughnut">Joke Rating: 
                  <Rating className="rating_stars" name="half-rating-read" defaultValue={joke.score} precision={0.05} readOnly />
                </h6>
              }/>
              </div>
              
              <Popup position='right center' trigger={<h6 className="sim_sc_display">Similarity Score: {joke.similarity}</h6>}>
                <Popup.Header>Here are the details!</Popup.Header>
                  <Popup.Content>
                    <h6 className="doughnut">Keywords Weight (cosine): {joke.cos_score}</h6>
                    <h6 className="doughnut">Categories Weight (jaccard): {joke.jac_score}</h6>
                    <h6 className="doughnut">Score Weight: {joke.sc_score}</h6>
                  </Popup.Content>
              </Popup>
          </div>
        </div>
        <br></br>
        </div> : null
      ))}
    </React.Fragment>
  )
};

export default JokeResults