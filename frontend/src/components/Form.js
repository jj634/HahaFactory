import React from 'react';
import axios from 'axios';
import { withRouter } from 'react-router-dom'

import { Form } from 'semantic-ui-react'
import { Slider } from "react-semantic-ui-range";
import scores from '../images/scores';
import sizes from '../images/size';
import maturities from '../images/maturity'

class JokeForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            isLoaded: false, // indicates if categories have been loaded from API GET request
            cat_options: [],         

            categories: this.props.categories || [], 
            search: this.props.search || '', 
            score: this.props.score || '', 
            size: this.props.size || '',
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        // this.createDropDownList = this.createDropDownList(this);
    }

    componentDidMount() {
            axios({
                method: 'GET',
                // url: `/api/cat-options`,
                url: `http://localhost:5000/api/cat-options`,
            })
            .then((response) => {
                this.setState({
                    cat_options: response.data.categories, 
                    isLoaded: true, 
                })
            })
            .catch(err =>
                console.log(err)
            );
    }

    handleChange = (e, { name, value }) => {
        this.setState({ [name]: value })
    }

    handleSubmit(event) {
        event.preventDefault();
        const { search, categories, score, size } = this.state

        const params = new URLSearchParams()
        if (this.state.search != null) params.append("search", search)

        if (this.state.categories !== null) {
        categories.forEach(cat => {
            params.append("categories", cat);
        })
        }

        if (this.state.score != null) params.append("score", score)
        if (this.state.size != null) params.append("size", size)

        const url = '?'+params.toString()
        this.props.history.push({
            pathname: '/',
            search: url
        })
    }

    createDropDownList = (list) => {
        return list.map((element) =>
            ({
                key: element,
                text: element,
                value: element
            })
        )
    }

    render() {
        const categoryList = this.createDropDownList(this.state.cat_options)
        const scoreList = this.createDropDownList(scores)
        const sizeList = this.createDropDownList(sizes)
        const maturityList = this.createDropDownList(maturities)

        const slider_settings = {
            start: 3,
            min: 1,
            max: 5,
            step: 1,
            onChange: value => {
                this.setState({
                    score: value
                })
            }
        };
      
        return (
            <Form onSubmit={this.handleSubmit} size = "large" key = "large">
                <Form.Input
                    placeholder="Enter your search"
                    name="search"
                    label="Keywords"
                    type="text"
                    onChange={this.handleChange}
                    defaultValue={this.props.search} 
                    clearable
                />

                <Form.Dropdown
                    closeOnChange
                    placeholder="Select Categories"
                    name="categories"
                    label="Categories"
                    multiple
                    search
                    selection
                    options={categoryList}
                    onChange={this.handleChange}
                    defaultValue = {this.props.categories}
                    clearable
                />

                
                <Form.Group widths='equal'>
                    <Form.Field>
                        <p><b>Relevancy       vs.      Funny Factor</b></p>
                        <Slider discrete value={this.props.score} color="white" settings={slider_settings} />
                    </Form.Field>
                    <Form.Dropdown
                        placeholder="Select Maturity"
                        name="maturity"
                        label="Maturity Rating"
                        selection
                        clearable
                        options={maturityList}
                        // onChange={this.handleChange}
                        // defaultValue = {this.props.score}
                    />

                    <Form.Dropdown
                        placeholder = "Select Joke Length"
                        name = "size"
                        label = "Joke Length"
                        selection
                        clearable
                        multiple
                        options = {sizeList}
                        onChange = {this.handleChange}
                        defaultValue = {this.props.size}
                    />
                </Form.Group>

                <Form.Group inline>
                    <Form.Button inline center secondary type="submit" size="large">Find Jokes</Form.Button>
                    <Form.Button center primary type="submit" size="large">I'm Feeling Funny!</Form.Button>
                </Form.Group>
            </Form>
        )
    }
}

export default withRouter(JokeForm);
