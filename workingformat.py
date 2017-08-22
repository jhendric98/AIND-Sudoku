# Find all instances of naked twins

        # loop over units checking if there is are any naked twins

            # get all boxes with a length of two


            # now get all the naked pair twins ie exists twice in pairs


            # iterate through the naked_twins removing the values from the non naked twin boxes


                # loop over the boxes in the unit and remove the pair from them
                # we could use peers as instead but would still need the check to
                # ensure we aren't impacting the other naked twin

                    # test to ensure we don't eliminate the values from either naked-twin

                        # Eliminate the naked twins as possibilities for their peers
                        # the sorted is required for passing the test assertions as the box values
                        # are expected to be in numerical order.


# assign_value(values, box, values[box].replace(digits[0], ""))
# assign_value(values, box, values[box].replace(digits[1], ""))
# values[box] = values[box].replace(digits[0], "")
# values[box] = values[box].replace(digits[1], "")


'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'
'B1', 'B2', 'B3'
'C1', 'C2', 'C3'
'D1'
'E1' 
'F1'
'G1'
'H1'
'I1'
