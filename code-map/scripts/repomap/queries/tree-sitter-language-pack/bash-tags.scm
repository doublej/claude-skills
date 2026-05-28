; Bash function definitions
(function_definition
  name: (word) @name.definition.function) @definition.function

; Function/command calls
(command
  name: (command_name
    (word) @name.reference.call)) @reference.call
