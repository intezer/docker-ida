import idc
import idaapi
import idautils

# Initialize IDA Python
idaapi.autoWait()

# List all function names into func_names
func_names = []
for function_address in idautils.Functions():
    func_names.append(idc.GetFunctionName(function_address))

# Output function names to file
filename = idaapi.get_root_filename()
with open('%s_functions.txt' % filename, 'w') as output_file:
    output_file.write('\n'.join(func_names))

idc.Exit(0)
