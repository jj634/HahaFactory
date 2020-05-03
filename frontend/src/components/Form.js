import React from 'react';
import axios from 'axios';
import { withRouter } from 'react-router-dom'

import { Form } from 'semantic-ui-react'
import { Slider } from "react-semantic-ui-range";
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
            sizes: this.props.sizes || [],
            maturity: this.props.maturity || '',
            displayMessage: false
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
        const { search, categories, score, sizes, maturity } = this.state

        const params = new URLSearchParams()

        const search_empty = search === null || search === ""
        const cat_empty = categories === null || categories.length == 0
        const score_empty = score === null || score === ""
        const maturity_empty = maturity === null || maturity === ""
        const size_empty = sizes === null || sizes.length == 0

        if((search_empty && cat_empty && size_empty) && (!score_empty || !maturity_empty)){
            this.setState({
                displayMessage: true
            })
        } else {
            if (!search_empty) params.append("search", search)
            if (!cat_empty) {
                categories.forEach(cat => {
                    params.append("categories", cat);
                })
            }
            if (!score_empty) params.append("score", score)
            if (!maturity_empty) params.append("maturity", maturity)
            if (!size_empty) {
                sizes.forEach(size => {
                    params.append("sizes", size);
                })
            }

            const url = '?' + params.toString()
            this.props.history.push({
                pathname: '/',
                search: url
            })
        }
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
        const sizeList = this.createDropDownList(sizes)
        const maturityList = this.createDropDownList(maturities)

        const slider_settings = {
            start: this.props.score || 0.25,
            min: 0,
            max: 0.5,
            step: 0.125,
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
                        <Slider discrete color="white" settings={slider_settings} />
                    </Form.Field>
                    <Form.Dropdown
                        placeholder="Select Maturity"
                        name="maturity"
                        label="Maturity Rating"
                        selection
                        clearable
                        options={maturityList}
                        onChange={this.handleChange}
                        defaultValue = {this.props.maturity}
                    />

                    <Form.Dropdown
                        placeholder = "Select Joke Length"
                        name = "sizes"
                        label = "Joke Length"
                        selection
                        clearable
                        multiple
                        options = {sizeList}
                        onChange = {this.handleChange}
                        defaultValue = {this.props.sizes}
                    />
                </Form.Group>

                {this.state.displayMessage
                    ? 
                    <h5 style={{color:'black'}}>Please provide an input for "Keywords", "Categories" or "Joke Length" to search.</h5>
                    : null}

                <Form.Group inline>
                    <Form.Button inline center secondary type="submit" size="large">Find Jokes</Form.Button>
                    <Form.Button center primary type="submit" size="large">I'm Feeling Funny!</Form.Button>
                </Form.Group>
            </Form>
        )
    }
}

export default withRouter(JokeForm);
