#!/bin/bash

_git_dispatcher() {
    local subcommands="install update uninstall activate deactivate"
	local subcommand="$(__git_find_on_cmdline "$subcommands")"

	if [ -z "$subcommand" ]; then
		__gitcomp "$subcommands"
		return
	fi

	case "$subcommand" in
        install|update)
            __git_dispatcher_version
            return
            ;;
        *)
            COMPREPLY=()
            ;;
	esac
}

__git_dispatcher_version() {
    versions=$(git ls-remote --heads --tags https://github.com/whiskeysierra/git-dispatcher.git | grep -oE "refs/(heads|tags)/.*[^}]$" | sed -E "s/refs\/(heads|tags)\///g")
    __gitcomp "$versions"
}

# alias __git_find_on_cmdline for backwards compatibility
if [ -z "`type -t __git_find_on_cmdline`" ]; then
	alias __git_find_on_cmdline=__git_find_subcommand
fi
