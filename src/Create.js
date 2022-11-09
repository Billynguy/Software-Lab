import { useState } from "react";
import { useHistory } from "react-router-dom";

const Create = () => {
    const [title, setTitle] = useState();
    const [id, setID] = useState();
    const [description, setDescription] = useState();
    const [users, setUsers] = useState();
    const [hwset1, setHwSet1] = useState(0);
    const [hwset2, setHwSet2] = useState(0);
    const history = useHistory();
    

    const handleSubmit = (e) => {
        e.preventDefault();
        const project = new FormData();//{id, title, description}
        project.set('projectid', id)
        project.set('name', title)
        project.set('description', description)

        

        fetch('/api/create-project',{
            method: 'POST',
            body: project
        }).then(() => {
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
            }).then(res => res.json()).then(data => console.log(data));
            
            history.push('/home');
        });

        

    }

    return (
        <div className="create">
            <h2>Add a New Project</h2>
            <form onSubmit={handleSubmit}>
            <label>Project ID:</label>
                <input 
                    type="text"
                    required
                    value={id}
                    onChange={(e) => setID(e.target.value)}
                />
                <label>Project Title:</label>
                <input 
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                
                <label>Project Description:</label>
                <textarea
                    required
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    ></textarea>
                <label>Add users:</label>
                <input 
                    type="text"
                    required
                    value={users}
                    onChange={(e) => setUsers(e.target.value)}
                />
                <button>Add Project</button>
            </form>

        </div>
    );
}

export default Create;