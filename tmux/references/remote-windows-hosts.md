# Remote Windows Hosts (SSH/SCP)

Canonical reference for working with Windows machines over SSH from a terminal
session (tmux, iTerm2, cmux — the driver doesn't matter, the gotchas are the same).

## SCP path gotcha

`scp` to Windows absolute paths **always fails** — the `C:` colon is parsed as a host separator:

```bash
# BROKEN — all of these fail:
scp file.txt user@host:"C:/Projects/foo/file.txt"
scp file.txt user@host:"C:\\Projects\\foo\\file.txt"

# WORKS — scp to home dir, then move via SSH:
scp file.txt user@host:file.txt
ssh user@host "move file.txt C:\\Projects\\foo\\file.txt"
```

## Writing file content directly

For small files, skip scp entirely and write via SSH stdin:

```bash
ssh user@host "cmd /c \"copy con C:\\Projects\\foo\\file.txt\"" < local-file.txt
# Or use PowerShell:
cat local-file.txt | ssh user@host "powershell -c \"[IO.File]::WriteAllText('C:\\Projects\\foo\\file.txt', \$input)\""
```

## Windows path rules in SSH commands

- Use **backslashes** inside `cmd /c` commands: `C:\\Projects\\foo`
- Use **forward slashes** inside PowerShell: `C:/Projects/foo`
- Always double-escape backslashes in bash strings
