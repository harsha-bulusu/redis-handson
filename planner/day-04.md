* Scripting with `EVAL`, sandboxed execution

  - why should we avoid usage of global variables in lua
  ```lua
    EVAL "
      type = 'admin'

      if type(123) == 'number' then
      return 'It is a number'
      end" 0

  ERR user_script:1: Attempt to modify a readonly table script: 370aa9b30e9ccd0b8d8a2fb14d8597680beded4d, on @user_script:1.
  ```
  
* Implement:

  * Lua script for atomic stock decrement
  * Rate limiter using sorted set + Lua