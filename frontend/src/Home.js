import { useState, useEffect } from "react";
import ProjectList from "./ProjectList";
import useFetch from "./useFetch";

const Home = () => {
    //const { data: projects, isPending, error} = useFetch('http://localhost:8000/projects');
    const [projectItems, setProjectItems] = useState([]);
    useEffect(
        () => {
            fetch('/api/user/session-project-list', {
                method: 'GET'
            }).then(res => res.json()).then(json => {
                setProjectItems(json.data.projects);
            });
        }, []
    );

    const projectItemsRender = projectItems.map((project) => {
        return (<li key={project}><a href={`/projects/${project}`}>{`Project ${project}`}</a></li>);
    })

    // {method: 'GET'}).then(res => res.json()).then(data => console.log(data))

    // const projectItems = projects.map((aproject) => {
    //     <li key={aproject.toString()}>
    //         {aproject}
    //     </li>
    // }
    // );

    return (  
        <div className="home">
            {/* <ul>{projectItemsRender}</ul> */}
            {projectItemsRender}
        </div>

    );  
}
 
export default Home;