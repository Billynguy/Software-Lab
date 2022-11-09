import { useState } from "react";
import { useHistory } from "react-router-dom";

const AddUser = () => {
    const [title, setTitle] = useState();
    const [description, setDescription] = useState();
    const [hwset1, setHwSet1] = useState(0);
    const [hwset2, setHwSet2] = useState(0);
    const [users, setUsers] = useState();
    const history = useHistory();
    

    const handleSubmit = (e) => {
        e.preventDefault();
        const project = {title, description, users, hwset1, hwset2}

        fetch('http://localhost:8000/projects',{
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(project)
        }).then(() => {
            history.push('/');
        });

    }

    return (
        <div className="add-user">
            <h2>Add a New User</h2>
            <form onSubmit={handleSubmit}>
                <label>User name:</label>
                <input 
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setUsers(e.target.value)}
                />
                <button>Add User</button>
            </form>

        </div>
    );
}

export default AddUser;