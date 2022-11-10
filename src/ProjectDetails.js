import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import useFetch from './useFetch';

const ProjectDetails = () => {

    const { id } = useParams();
    const [curUserID, setCurUserID] = useState();
    //const { data: project, error, isPending} = useFetch('http://localhost:8000/projects/' + id);
    const [users, setUsers] = useState();
    const [projectItems, setProjectItems] = useState([]);
    const [resourceItems, setResourceItems] = useState([]);

    const [displayPopupAddUser, setDisplayPopupAddUser] = useState(false);
    const [popupTextAddUser, setPopupTextAddUser] = useState("");


    //const [hwItem2, setHwItem2] = useState([]);
    useEffect(
        () => {
            fetch(`/api/project/${id}/project-info`, {
                method: 'GET'
            }).then(res => res.json()).then(json => {
                setProjectItems(json.data);
            });

            fetch(`/api/project/${id}/resources`, {
                method: 'GET'
            }).then(res => res.json()).then(json => {
                setResourceItems(json.data.resources);
            });
            
        }, []
    );

    // const projectItemsRender = projectItems.map((comps) => {
    //     return (<li key={comps}>{`${comps.name } ID: ${comps.projectid} ${comps.description}`}</li>);
    // })

    const resourceItemsRender = resourceItems.map((project) => {
        return (<li key={project}>{`${project.name} checked out units: ${project.checkedOut}`}</li>);
    })


    const handleSubmit = (e) => {
        e.preventDefault();
        var parsedUsers = users.split(', ')
            
        const userids = []
        for(let i = 0; i < parsedUsers.length; i++){
            userids.push(parsedUsers[i]);
        }
        const usersForm = new FormData();
        usersForm.set('userids', userids);
        fetch(`/api/project/${id}/authorize-user-multiple`, {
            method: 'POST',
            body: usersForm,
        }).then(res => res.json()).then(data => {
            if (!data.status.success){
                setPopupTextAddUser(data.status.reason)
                //setDisplayPopupAddUser(true)
            }
            else{
                setPopupTextAddUser("User(s) successfully added.")
                //setDisplayPopupAddUser(true)
            }
            setDisplayPopupAddUser(true)
            
        });
    }

    return ( 
        <div className="project-details">
            {/* {isPending && <div>Loading...</div>}
            {error && <div>{error}</div>} */}
            {(
                <article>
                    <div>
                        <h1>{projectItems.name}</h1>
                        <h4>Project ID: {projectItems.projectid}</h4>
                        <h4>{projectItems.description}</h4>
                        {/* {projectItemsRender} */}
                        {resourceItemsRender}
                    
                        <Link to={`/projects/${id}/resources`}>
                            <h2>Resource Page</h2>
                        </Link>
                    </div>
                    <form onSubmit={handleSubmit}>
                        <label>Add users:</label>
                        <input 
                            type="text"
                            required
                            value={users}
                            onChange={(e) => setUsers(e.target.value)}
                        />
                        <button>Add User</button>

                    </form>
                </article>
                
            )}
            {displayPopupAddUser && <h3>{popupTextAddUser}</h3>}
        </div>
     );
}
 
export default ProjectDetails;