import { useParams } from "react-router-dom";
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
                    </div>
                </article>
            )}
        </div>
     );
}
 
export default ProjectDetails;