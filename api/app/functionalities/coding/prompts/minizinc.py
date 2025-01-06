prompt_template = """
You're an expert programmer in a team of operations research experts. The goal of the team is to solve an optimization or satisfaction problem. Your task is to write MiniZinc code for the {clauseType} of the problem.

Here's the {clauseType} we need you to write the code for:

-----
Description: {clauseDescription}
Formulation: {clauseFormulation}
-----

Here's the list of variables:

{relatedVariables}

Here's the list of parameters:

{relatedParameters}

Here's the problem summary:
{background}

Assume the parameters and variables are already defined and added to the model. Generate the code needed to define the {clauseType} and add it to the model accordingly.

Here is an example of code to add the objective, $\\max \\sum_{{i=1}}^{{N}} price_i x_i$ where the shape of both price and x is [N], to the model:

solve maximize sum(i in 1..N) (price[i] * x[i]);

Here is an example of code to add a constraint, $\\forall i, SalesVolumes[i] \leq MaxProductionVolumes[i]$ where the shape of both SalesVolumes and MaxProductionVolumes is [N], to the model:

constraint SalesVolumes <= MaxProductionVolumes;

- When indexing make sure that you use 1 based indexing, starting from 1 and not 0.
- Only generate the code needed to define the {clauseType} and add it to the model accordingly. 
- Do not include any comments or explanations, unless no code is needed. If no code is needed, just return a comment saying "No code needed".
- Assume imports, parameters definitions, variable definitions, and other setup code is already written. You must not include any setup code.
- Even for simple constraints like non-negativity or sign constraints, include code to add them to the model explicitly (they are not added in the variable definition step).

Take a deep breath, and solve the problem step by step.
"""

import_code = "import minizinc"


def generate_variable_code(symbol, var_type, shape):
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