# Part Title Test

This is a part-level content that should trigger the Part/Chapter logic.

## Chapter Title Test  

This chapter should follow the part without causing brace errors.

### Section with Code

```spin2
CON
  TEST_PIN = 10

PUB main()
  pinstart(TEST_PIN, P_TRANSITION, 1000, 0)
```

This tests both the Part/Chapter formatting and the code block rendering that was causing the `\thispagestyle has an extra }` error.