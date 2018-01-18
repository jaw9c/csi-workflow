import subprocess
import os
x = "testy123"
result = "hub pull-request -m \"" + x + "\" -h `git rev-parse --abbrev-ref HEAD` -b master -l \"master\""

out = subprocess.check_output(result, shell=True)
print(out)
