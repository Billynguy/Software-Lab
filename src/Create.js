import { useState } from "react";
import { useHistory } from "react-router-dom";

const Create = () => {
    const [title, setTitle] = useState();
    const [id, setID] = useState();
    const [description, setDescription] = useState();
    const [hwset1, setHwSet1] = useState(0);
    const [hwset2, setHwSet2] = useState(0);
    const history = useHistory();
    

    const handleSubmit = (e) => {
        e.preventDefault();
        const project = {title, description, hwset1, hwset2}

        fetch('http://localhost:8000/projects',{
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(project)
        }).then(() => {
            history.push('/home');
        });

    }

    return (
        <div className="create">
            <h2>Add a New Project</h2>
            <form onSubmit={handleSubmit}>
                <label>Project Title:</label>
                <input 
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <label>Project ID:</label>
                <input 
                    type="text"
                    required
                    value={id}
                    onChange={(e) => setID(e.target.value)}
                />
                <label>Project Description:</label>
                <textarea
                    required
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    ></textarea>
                <button>Add Project</button>
            </form>

        </div>
    );
}

export default Create;