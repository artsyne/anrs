"""ANRS CLI shell completion support."""

import click


def get_completion_script(shell: str) -> str:
    """Generate shell completion script for the given shell."""
    from anrs.main import cli

    if shell == "bash":
        return _get_bash_completion()
    elif shell == "zsh":
        return _get_zsh_completion()
    elif shell == "fish":
        return _get_fish_completion()
    else:
        raise ValueError(f"Unsupported shell: {shell}")


def _get_bash_completion() -> str:
    """Generate bash completion script."""
    return '''# ANRS bash completion
# Add to ~/.bashrc or ~/.bash_profile:
#   eval "$(anrs completion bash)"

_anrs_completion() {
    local IFS=$'\\n'
    local response

    response=$(env COMP_WORDS="${COMP_WORDS[*]}" COMP_CWORD=$COMP_CWORD _ANRS_COMPLETE=bash_complete $1)

    for completion in $response; do
        IFS=',' read type value <<< "$completion"
        COMPREPLY+=("$value")
    done

    return 0
}

_anrs_completion_setup() {
    complete -o default -F _anrs_completion anrs
}

_anrs_completion_setup
'''


def _get_zsh_completion() -> str:
    """Generate zsh completion script."""
    return '''#compdef anrs
# ANRS zsh completion
# Add to ~/.zshrc:
#   eval "$(anrs completion zsh)"

_anrs() {
    local -a commands
    local -a options

    commands=(
        'init:Initialize ANRS in a repository'
        'status:Show ANRS status for a repository'
        'upgrade:Upgrade .anrs/ to latest version'
        'adapter:Manage AI tool adapters'
        'harness:Run quality checks'
        'doctor:Diagnose and repair installation'
    )

    _arguments -C \\
        '--version[Show version]' \\
        '--help[Show help]' \\
        '1:command:->command' \\
        '*::args:->args'

    case $state in
        command)
            _describe 'command' commands
            ;;
        args)
            case $words[1] in
                init)
                    _arguments \\
                        '--level[Installation level]:level:(minimal standard full)' \\
                        '--adapter[Install adapter]:adapter:(cursor claude-code codex opencode)' \\
                        '--force[Force overwrite]' \\
                        '--merge[Merge with existing]' \\
                        '--dry-run[Preview changes]' \\
                        '*:path:_files -/'
                    ;;
                adapter)
                    local -a subcommands
                    subcommands=(
                        'list:List available adapters'
                        'install:Install an adapter'
                    )
                    _arguments \\
                        '1:subcommand:->subcmd' \\
                        '*::subargs:->subargs'
                    case $state in
                        subcmd)
                            _describe 'subcommand' subcommands
                            ;;
                        subargs)
                            case $words[1] in
                                install)
                                    _arguments \\
                                        '1:adapter:(cursor claude-code codex opencode)' \\
                                        '--force[Force overwrite]' \\
                                        '--skip[Skip if exists]' \\
                                        '--dry-run[Preview changes]' \\
                                        '*:path:_files -/'
                                    ;;
                            esac
                            ;;
                    esac
                    ;;
                harness)
                    _arguments \\
                        '--level[Harness level]:level:(L1 L2 L3 security all)' \\
                        '--strict[Strict mode]' \\
                        '*:path:_files -/'
                    ;;
                upgrade)
                    _arguments \\
                        '--dry-run[Preview changes]' \\
                        '--force[Force upgrade]' \\
                        '--no-backup[Skip backup]' \\
                        '--list-backups[List backups]' \\
                        '*:path:_files -/'
                    ;;
                doctor)
                    _arguments \\
                        '--fix[Attempt auto-fix]' \\
                        '--verbose[Verbose output]' \\
                        '*:path:_files -/'
                    ;;
                status)
                    _arguments '*:path:_files -/'
                    ;;
            esac
            ;;
    esac
}

_anrs "$@"
'''


def _get_fish_completion() -> str:
    """Generate fish completion script."""
    return '''# ANRS fish completion
# Add to ~/.config/fish/completions/anrs.fish

complete -c anrs -f

# Main commands
complete -c anrs -n __fish_use_subcommand -a init -d 'Initialize ANRS'
complete -c anrs -n __fish_use_subcommand -a status -d 'Show status'
complete -c anrs -n __fish_use_subcommand -a upgrade -d 'Upgrade .anrs/'
complete -c anrs -n __fish_use_subcommand -a adapter -d 'Manage adapters'
complete -c anrs -n __fish_use_subcommand -a harness -d 'Run quality checks'
complete -c anrs -n __fish_use_subcommand -a doctor -d 'Diagnose installation'

# init options
complete -c anrs -n "__fish_seen_subcommand_from init" -l level -d 'Level' -a 'minimal standard full'
complete -c anrs -n "__fish_seen_subcommand_from init" -l adapter -d 'Adapter' -a 'cursor claude-code codex opencode'
complete -c anrs -n "__fish_seen_subcommand_from init" -l force -d 'Force overwrite'
complete -c anrs -n "__fish_seen_subcommand_from init" -l merge -d 'Merge config'
complete -c anrs -n "__fish_seen_subcommand_from init" -l dry-run -d 'Preview'

# adapter subcommands
complete -c anrs -n "__fish_seen_subcommand_from adapter" -a list -d 'List adapters'
complete -c anrs -n "__fish_seen_subcommand_from adapter" -a install -d 'Install adapter'

# harness options
complete -c anrs -n "__fish_seen_subcommand_from harness" -l level -d 'Level' -a 'L1 L2 L3 security all'
complete -c anrs -n "__fish_seen_subcommand_from harness" -l strict -d 'Strict mode'

# doctor options
complete -c anrs -n "__fish_seen_subcommand_from doctor" -l fix -d 'Auto-fix'
complete -c anrs -n "__fish_seen_subcommand_from doctor" -l verbose -d 'Verbose'
'''


@click.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell: str) -> None:
    """Generate shell completion script.

    Output the completion script for the specified shell.
    Add to your shell config to enable tab completion.

    \b
    Examples:
      # Bash (~/.bashrc)
      eval "$(anrs completion bash)"

      # Zsh (~/.zshrc)
      eval "$(anrs completion zsh)"

      # Fish (~/.config/fish/completions/anrs.fish)
      anrs completion fish > ~/.config/fish/completions/anrs.fish
    """
    click.echo(get_completion_script(shell))
