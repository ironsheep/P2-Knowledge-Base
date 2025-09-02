# Test File - No Blank Lines

This text has no blank line before the code.
```spin2
PUB test1()
  ' This needs a blank line inserted
```

Here's another one:

Some text immediately before code.
```spin2  
PUB test2()
  ' This also needs a blank line
```

But this one already has a blank line:

```spin2
PUB test3()
  ' This one is fine
```

And text right before again.
```pasm2
  mov x, #10
  ' PASM2 needs blank line too
```