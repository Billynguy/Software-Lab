import { Link } from 'react-router-dom';

const Navbar = () => {


    return (  
        <nav className="navbar">
            <h1>ECE461L Website</h1>
            <div className="links">
                <Link to="/home">Home</Link>  
                <Link to="/create">Create Project</Link>
                <Link to="/" onClick={() => fetch('/api/sign-out')}>Logout</Link>
                
            </div>    
        </nav>
    );
}
 
export default Navbar;