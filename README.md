
Develop-local branch changed me

==================== GIT Examples ====================
example 1. develop-bill changes locally
first pull develop branch to create your local branch in the image of:
first time create local branch example:  git checkout -b develop-bill

====================
-- example to merge develop-bill into develop and merge develop into master and create a version tag
-- develop-local
git status # make sure you see the changed files you expect to see
git add -A
git commit -m "added readme notes for git examples
git push

-- develop 
git checkout develop && git pull 
git merge develop-bill
git push

-- master
git checkout main && git pull
git merge develop
git push

-- tag it
git tag -a task_id_v1.0.1 -m "Releasing version v1.0.1"
git push origin --tags

-- reload your personal branch so not to accidentially hammer master branch
git checkout develop-bill && git pull 

====================

---------- after local git init - 
To add a new remote, use the git remote add command on the terminal, in the directory your repository is stored at.
 

  git remote add origin https://github.com/OWNER/REPOSITORY.git 

  git remote -v

 main was not recognized until I did: git fetch origin 

 There was no develop so I did:
git checkout main && git pull
git checkout -b develop
git push --set-upstream origin develop
-- not you are still on main

example 1. develop-bill changes locally
first pull develop branch to create your local branch in the image of:
first time create local branch example:  git checkout -b develop-bill


====================