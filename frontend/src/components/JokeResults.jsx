// adapted from: https://pusher.com/tutorials/consume-restful-api-react

import React from 'react'
import { Icon, Label, Popup, Button } from 'semantic-ui-react'
import Highlighter from "react-highlight-words";
import Rating from '@material-ui/lab/Rating';
import { Doughnut } from 'react-chartjs-2';


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
                <h6 className="star_hover">
                  <Rating className="rating_stars" name="half-rating-read" defaultValue={joke.score} precision={0.1} readOnly />
                </h6>
              }/>
          </div>

              <h6 className="sim_sc_display">Similarity Score: {Number((Number(joke.similarity)*100).toFixed(1))+ "%"}</h6>
              <Popup position='right center' trigger={<Icon className="info_icon" color='teal' name='question circle' size='large' />} hoverable>
                <Popup.Header>Similarity Score Breakdown</Popup.Header>
                  <Popup.Content>
                    <Doughnut
                    data={
                      {
                        labels: ['Keywords (%)', 'Categories (%)', 'Funny Factor (%)'],
                        datasets: [
                          {
                            label: 'breakdown',
                            backgroundColor: [
                              '#FDC144',
                              '#FD6585',
                              '#3DA3E8'
                            ],
                            hoverBackgroundColor: [
                              '#FEDB93',
                              '#FEBCCA',
                              '#3DCEE8'
                            ],
                            data: [
                                    Number((Number(joke.cos_score)/Number(joke.similarity)*100).toFixed(1)), 
                                    Number((Number(joke.jac_score)/Number(joke.similarity)*100).toFixed(1)), 
                                    Number((Number(joke.sc_score)/Number(joke.similarity)*100).toFixed(1))
                                  ]
                          } 
                        ]
                      }
                    }
                    options={{
                      legend:{
                        display:true,
                        position:'right',
                        fontSize: 4
                      }
                    }}
                    />
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