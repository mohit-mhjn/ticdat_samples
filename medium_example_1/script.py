"""
This is an example integrity check that is developed with ticdat. This is an
illustration from my medium blog. The readers/others can take this up and
feel free to play around with.

Run this script by passing the following command on your terminal or whatever
way you're used to running .py files. In the original version of "data_file.csv"
I have intentionally induced some data errors, so that you could see how ticdat
highlights the data integrity failures.

 python3 script.py -i ./data

You should see duplicates, data_type_failures printed in the program output.
Try to resolve the integrity fails or induce your own to get comfortable with
these ways.
"""

from ticdat import PanDatFactory, standard_main
from pprint import pprint
import pandas as pd

# Defining the Schema >>
input_schema = PanDatFactory(
    survey = [["SSN"],["Mobile No.", "Sex", "Date-of-Birth",
                       "Hand-preference", "Income"]]
)

# Defining the data rules >>
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
