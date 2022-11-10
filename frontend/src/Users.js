import { Link } from "react-router-dom";

const Users = ({ users }) => {
    return (
        <div className="user-list">
            <h2>Users</h2>
            {users.map((user) => (
                <div className="user">
                   <article>
                        <p>{ user }</p>
                    </article>

                </div>     
            ))}
        </div>
    )
}
 
export default Users;