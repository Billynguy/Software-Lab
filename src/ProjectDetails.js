import { useParams, Link } from "react-router-dom";
import useFetch from './useFetch';

const ProjectDetails = () => {

    const { id } = useParams();
    const { data: project, error, isPending} = useFetch('http://localhost:8000/projects/' + id);


    return ( 
        <div className="project-details">
            {isPending && <div>Loading...</div>}
            {error && <div>{error}</div>}
            {project && (
                <article>
                    <h2>{project.title}</h2>
                    <div>
                        <p>HW Set 1: {`${project.hwset1}`}</p>
                        <p>HW Set 2: {`${project.hwset2}`}</p>
                        <Link to={`/projects/${project.id}/resources`}>
                            <h2>Resource Page</h2>
                        </Link>
                    </div>
                </article>
            )}
        </div>
     );
}
 
export default ProjectDetails;