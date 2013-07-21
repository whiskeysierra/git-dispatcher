[![Railway turntable and roundhouse](icon.png)](http://commons.wikimedia.org/wiki/File:Train_roundhose_1909.jpg)

# Git Dispatcher [![Build Status](https://travis-ci.org/whiskeysierra/git-dispatcher.png?branch=master)](http://travis-ci.org/whiskeysierra/git-dispatcher)

`git dispatcher` is a custom git command which simplifies the installation and usage of git hooks manage by
[Git Hooks](https://github.com/whiskeysierra/git-hooks).

## Requirements

- Python 2.6 or 2.7
 
To install the required python libraries run:
    
    sudo pip install -r requirements.txt

## Installation
The easiest way to install `git dispatcher` is to checkout the repository and add an alias to your `.gitconfig`:

    git clone git@github.com:whiskeysierra/git-dispatcher.git ~/.git-dispatcher
    git config --global --add alias.dispatcher '!~/.git-ignore/git-dispatcher.py'
    
Alternatively, in case you have `~/bin` in your PATH, you may also just add a link to `git-dispatcher.py`:

    ln -s ~/bin/git-dispatcher ~/.git-dispatcher/git-dispatcher.py
    
Optionally, you may want to enable bash completion for `git dispatcher`:

    echo "source ~/.git-dispatcher/git-dispatcher-completion.bash" >> ~/.bashrc
    
## Quickstart
To install git hooks to your existing repository, just:

    cd path/to/your/project
    git dispatcher install
    
The [Git Hooks](https://github.com/whiskeysierra/git-hooks) tool is now installed in `path/to/your/project/.git-hooks`.
Technically it is a subtree, you'll have one (or two) new commits in your repository.

The dispatcher is installed, but not yet activated. To enable it, run:

    git dispatcher activate
    
For every known git hook, that is not yet occupied by an existing script, the dispatcher will be linked and used as
the hook script. To enable one or more custom hooks, create them in `path/to/your/project/git-hooks/<hook>.d/`.

For more details about the features and usage of [Git Hooks see here](https://github.com/whiskeysierra/git-hooks).

## Attributions
![Public Domain](http://i.creativecommons.org/p/mark/1.0/80x15.png)
The train roundhouse photo from [Wikimedia Commons](http://commons.wikimedia.org/wiki/File:Train_roundhose_1909.jpg) is in the
[Public Domain](http://en.wikipedia.org/wiki/public_domain).


