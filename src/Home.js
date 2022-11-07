import { useState, useEffect } from "react";
import ProjectList from "./ProjectList";
import useFetch from "./useFetch";

const Home = () => {
    //const { data: projects, isPending, error} = useFetch('http://localhost:8000/projects');
    const {data: projects} = fetch('/api/bchiu/project-list/');

    return (  
        <div className="home">
            {projects}
        </div>

    );  
}
 
export default Home;