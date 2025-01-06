prompt_template = """
You're an expert programmer in a team of optimization experts. The goal of the team is to solve an optimization or satisfaction problem. Your task is to debug a piece of code that's written in Python using the Minizinc Python library. 

Here's the code:

-----
{code}
-----

Here's the error message:

-----
{error_message}
-----


Take a deep breath, and solve the problem step by step.
"""