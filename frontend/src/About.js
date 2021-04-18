import React from 'react';

import { Button } from 'semantic-ui-react'

import Logo from './components/Logo'
import sample from './images/sample_input.JPG'
import result from './images/sample_result.JPG'
import similarity from './images/sample_similarity.JPG'

class About extends React.Component {
    constructor(props) {
        super(props)
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(event) {
        event.preventDefault();
        this.props.history.push({
            pathname: '/'
        })
    }
    render() {
        return (
            <React.Fragment>
                <Logo />
                <div style={{ alignItems: 'center', justify: 'center', maxWidth: '55%', left:'22.5%',  position: 'absolute', margin: "20px" }}>
                    <div style={{ textAlign: 'center'}}>          
                        <h2> Need a <b>pick-up line</b>?</h2> 
                        <h2>A <b>funny opener</b> for your upcoming speech? </h2> 
                        <h2>Or can’t remember the <b>punchline</b> of a joke you’ve heard before? … </h2>
                        <br/>
                        <h3 style={{ color: '#303030' }}> Then <b> HahaFactory</b> is the perfect place for you to find a laugh! </h3>
                    </div>
                    <h4 style={{ color: '#303030' }}>
                        <br/>
                        With jokes scraped from numerous sources covering different categories, types, maturity and length, 
                        our joke recommendation engine helps <b>you</b> find appropriate jokes for <b>any and every occassion.</b>
                        <hr></hr>                 
                        Our <b>simple search</b> allows you to input any keywords to your search, and relevant results will be displayed.
                        <br/><br/>
                        If you would like to refine your search further, the <b> advanced search</b> allows you to manually
                        add joke categories, adjust the relevancy vs. funny factor, and filter jokes based on maturity and length. 
                        <br/><br/>
                        Below is an example of a sample input.
                        <br/><br/> 
                        <img src={sample} style = {{width: '100%', height: '100%'}} />
                        <br /><br />
                        Relevant results are outputted with each joke displaying its joke score, a similarity score, and any relevant categories it falls under.
                        <br /><br />
                        <img src={result} style={{ width: '75%', height: '75%', left: '13%', position: 'relative' }} />
                        <br /><br />
                        The <b> Joke Score</b> is an indication of how funny the joke is. These scores were accumulated and standardized across our different data sources, and learned through KNN clustering.
                        <br /><br />
                        The <b> Similarity Score</b> is an indication of how relevant the joke is to the inputted query. Results are ranked based on similarity score. 
                        <br /><br />
                        <img src={similarity} style={{ width: '75%', height: '75%', left: '13%', position: 'relative' }} />
                        <br /><br />
                        To gain a better understanding of this score, you may hover over the similarity score number to see a <b>visual breakdown.</b>
                        The percent displayed corresponds to the weight that the corresponding input contributed to the total similarity score. 
                        <hr></hr>  
                        Our algorithm currently uses a <b>combination of similarity measurements </b>(fast jaccard, and fast cosine) and
                        and a <b> unique weighting system </b> to help you find results that are not only relevant, but also funny. 
                        Some additional features in our engine include <b>typo recognition </b>and an <b>"I'm Feeling Funny" </b>random joke generator.
                        <br/><br/>
                        We hope that you enjoy this insight into your results and find our recommendation engine fun! Have fun generating some more laughs!
                        <br /><br />
                    </h4>
                    <h4 style={{ textAlign: 'center', color: 'white'}}>
                        <a href="http://hahafactory-og.herokuapp.com/" target="_blank" style={{ margin: '20px' }}>First Prototype</a> 
                        <a href="http://hahafactory-v2.herokuapp.com/" target="_blank" style={{ margin: '20px' }}>Second Prototype</a> 
                        <a href="http://hahafactory.herokuapp.com/" target="_blank" style={{ margin: '20px' }}>Third Prototype</a> 
                    </h4>
                    <Button color = 'white' size = 'large' style={{ left:'38%', position: 'absolute', margin: '20px' }} onClick = {this.handleClick}>
                        Back to Search
                    </Button>
                </div>
            </React.Fragment>
        )
    }
}

export default About;