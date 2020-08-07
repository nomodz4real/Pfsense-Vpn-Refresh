#!/usr/bin/python3

import tasks as t
import os
import getpass

if __name__ == "__main__":
    user = getpass.getuser()
    path = t.populate_test_files_and_vars(user)
    os.chdir(path)
    bestserver = t.get_server()
    print("Server Found: " + bestserver)
    if user == 'root':
        t.log_run(bestserver)
    t.set_pfsense_config(bestserver)
    t.reload_pfsense()
    print("\nDone!")