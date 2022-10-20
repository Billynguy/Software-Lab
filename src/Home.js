import { useState } from "react";

const Home = () => {
    const [projects, setProjects] = useState([
        { title: 'Project 1', id: 1},
        { title: 'Project 2', id: 2},
        { title: 'Project 3', id: 3},
    ])
    return (  
    <div className="home">
        <h1>Projects</h1>
        {projects.map((project) =>(
            <div className="project-preview" key={project.id}>
                <h2>{ project.title}</h2>
            </div>
        ))}

        <div className="links">
            <a href="/create" style={{
            color: "white",
            backgroundColor: '#3e35f1',
            borderRadius: '4px'
        }}>New Project</a>
        </div>
        
    </div>  
    );  
}
 
export default Home;