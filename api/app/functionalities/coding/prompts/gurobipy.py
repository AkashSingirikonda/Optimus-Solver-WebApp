prompt_template = """
You're an expert programmer in a team of optimization experts. The goal of the team is to solve an optimization problem. Your task is to write gurobipy code for the {clauseType} of the problem.

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

Assume the parameters and variables are already defined and added to the model, gurobipy is imported as gp, and the model is named model. Generate the code needed to define the {clauseType} and add it to the model accordingly.

Here is an example of code to add the objective to the model:

model.setObjective(quicksum(profit[k] * x[k, i] - storeCost * s[k, i] for k in range(K) for i in range(I)), gp.GRB.MAXIMIZE)

Here is an example of code to add a constraint to the model:

for i in range(I):
    for m in range(M):
        model.addConstr(storage[i, m] <= storageSize[m], name="storage_capacity")

Here is an example of code to add a variable to the model:

y = model.addVar(name="y", vtype=GRB.BINARY)

- Only generate the code needed to define the {clauseType} and add it to the model accordingly. 
- Do not include any comments or explanations, unless no code is needed. If no code is needed, just return a comment saying "No code needed".
- Assume imports, parameters definitions, variable definitions, and other setup code is already written. You must not include any setup code.

- Even for simple constraints like non-negativity or sign constraints, include code to add them to the model explicitly (they are not added in the variable definition step).

Take a deep breath, and solve the problem step by step.
"""


def generate_variable_code(symbol, type, shape):
    if not shape or len(shape) == 0:
        return f"{symbol} = model.addVar(name='{symbol}', vtype=gp.GRB.{type.upper()})"
    else:
        shape_args = ", ".join(shape)
        return f"{symbol} = model.addVars({shape_args}, name='{symbol}', vtype=gp.GRB.{type.upper()})"
