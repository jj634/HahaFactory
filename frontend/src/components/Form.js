import React from 'react';
import axios from 'axios';
import { withRouter } from 'react-router-dom'

import { Button, Form } from 'semantic-ui-react'
import scores from '../images/scores';
import length from '../images/length';

class JokeForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            isLoaded: false, // indicates if categories have been loaded from API GET request
            cat_options: [],         

            categories: this.props.categories, 
            search: this.props.search, 
            score: this.props.score, 
            length: this.props.length, 
        }
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
            axios({
                method: 'GET',
                url: `http://localhost:5000/api/cat-options`
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
        const { search, categories, score, length } = this.state

        const params = new URLSearchParams()
        if (this.state.search != null) params.append("search", search)

        if (this.state.categories !== null) {
        categories.forEach(cat => {
            params.append("categories", cat);
        })
        }

        if (this.state.score != null) params.append("score", score)
        if (this.state.length != null) params.append("length", length)

        const url = '?'+params.toString()
        this.props.history.push({
            pathname: '/',
            search: url
        })
    }

    render() {
        const categoryList = this.state.cat_options.map((cat) =>
            ({
                key: cat,
                text: cat,
                value: cat
            })
        );

        const scoreList = scores.map((score) =>
            ({
                key: score,
                text: score,
                value: score
            })
        );

        const lengthList = length.map ((length) => 
            (
                < Form.Radio
                                    name = "length"
                                    label={length}
                                    defaultValue = {this.propslength}
                                    checked = { length === this.props.length}
                                    onChange = { this.handleChange }
        />
            ))
        return (
                        <Form onSubmit={this.handleSubmit}>
                            <Form.Input
                                placeholder="Search"
                                name="search"
                                label="Keywords"
                                type="text"
                                onChange={this.handleChange}
                                defaultValue={this.props.search} 
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
                            />

                            <Form.Dropdown
                                placeholder="Select Minimum Score"
                                name="score"
                                label="Minimum Score"
                                selection
                                options={scoreList}
                                onChange={this.handleChange}
                                defaultValue = {this.props.score}
                            />

                            <Form.Group inline>
                                <label>Size</label>
                                {lengthList}
                            </Form.Group>

                            <Button class="ui button" type="submit">Go</Button>
                        </Form>
        )
    }
}

export default withRouter(JokeForm);
