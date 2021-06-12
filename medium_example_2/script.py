"""
# Example-2

This is an example integrity check that is developed with ticdat. This is an
illustration from my medium blog. The readers/others can take this up and
feel free to play around with the code.

Recall from the content on medium, you need to focus on two things -
1. *Defining the schema*
2. *Defining the rules*

Run this script by passing the following command on your terminal or whatever
way you're used to running .py files. In the original version of data
I have intentionally induced some data errors, so that you could see how ticdat
highlights the data integrity failures. Beyond example-1 this example contains
`add_data_row_predicate` and `add_foreign_key` methods.

```
python3 script.py -i ./data
```

You should see duplicates, data_type_failures, foreign key failures and data row failures printed in the program output.
Try to resolve the integrity fails or induce your own to get comfortable with
these ways.
"""

from ticdat import PanDatFactory, standard_main
from pprint import pprint
import pandas as pd

# 1. Defining the Schema >>
input_schema = PanDatFactory(
    survey = [["SSN"],["Mobile No.", "Sex", "Date-of-Birth",
                       "Hand-preference", "Income", "Monthly Expenditure"]],
    premium = [["SSN"],["Date Registered","Tenure"]]
)

# 2. Defining the data rules >>
# Highlights of this example --
input_schema.add_foreign_key("survey","premium",["SSN","SSN"])

input_schema.add_data_row_predicate(
"survey",
lambda row: row["Monthly Expenditure"] <= row["Income"],
predicate_name = "Expense cannot be grater than income",
predicate_failure_response = "Error Message")


# Beyond everything is same as in example_1
input_schema.set_data_type("premium", "SSN",
                           number_allowed=True,
                           min = 100000000,
                           max = 999999999,
                           must_be_int = True)

input_schema.set_data_type("survey", "SSN",
                           number_allowed=True,
                           min = 100000000,
                           max = 999999999,
                           must_be_int = True)

input_schema.set_data_type("survey", "Mobile No.",
                           number_allowed=True,
                           min = 999999999,
                           inclusive_min = False,
                           max = 9999999999,
                           must_be_int = True)

input_schema.set_data_type("survey", "Sex",
                          number_allowed=False,
                          strings_allowed=["Female","Male","Other"],
                          nullable=True)

input_schema.set_data_type("survey", "Date-of-Birth",
                           datetime=True)

input_schema.set_data_type("survey", "Hand-preference",
                          number_allowed=False,
                          strings_allowed=["Right","Left"])

input_schema.set_data_type("survey", "Income",
                          number_allowed=True,
                          min=0)

input_schema.set_default_value("survey", "Mobile No.", 9999999999)


# --- Following stuff is relevant to the execution of this script ---
# You can still see it, the context may be incomplete
solution_schema = PanDatFactory(
    table = [["Key"],["Values"]]
)

def solve(dat):

    # Imagine dat like an instance of your data
    # The below lines try to pass the data instance (dat)
    # through the defined rules (input_schema)

    assert input_schema.good_pan_dat_object(dat)
    duplicates = input_schema.find_duplicates(dat)
    foreign_key_fails = input_schema.find_foreign_key_failures(dat)
    data_type_fails = input_schema.find_data_type_failures(dat)
    data_row_fails = input_schema.find_data_row_failures(dat)

    print("\nDuplicates:")
    pprint(duplicates)
    print("\nForeign Key Failures:")
    pprint(foreign_key_fails)
    print("\nData Type Failures:")
    pprint(data_type_fails)
    print("\nData Row Failures:")
    pprint(data_row_fails)

    # Confirm if everything is ok?
    assert not duplicates, "Duplicates Found!"
    assert not foreign_key_fails, "Foreign Key Failures Found!"
    assert not data_type_fails, "Data Type Failures Found!"
    assert not data_row_fails, "Data Row Failures Found!"

    print("Youd Data has passed integrity checking!")
    # Do your own stuff here at this stage
    # SOME LOGICAL PROCESSING IS HAPPENING HERE AND PRODUCING OUTPUT

    # Generate your outputs
    table = pd.DataFrame(columns=["Key","Values"])
    print("NOTE: This script doesn't produce any useful output")
    return solution_schema.PanDat(**{"table":table})

if __name__=="__main__":
    standard_main(input_schema,solution_schema,solve)
