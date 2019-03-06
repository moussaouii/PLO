import React from 'react';

import {Navbar, Row, Col} from 'react-bootstrap';

class Header extends React.Component {
    render() {
        return (

            <Row className="justify-content-md-center">
                <Col>
                    <Navbar>
                        <Navbar.Brand href="#home">Projet Long</Navbar.Brand>
                        <Navbar.Toggle/>
                        <Navbar.Collapse className="justify-content-end">
                            <Navbar.Text>
                                <a href="#login">ENSEEIHT</a>
                            </Navbar.Text>
                        </Navbar.Collapse>
                    </Navbar>
                </Col>
            </Row>
        );
    }
}


export default Header;