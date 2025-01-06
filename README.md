# OptiMUS Solver

This repo contains the code for backend and frontend of [OptiMUS Solver Web App](https://optimus-solver.com/). For OptiMUS paper repositories, see [OptiMUS GitHub Repository](https://github.com/teshnizi/OptiMUS).

![image](https://github.com/user-attachments/assets/64837284-6f78-4158-90b3-4dae76e6e426)

## Structure

The backend, built with Flask, is located in the [`api/`](api/) directory. The frontend, a React application, can be found in the [`app/`](app/) directory.

## Dataset

You can download the dataset from [https://huggingface.co/datasets/udell-lab/NLP4LP](https://huggingface.co/datasets/udell-lab/NLP4LP). Please note that NLP4LP is intended and licensed for research use only. The dataset is CC BY NC 4.0 (allowing only non-commercial use) and models trained using the dataset should not be used outside of research purposes (The updated version will be added soon).

## Running the project locally 

What you need:
- A system with python and node/npm installed
- A [firestore project](https://firebase.google.com/docs/firestore/quickstart) with a [service account](https://firebase.google.com/support/guides/service-accounts).

Steps:
0. Create a Firestore project on Firebase, enable authentication and storage, and download a json credential key for it. Here are the steps:
- Go to the Firebase Console and select your Firebase project (Create one if you don't have one)
- Open Project Settings: In the Firebase console, click on the gear icon next to Project Overview in the sidebar. Select Project settings from the dropdown.
- Navigate to Service Accounts: In the Project settings page, click on the Service accounts tab at the top
- Generate a New Private Key: Under the Firebase Admin SDK section, click on Generate new private key. Firebase will create a new private key in JSON format and download it to your computer automatically.
- Embed the json into base64 using `base64 -i admin_creds.json -o admin_creds_base64.txt` (change admin_creds.json to your credentials file name)

You’ll need this JSON file to authenticate your Firebase Admin SDK requests.
1. Edit [the main .env.example](https://github.com/OptiMUS-optimization-modeling/Optimus-Solver-WebApp/blob/main/.env.example) file and add your `OPENAI_API_KEY` and `FIREBASE_CREDENTIALS` from your service account. `FIREBASE_CREDENTIALS` should be the base64 encoding of your firebase json credentials (explained in step 0). 
2. Edit [the frontend .env.example](https://github.com/OptiMUS-optimization-modeling/Optimus-Solver-WebApp/blob/main/interface/.env.example) file and add your frontend firebase credentials (You can get one via firebase dashboard > settings > general > add app > web app).
3. Rename both `.env.example` files to `.env`
4. Open new terminals (so .env files take effect), create a new virtual environment, and run `pip install -r requirements.txt` to install the requirements.
5. Start the flask backend using `flask run`. (You may have to modify $PATH, $PYTHONPATH, and/or $FLASKAPP to get this to work)
6. Install and start the react frontend:

   ```
   cd interface/
   npm install
   npm start
   ```

7. Open `http://localhost:3000/` in your browser.

## Contribution

To contribute to the web app, please open an issue or a pull request. All code functionalities are in the [`/api/app/functionalities`](api/app/functionalities) directory.

## Adding New Solvers

To add new a new solver, please follow these steps:

1. Create a **coding prompt** file SOLVER_NAME.py in [Coding Prompts](https://github.com/OptiMUS-optimization-modeling/Optimus-Solver-WebApp/tree/main/api/app/functionalities/coding/prompts). Make sure you also include the **variable code generation function()**, the **import code**, and the **get_info_code**)
   1.   **get_info_code** This code is used to get the solver information after the model is run. It should support all status (OPTIMAL, INFEASIBLE, UNBOUNDED, etc.) and store the objective value, variables, runtime, and iteration count in the solving_info dictionary.
   2. **variable code generation function()** is used to generate variable codes from their symbol, shape, and type.

2. Create a **formulation prompt** file SOLVER_NAME.py in [Formulation Prompts](https://github.com/OptiMUS-optimization-modeling/Optimus-Solver-WebApp/tree/main/api/app/functionalities/formulation/prompts)
3. Create a **debugging prompt** file SOLVER_NAME.py in [Debugging Prompts](https://github.com/OptiMUS-optimization-modeling/Optimus-Solver-WebApp/tree/main/api/app/functionalities/debugging/prompts)
4. Add the solver to the dropdown list in the front end [Analysis Page](https://github.com/OptiMUS-optimization-modeling/Optimus-Solver-WebApp/blob/main/interface/src/Pages/MainApp/Analysis/AnalysisPage.js). For example for cvxpy, you should add this line  `<option value="cvxpy">cvxpy</option>`
5. Add the solver import instruction to (https://github.com/OptiMUS-optimization-modeling/Optimus-Solver-WebApp/tree/main/api/solver_list.json)

Create a PR request to merge the code. You can look at the existing prompt files for gurobipy for reference. 

# Privacy Policy

The data uploaded to the web app is not used for any commercial purposes. The usage data can be used by in the future to 1) improve the web app and 2) do academic user studies on how people model and solve optimization problems.
