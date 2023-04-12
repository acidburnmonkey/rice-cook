import subprocess
programs =[]

with open("data.txt", 'r') as file:
    for line in file:
        programs.append(line.strip())
    print(programs)

try:
    subprocess.check_call(['dnf', 'install', *programs])   
except:
    print(Exception())











'''
def programs_installed_check(programs):
    missing_programs = []
    for program in programs:
        result = os.system(f"which {program} > /dev/null 2>&1")
        if result != 0:
            missing_programs.append(program)
    if missing_programs:
        print(f"The following programs are missing: {', '.join(missing_programs)}")
        return False
    else:
        print("All programs are installed.")
        return True


programs_to_check = ["awk", "sed", "grffffep"]
programs_installed_check(programs_to_check)
'''
