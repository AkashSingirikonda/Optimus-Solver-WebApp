import os
import subprocess
from api.app.functionalities.debugging.fix_code import fix_code

### auto_testing_helper functions for cvxpy
# Import Code
import_code = "import minizinc"

# Get variable code
def get_var_code(symbol, var_type, shape):
    var_type = var_type.lower()
    if var_type not in ["continuous", "binary", "integer"]:
        raise ValueError(f"Unsupported variable type: {var_type}")
    
    if shape:
        if len(shape) == 1:
            shape_str = f"1..{shape[0]}"
            array_type = f"array[{shape_str}] of "
        else:
            shape_str = " ,".join([f"1..{dim}" for dim in shape])
            array_type = f"array[{shape_str}] of "
    else:
        array_type = ""

    var_declaration = ""
    if var_type == "discrete" or var_type == "integer":
        var_declaration = f"{array_type}var int: {symbol};"
    elif var_type == "continuous":
        var_declaration = f"{array_type}var float: {symbol};"

    return f"model.add_string(\"{var_declaration}\")"

# Synthesize the code
def synthesize_code_minizinc(data, dir):

    parameters = data["parameters"]
    variables = data["variables"]
    constraints = data["constraints"]
    objective = data["objective"]

    prep_code = ("""
import json
import numpy as np

import minizinc

with open("parameters.json", "r") as f:
    parameters = json.load(f)

model = minizinc.Model()
""")
    code = []
    code.append(prep_code)
    code.append("\n\n### Define the parameters\n")
    ## Debug:
    print("####")
    print(data["parameters"].items())
    for symbol, p in data["parameters"].items():
        shape = p["shape"]
        # definition = p["definition"]
        if len(shape) == 0:
            # Scalar parameter
            mzn_type = "float"
            param_string = f"{mzn_type}: {symbol};"
        else:
            # Array parameter
            # Check if shape contains symbols or numbers
            dimensions = ", ".join([
                f"1..{s}" if isinstance(s, str) else f"1..{s}" for s in shape
            ])
            element_type = "float"
            param_string = f"array[{dimensions}] of {element_type}: {symbol};"
            
        # Add instance assignment code
        a = "model.add_string('" + param_string + "\')" + "\n"
        code.append(a)
    
    code.append("\n\n### Define the variables\n")
    for symbol, v in variables.items():
        code.append(get_var_code(symbol, v["type"], v["shape"]))
    
    code.append("\n\n### Define the constraints\n")
    for c in constraints:
        a = c['code']
        code.append(f"model.add_string('{a}')")
    
    code.append("\n\n### Define the objective\n")
    a = objective["code"]
    code.append(f"model.add_string(\'{a}\')")

    # Select a solver (To optimize)
    code.append(f"\n# Instantiate Model\nsolver = minizinc.Solver.lookup(\"highs\")\n")

    # Creating model instance
    code.append(f"\n# Create Instance\ninstance = minizinc.Instance(solver, model)\n")

    # Adding instance parameters
    for symbol, p in data["parameters"].items():
        shape = p["shape"]
        code.append(f'{symbol} = parameters["{symbol}"] # shape: {p["shape"]}, definition: {p["definition"]}')
        code.append(f"instance['{shape}'] = {shape}\n")
    
    # Optimize the model
    code.append("\n\n### Optimize the model\n")
    code.append(f"\n# Optimize model\nresult = instance.solve()\n")

    # Take care of model output!

        #
#    code.append(
#      """
# if problem.status in ["OPTIMAL", "OPTIMAL_INACCURATE"]:
#     with open("output_solution.txt", "w") as f:
#        f.write(str(problem.value))
# else:
#     with open("output_solution.txt", "w") as f:
#        f.write(problem.status)
# """
#        )

#    code_str = "\n".join(code)

    with open(os.path.join(dir, "code.py"), "w") as f:
        f.write("\n".join(code))

## Execute the code
def execute_code(dir, code_filename):
    try:
        code_path = os.path.join(dir, code_filename)
        # Using Python's subprocess to execute the code as a separate process
        result = subprocess.run(
            ["python", code_filename],
            capture_output=True,
            text=True,
            check=True,
            cwd=dir,
        )
        # save result in a file
        with open(os.path.join(dir, "code_output.txt"), "w") as f:
            f.write(f"Optimal Objective Value: {result.stdout}\n")
        return result.stdout, "Success"
    except subprocess.CalledProcessError as e:
        return e.stderr, "Error"

## Execute the code with debug support
def execute_and_debug(dir, max_tries=3):

    code_filename = "code.py"
    with open(os.path.join(dir, code_filename), "r") as f:
        code = f.read()

    for iteration in range(max_tries):

        # Execute the code
        output, status = execute_code(dir, code_filename)

        # Print status and update the prompt if needed
        if status == "Success":
            break
        else:
            debug_data = {
                "code": code,
                "error_message": output,
                "solver": "minizinc",
            }
            debug_data.update(fix_code(debug_data))
            code = debug_data["code"]
            code_filename = f"code_{iteration + 1}.py"
            code_file_path = os.path.join(dir, code_filename)
            with open(code_file_path, "w") as f:
                f.write(code)