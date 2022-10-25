import { useState, useEffect } from "react";
import ProjectList from "./ProjectList";

const Home = () => {
    const [projects, setProjects] = useState(null);
    const [isPending, setIsPending] = useState(true);
    // COMMMENTED as we will eventually make delete request to server
    // const handleDelete = (id) => {
    //     const newProjects = projects.filter(project => project.id !== id); // leaves orig array unchanged, and returns a new array based on orig array
    //     setProjects(newProjects);
    // }

    // useEffect fires on every render
    useEffect(() => {                           // can't make this async
        fetch('http://localhost:8000/projects')
            .then(res => {                      // 'then' fires a function once the fetch promise has resolved, ie once we have the data back. Reponse object res is NOT the data
                return res.json()               // passes the json into a javascript object, the 'return res.json()' returns a promise b/c res.json() is aync
            })
            .then(data => {                     // we get the data now   
                setProjects(data);
                setIsPending(false);
            })       
        ;
    }, []);                                     // fetch this data once when the component renders

    return (  
        <div className="home">
            { isPending && <div>Loading...</div>}
            {projects && <ProjectList projects={projects} title="All Projects" />}
        </div>

    );  
}
 
export default Home;