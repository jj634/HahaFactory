// adapted from: https://pusher.com/tutorials/consume-restful-api-react

import React from 'react'
import { Icon, Label, Popup, Button } from 'semantic-ui-react'

const JokeResults = ({ jokes }) => {
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
            {joke.text.split('\n').map ((item, i) => <h5 key={i}>{item}</h5>)}
            {/* <h6 className="card-subtitle mb-2 text-muted">{joke.score}</h6> */}
              {joke.categories.map((cat) => <Label>
                {cat}
              </Label>)}
              <h6 className="doughnut">Joke Score (stars pls): {joke.score}</h6>
              
              <Popup position='bottom left' trigger={<h6 className="doughnut">Similarity Score: {joke.similarity}</h6>}>
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