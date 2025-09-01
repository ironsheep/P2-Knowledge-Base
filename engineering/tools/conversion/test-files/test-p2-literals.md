# Test P2 Literals Protection

## In Text
The #immediate value uses # for immediates, $ for hex like $FF_AA, % for binary like %1010_0001, and _ for separators.

## Mixed with Images
Here's an image ![Test](assets/test_image.png) and then P2 text: Use #25_000_000 for half-second delay.

## Code Block (should NOT be escaped)
```pasm2
mov x, #42
waitx ##25_000_000
wrlong data, ##$1000
```

## More Text
The value $1_0000_0000 represents full circle with 2^32 positions.