# Program Name: Transfer
# File Name: main
# Description: gets changes between two directories and merges, records, and applies them if necessary
# Notes: requires a file

#TOD0#
#check#
# make ctime unique
# check for changes (using old mpath)
# if^ there are changes, merge(hard) changes to that machines changes (0 or 1)
#
# if^ there are changes on the other machine, merge(soft) with any changes on the other machine update

#check#
# make ctime unique
# using old mpath check for changes in the mpath
# hard_merge to changes0 or 1:, record changes in the loc
# check for changes in the opposite, changes1 or 0:
# if^ soft_merge changes0 and 1:
# hard_merge changes to merged_changes0 and 1:
#apply#
# if^ make changes on the active machine, removing files from server(one drive in this case) that are no longer needed
# *all of this scheduled to run ever 10 min

#INIT#
#imports#
import mapping
import changes

#MAIN#
if __name__ == '__main__':
    print("nothing yet")

# Author: Jack Paul Martin
# Start: 1/14/2021, Completion: