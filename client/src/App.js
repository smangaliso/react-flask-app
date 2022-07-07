import React, { useEffect, useState } from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Table from "react-bootstrap/Table";

const App = () => {
  const [cases, setCases] = useState([]);
  const [vaccines, setVaccines] = useState([]);

  useEffect(() => {
    fetch("/cases", {
      method: "GET",
      headers: { "content-type": "applications/json" },
    })
      .then((resp) => resp.json())
      .then((resp) => setCases(resp))
      .catch((err) => console.log(err));
  }, []);

  useEffect(() => {
    fetch("/vaccines", {
      method: "GET",
      headers: { "content-type": "applications/json" },
    })
      .then((resp) => resp.json())
      .then((resp) => setVaccines(resp))
      .catch((err) => console.log(err));
  }, []);
  return (
    <div className="App">
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Country</th>
            <th>Confirmed</th>
            <th>Death</th>
          </tr>
        </thead>
        <tbody>
          {cases.map((case_) => {
            return (
              <tr key={case_.id}>
                <td>{case_.country}</td>
                <td>{case_.confirmed}</td>
                <td>{case_.death}</td>
              </tr>
            );
          })}
        </tbody>
      </Table>
      <Table className="mt-4" striped bordered hover>
        <thead>
          <tr>
            <th>Country</th>
            <th>Administered</th>
            <th>Partially Vaccinated</th>
            <th>Fully Vaccinated</th>
          </tr>
        </thead>
        <tbody>
          {vaccines.map((vaccine) => {
            return (
              <tr key={vaccine.id}>
                <td>{vaccine.country}</td>
                <td>{vaccine.administered}</td>
                <td>{vaccine.people_partially_vaccinated}</td>
                <td>{vaccine.people_vaccinated}</td>
              </tr>
            );
          })}
        </tbody>
      </Table>
    </div>
  );
};

export default App;
