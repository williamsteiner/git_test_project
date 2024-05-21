def generate_power_query(column_name, step_label):
    step_label = '#"' + step_label + '"'
    col_label = "_" + column_name.lower()
    new_step_label = '#"Added custom' + col_label 
    steps = [
        (f', {new_step_label}"' , f"{step_label}"        , "_year", "Date.Year"),
        (f'{new_step_label}_a"' , f'{new_step_label}"'   , "_month", "Date.Month"),
        (f'{new_step_label}_b"' , f'{new_step_label}_a"' , "_day", "Date.Day"),
        (f'{new_step_label}_c"' , f'{new_step_label}_b"' , "_mo_name", "Date.MonthName"),
        (f'{new_step_label}_d"' , f'{new_step_label}_c"' , "_qtr", '"Qtr " & Text.From(Date.QuarterOfYear')
    ]
    
    query = []
    counter =0
    for step in steps:
        counter +=1
        step_name, previous_step, suffix, func = step 
        #if suffix == "_qtr":
        #    line = f'  {step_name} = Table.AddColumn({previous_step}, "_{column_name.lower()}{suffix}", each {func}([{column_name}]))'
        #else:
        #    line = f'  {step_name} = Table.AddColumn({previous_step}, "_{column_name.lower()}{suffix}", each {func}([{column_name}]))'
        if counter <5:
            add_last_char = ","
        else:
            add_last_char = ")"     
        line = f'  {step_name} = Table.AddColumn({previous_step}, "_{column_name.lower()}{suffix}", each {func}([{column_name}]))' + add_last_char
        query.append(line)
    
    query.append(f'in \n  {step_name}')
    
    return '\n'.join(query)

# Prompt the user to input the column name and step label
column_name = input("Enter the column name: ")
step_label = input("Enter the step label: ")

# Generate the Power Query M code
power_query_code = generate_power_query(column_name, step_label)
print("\nGenerated Power Query M Code:\n")
print(power_query_code)

