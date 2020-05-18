import React from 'react';
import axios from 'axios';
import { withRouter } from "react-router";

import { Form, Accordion, Icon } from 'semantic-ui-react'
import { Slider } from "react-semantic-ui-range";

import sizes from '../images/size';
import maturities from '../images/maturity'
import random from '../images/random'

class JokeForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            isLoaded: false,
            cat_options: [],

            categories: [],
            search: '',
            score: '',
            sizes: [],
            maturity: '',

            displayMessage: false,
            isOpen: false,
            URLParam: null,
        }
        this.advanced = React.createRef()
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAdvanced = this.handleAdvanced.bind(this);
        this.handleLucky = this.handleLucky.bind(this);
    }

    fillForm() {
        const URLParams = new URLSearchParams(this.props.location.search)
        const category_param = URLParams.getAll("categories")
        const score_param = URLParams.get("score")
        const search_param = URLParams.get("search")
        const size_param = URLParams.getAll("sizes")
        const maturity_param = URLParams.get("maturity")

        const cat_empty = category_param === null || category_param.length === 0
        const score_empty = score_param === null || score_param === "" || score_param === 0.25
        console.log(score_empty)
        const maturity_empty = maturity_param === null || maturity_param === ""
        const size_empty = size_param === null || size_param.length === 0

        const open = !cat_empty || !score_empty || !maturity_empty || !size_empty

        axios({
            method: 'GET',
            // url: `/api/cat-options`,
            url: `http://localhost:5000/api/cat-options`,
        })
            .then((response) => {
                this.setState({
                    cat_options: response.data.categories,
                    isLoaded: true,
                    categories: category_param || [],
                    score: score_param || 0.25,
                    sizes: size_param || [],
                    maturity: maturity_param || '',
                    search: search_param || '',
                    isOpen: open,
                    URLParam: URLParams
                })
            })
            .catch(err =>
                console.log(err)
            );
    }

    componentDidMount() {
        this.fillForm()
    }

    static getDerivedStateFromProps(nextProps, prevState) {
        const newURLParams = new URLSearchParams(nextProps.location.search)
        const oldURLParams = prevState.URLParam || new URLSearchParams()
        newURLParams.sort()
        oldURLParams.sort()
        const new_URL = newURLParams.toString()
        const old_URL = oldURLParams.toString()

        return new_URL !== old_URL
            ? { isLoaded: false, displayMessage: false }
            : null
    }

    componentDidUpdate(prevProps) {
        if (this.state.isLoaded === false) {
            this.fillForm();
        }
        this.focus()
    }

    handleChange = (e, { name, value }) => {
        this.setState({ [name]: value })
    }

    tonewURL = (search, categories, score, sizes, maturity) => {
        const params = new URLSearchParams()

        const search_empty = search === null || search === ""
        const cat_empty = categories === null || categories.length === 0
        const score_empty = score === null || score === ""
        const maturity_empty = maturity === null || maturity === ""
        const size_empty = sizes === null || sizes.length === 0

        if ((search_empty && cat_empty && size_empty && maturity_empty)) {
            this.setState({
                displayMessage: true
            })
        }
        else {
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

    handleSubmit(event) {
        event.preventDefault();
        const { search, categories, score, sizes, maturity } = this.state
        this.tonewURL(search, categories, score, sizes, maturity)
    }

    handleAdvanced = (e, titleProps) => {
        e.preventDefault();
        const { isOpen } = this.state
        const newActive = !isOpen
        this.setState({ isOpen: newActive })
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

    focus() {
        console.log("fucos")
        // if (this.advanced) {
            this.advanced.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
        // };
    }

    handleLucky(event) {
        event.preventDefault();
        const cat_options = this.state.cat_options.map((cat) => (
            {
                "categories": [cat]
            }
        ))

        const random_inputs = random.concat(cat_options)
        var item = random_inputs[Math.floor(Math.random() * random_inputs.length)];

        const cat = item.categories || []
        const search = item.search || ''
        const sizes = item.sizes || []
        const maturity = item.maturity || ''
        this.tonewURL(search, cat, 0.25, sizes, maturity)
    }

    render() {
        const categoryList = this.createDropDownList(this.state.cat_options)
        const sizeList = this.createDropDownList(sizes)
        const maturityList = this.createDropDownList(maturities)

        const slider_settings = {
            start: this.state.score,
            min: 0,
            max: 0.5,
            step: 0.125,
            onChange: value => {
                this.setState({
                    score: value
                })
            }
        };

        const icon = this.state.isOpen ? 'chevron down' : 'chevron right'

        return (
            <div ref={this.advanced}>
                <br />
                <Form onSubmit={this.handleSubmit} size="large" key="large" >
                    <Form.Input
                        placeholder="Enter your search"
                        name="search"
                        type="text"
                        onChange={this.handleChange}
                        value={this.state.search}
                        focus
                    />
                    < Accordion>
                        <Accordion.Title onClick={this.handleAdvanced}>
                            <Icon name={icon} />Advanced Search
                    </Accordion.Title>
                    </Accordion>
                    {this.state.isOpen
                        ? <div>
                            < Form.Dropdown
                                closeOnChange
                                placeholder="Select Categories"
                                name="categories"
                                label="Categories"
                                multiple
                                search
                                selection
                                options={categoryList}
                                onChange={this.handleChange}
                                value={this.state.categories}
                                clearable
                                focus
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
                                    value={this.state.maturity}
                                />

                                <Form.Dropdown
                                    placeholder="Select Joke Length"
                                    name="sizes"
                                    label="Joke Length"
                                    selection
                                    clearable
                                    multiple
                                    closeOnChange
                                    options={sizeList}
                                    onChange={this.handleChange}
                                    value={this.state.sizes}
                                    focus
                                />
                            </Form.Group>
                        </div>
                        : null
                    }
                    {this.state.displayMessage
                        ?
                        <h5 style={{ color: 'black' }}>Please provide an input for "Keywords", "Categories", "Maturity" or "Joke Length" to search.</h5>
                        : null
                    }

                    <Form.Group inline style={{ justifyContent: 'center', alignItems: 'center' }}>
                        <Form.Button secondary type="submit" size="large">Find Jokes</Form.Button>
                        <Form.Button primary size="large" onClick={this.handleLucky} >I'm Feeling Funny!</Form.Button>
                    </Form.Group>
                </Form >
            </div>
        )
    }
}

export default withRouter(JokeForm);