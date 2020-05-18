import React from "react";
import { withRouter } from "react-router";

import logo from '../images/operator.png';

class Logo extends React.Component {
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
    render(){
        return (
            <div onClick={this.handleClick} style={{ cursor: 'pointer'}}>
                <header className="App-header">
                    <h1>HahaFactory:</h1>
                    <h2>Finding Hilarious Jokes for You</h2>
                    <img src={logo} className="App-logo" alt="logo" onClick={this.handleClick}/>
                </header>
            </div>
        )
    }
}
export default withRouter(Logo);
