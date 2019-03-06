import React, {Component} from 'react';
import {Button, Jumbotron, Form, Container, Row, Col, Table, Badge, Alert} from 'react-bootstrap';
import Footer from './Footer.js';
import Header from './Header.js';
import axios from 'axios';
import config from './config.js';
import './App.css';


class App extends Component {
    constructor() {
        super();
        this.state = {
            msg: '',
            formValid: false,
            displayResult: false,
            displayError: false,
            error: '',
            result: {}

        };
        this.submit = this.submit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.validateForm = this.validateForm.bind(this);
        this.displayResult = this.displayResult.bind(this);
        this.displayError = this.displayError.bind(this);
        this.displayIntent = this.displayIntent.bind(this);
        this.displayEntities = this.displayEntities.bind(this)
    }

    async submit(e) {
        e.preventDefault();
        try {
            let data = JSON.stringify({

                message: this.state.msg,
                token: config.token,
            });
            let result = await axios.post(config.url, data,
                {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

            this.setState({displayResult: true, result: result.data, displayError:false});
            console.log(result.data);
        } catch (e) {
            this.setState({displayResult: true, result: {}, error: e});
            console.log(e);
        }

    }

    handleChange(e) {
        this.setState({msg: e.target.value}, this.validateForm);
    }


    static addEntity(entity, i) {

        return (
            <tr key={i}>
                <td>{entity.hasOwnProperty("entity") ? entity['entity'] : 'None'}</td>
                <td>{entity.hasOwnProperty("value") ? JSON.stringify(entity['value']) : 'None'}</td>
                <td>{entity.hasOwnProperty("confidence") ? entity['confidence'] : 'None'}</td>
            </tr>


        );

    }

    displayIntent() {
        if (!this.state.result.hasOwnProperty("intent")  || this.state.result.intent == null) {
            return (
                <h5>
                    Intent :  &nbsp; &nbsp;None &nbsp;&nbsp;
                </h5>
            );
        } else {
            return (<h5>
                Intent
                :  &nbsp; &nbsp;{this.state.result.intent.hasOwnProperty("name") ? this.state.result.intent.name : 'None'} &nbsp;&nbsp;
                <Badge variant="secondary">
                    {this.state.result.intent.hasOwnProperty("confidence") ? this.state.result.intent.confidence : 'None'}</Badge>
            </h5>);
        }


    }

    displayEntities() {
        if (undefined !== this.state.result.entities && this.state.result.entities.length > 0) {
            return (
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>Entity Name</th>
                        <th>Value</th>
                        <th>Confidence</th>

                    </tr>
                    </thead>
                    <tbody>
                    {this.state.result.entities.map(App.addEntity)}
                    </tbody>
                </Table>
            );

        } else {
            return (
                <h5> No entity found </h5>
            );
        }


    }

    displayError(){
        if(this.state.displayError){
            return        (
  <Alert  variant="danger">
    Error : {this.state.Error}
  </Alert>
);
        }

    }

    displayResult() {
        if (this.state.displayResult) {
            return (
                <div>
                    {this.displayIntent()}
                    <br/>
                    {this.displayEntities()}

                </div>
            );


        }
    }

    validateForm() {
        if (this.state.msg.length === 0) {
            this.setState({formValid: false});
        } else {
            this.setState({formValid: true});
        }
    }


    render() {
        return (
            <div>
                <Header/>


                <Jumbotron>
                    <Container id="content" fluid={true}>
                        <Row className="justify-content-md-center">
                            <Col md="auto">
                                <h2>Semantic analyzer - Chatbot Tourism</h2>
                            </Col>
                        </Row>
                        <br/>
                        {this.displayError()}
                        <br/>

                        <Form onSubmit={this.submit}>

                            <Form.Group
                                controlId="userName"
                                n
                            >


                                <Form.Control
                                    type="text"
                                    value={this.state.msg}
                                    placeholder="write here a sentence to parse"
                                    onChange={this.handleChange}
                                />


                            </Form.Group>


                            <Button type="submit" variant="primary" disabled={!this.state.formValid} size="lg" block>
                                Parse Sentence
                            </Button>

                        </Form>
                        <br/>
                        <br/>
                        {this.displayResult()}</Container>
                </Jumbotron>


                <Footer/>
            </div>
        );
    }
}

export default App;
