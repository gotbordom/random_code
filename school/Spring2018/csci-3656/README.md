# CSCI-3656 Numerical Computation

## Quick info from the [Syllabus](Syllabus.md)

CU Boulder: CSCI 3656 (Spring 2018)

Meeting Time: Tue/Thu 12:30-1:45pm in FLMG 156

## Git Repository

Course materials and homework assignments are maintained in the
[course repository](https://git.cs.colorado.edu/csci-3656/csci-3656).
You should
[fork](https://git.cs.colorado.edu/csci-3656/csci-3656/forks/new) this
repository to your account.

I like to use the SSH protocol for accessing repositories.  For that,
you will have to
[set your ssh key](https://git.cs.colorado.edu/profile/keys) in your
user settings.  If you use HTTPS, you'll need to enter your password
each time you push.

You can clone the repository by issuing this command in a terminal

    git clone git@git.cs.colorado.edu:csci-3656/csci-3656

or (via https)

    git clone https://git.cs.colorado.edu/csci-3656/csci-3656

You should also add a remote to submit homework via your fork

    git remote add -f submit git@git.cs.colorado.edu:YOURUSERNAME/csci-3656

or (via https)

    git remote add -f submit https://git.cs.colorado.edu/YOURUSERNAME/csci-3656

If configured correctly, running `git remote -v` will produce output
like

    origin  git@git.cs.colorado.edu:csci-3656/csci-3656 (fetch)
    origin  git@git.cs.colorado.edu:csci-3656/csci-3656 (push)
    submit  git@git.cs.colorado.edu:YOURUSERNAME/csci-3656 (fetch)
    submit  git@git.cs.colorado.edu:YOURUSERNAME/csci-3656 (push)

You can pull new notebooks and homework assignments using

    git pull

### Coding homework assignments

Coding homeworks are in the [homework](homework/) directory and
submitted via Git by pushing to your fork of this repository.

Specifically, you should run

    git pull

to get the latest assignments.  After completing the homework, saving
your notebook, and committing (`git commit`), you will submit your
homework by pushing the branch ('master') to your fork using

    git push submit master

Here `submit` is the name of the remote for your fork (set above) and
`master` is the name of the branch.  (You can update your homework
submission as many times as you like before the due date.)

## Moodle

Please enroll in this class on https://moodle.cs.colorado.edu.

## Notebooks

1. [Rootfinding](Rootfinding.ipynb)
