import { useState, useEffect } from "react";
import ProjectList from "./ProjectList";
import useFetch from "./useFetch";

const Home = () => {
    const { data: projects, isPending, error} = useFetch('http://localhost:8000/projects');

    return (  
        <div className="home">
            { error && <div>{error}</div>}
            { isPending && <div>Loading...</div>}
            {projects && <ProjectList projects={projects} title="All Projects" />}
        </div>

    );  
}
 
export default Home;