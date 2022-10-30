# Software-Lab

ECE461L Software Lab Group consisting of Daniel Xie, Gaurav Belani, Billy Nguyen, Kerry Tu, and Bobby Chiu. Group name is Los Pollos Hermanos.

## Running the Development Server

### React Front-end
0. You must have [Node.js](https://nodejs.org/en/) installed.
1. Clone this repo with ``git clone https://github.com/evmaki/ee461-frontend-in-react.git``
2. ``cd`` into ``ee461-frontend-in-react``
3. Run ``npm install`` to install the project's dependencies (i.e. React and all the JS libraries it depends on).
4. Once the dependencies are downloaded, run ``npm start`` to start the development server.
5. You can access the interface while you're working on it at http://localhost:3000 in your web browser.

### Flask Back-end

Make sure you have Python 3 installed.

After cloning this repo, you will need to set up a virtual environment and install the required Python packages for the back-end:

```sh
cd backend
py -3 -m venv venv # For Windows, or `python3 -m venv venv` on non-Windows systems
venv/Scripts/activate # For Windows, or `source venv/bin/activate` on non-Windows systems
pip install -r requirements.txt
```

Also, you will need to create a `.env` file that looks like the following with appropriate substitution:

```env
# MongoDB Atlas connection string variables
MONGODB_USERNAME=<username>
MONGODB_PASSWORD=<password>
MONGODB_CLUSTER_ADDRESS=<cluster-address>
```

After preparing the requirements, make sure you activate the virtual environment. Then, you can run the back-end Flask app:

```sh
venv/Scripts/activate # For Windows, or `source venv/bin/activate` on non-Windows systems
flask run # Or `flask --debug run`
```
