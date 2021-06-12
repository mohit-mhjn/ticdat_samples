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
