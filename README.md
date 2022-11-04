# Software-Lab
ECE461L Software Lab Group consisting of Daniel Xie, Gaurav Belani, Billy Nguyen, Kerry Tu, and Bobby Chiu. Group name is Los Pollos Hermanos.

## Running the Development Server

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

# Flask secret key
FLASK_SECRET_KEY=<some-generated-key>
```

After preparing the requirements, make sure you activate the virtual environment. Then, you can run the back-end Flask app:

```sh
venv/Scripts/activate # For Windows, or `source venv/bin/activate` on non-Windows systems
flask run # Or `flask --debug run`
```
